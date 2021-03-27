# import libraries
import requests
from bs4 import BeautifulSoup
import re

print('Starting...')

#url to be scraped
url = 'https://old.reddit.com/r/GameDeals/'

headers = {'User-Agent': 'Mozilla/5.0'}

#gets the reponse
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")

#get all the deals in the page
deals = soup.find_all('a', attrs={'class': 'title may-blank outbound'})

#Threshold : If discount is above this, get the deal
discountThreshold = 75.0

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
	
	finalText = store + '|' + title + '|' + deal['href'] + '|' + status
	
	#Get the deal if big discount and not expired
	if(status!='Expired' and isBigDiscount):
		print(finalText)  
		#print ("")
