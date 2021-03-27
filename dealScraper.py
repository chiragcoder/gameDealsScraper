# import libraries
import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import smtplib

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

		soup = BeautifulSoup(response.content, "html.parser")

		#get all the deals in the page
		deals = soup.find_all('a', attrs={'class': 'title may-blank outbound'})

		for deal in deals:

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
			
			#Span contains whether deal expired or not
			span = deal.parent.find('span').text
			status = 'Expired' if span == 'Expired' else 'Active'
			
			finalText = store + '\n' + title.strip() + '\n' + deal['href'] + '\n\n'
			
			#Get the deal if big discount and not expired, and deal not already sent
			if(status!='Expired' and isBigDiscount and finalText not in sentSet):
				sentSet.add(finalText)
				mailContent = mailContent + finalText
				print(finalText)
				

		if(mailContent!=''):
			print("Sending mail...")
			sendMail(mailContent)
			print("Mail sent")

	except Exception as e:
		print(e)

	#Seconds
	time.sleep(30 * 60)