from bs4 import BeautifulSoup
import urllib
import re

prices = []

# Get the HTML Source
filehandle = urllib.request.urlopen('http://currency.poe.trade/search?league=Breach&online=x&want=6&have=4')

# Parse the HTML Source
soup=BeautifulSoup(filehandle.read(),'html.parser')


#Get all of the buy and sell values and add them to the prices array
for i in soup.findAll("div", {"data-sellvalue":True}):
	prices.append([i.get("data-sellvalue"), i.get("data-buyvalue")])

print(prices)
