# import libraries
import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import smtplib
import traceback

senderId = ''
senderPass = ''
receiverID = ''

def sendMail(mailBody):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication, sender mail, sender password
    s.login(senderId, senderPass)

    # message to be sent
    message = 'Subject: {}\n\n{}'.format('New game deals found', mailBody)

    # sending the mail. Encode because euro symbol break the code
	# sender mail, receiver mail
    s.sendmail(senderId, receiverID, message.encode("utf8"))

    # terminating the session
    s.quit()

print('Starting...')

#url to be scraped
url = 'https://old.reddit.com/r/GameDeals/'

headers = {'User-Agent': 'Mozilla/5.0'}

#Threshold : If discount is above this, get the deal
discountThreshold = 75.0

#Set which contains deals that have been sent already
sentSet = {'1'}
sentSet.remove('1')

while True:

	try:

		print('Checking deals...',datetime.datetime.now())

		mailContent = ''

		#gets the response
		response = requests.get(url, headers=headers)

		soup = BeautifulSoup(response.text, "html.parser")

		#get all the deals in the page.
		#All the 'a' elements containing "title may-blank".
		deals = soup.find_all('a', re.compile("title may-blank"))

		for deal in deals:

			try:

				#Remove [] from store string
				store = deal.text.split(']')[0].strip('[')
				title = deal.text.split(']')[1]

				#Find all numbers in the title which are followed by %
				discounts = re.findall(r'\d+%', title)

				isBigDiscount = False

				for discount in discounts:
					#remove the %
					discountFloat = float(discount.strip('%'))
					if(discountFloat >= discountThreshold):
						isBigDiscount = True
						break
				
				#TODO Active or Expired

				href = deal.get('href')

				#IF direct link not mentioned
				if('/r/GameDeals' in deal.get('href')):
					href = 'https://www.reddit.com' + href

				finalText = store + '\n' + title.strip() + '\n' + href + '\n\n'
				

				#Get the deal if big discount, and deal not already sent
				if(isBigDiscount and finalText not in sentSet):
					sentSet.add(finalText)
					mailContent = mailContent + finalText
					print(finalText)

			except Exception as e:
				traceback.print_exc()
				print(deal.text,'\n\n')

		if(mailContent!=''):
			print("Sending mail...")
			sendMail(mailContent)
			print("Mail sent")

	except Exception as e:
		traceback.print_exc()

	#Seconds
	time.sleep(30 * 60)