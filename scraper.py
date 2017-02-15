from bs4 import BeautifulSoup
from DBConnector import DBConnector
import urllib3
import datetime as dt
import time

# Dictionary of all the currencies for poe.trade
currencies = {	1: 'Orb of Alteration', 2: 'Orb of Fusing', 3: 'Orb of Alchemy', 4: 'Chaos Orb', 5: 'Gemcutter\'s Prism', 6: 'exalted',
				7: 'Chromatic Orb', 8: 'Jeweler\'s Orb', 9: 'Orb of Chance', 10: 'Cartographer\'s Chisel', 11: 'Orb of Scouring', 12: 'Blessed Orb',
				13: 'Orb of Regret', 14: 'Regal Orb', 15: 'Divine Orb', 16: 'Vaal Orb', 17: 'Scroll of Wisdom', 18: 'Portal Scroll', 19: 'Armourer\'s Scrap',
				20: 'Blacksmith\'s Whetstone', 21: 'Glassblower\'s Bauble', 22: 'Orb of Transmutation', 23: 'Orb of Augmentation', 24: 'Mirror of Kalandra',
				25: 'Eternal Orb', 26: 'Perandus Coins', 35: 'Silver Coin', 27: 'Sacrifice at Dusk', 28: 'Sacrifice at Midnight', 29: 'Sacrifice at Dawn', 30: 'Sacrifice at Noon',
				31: 'Mortal Grief', 32: 'Mortal Rage', 33: 'Mortal Hope', 34: 'Mortal Ignorance', 40: 'Offering to the Godess', 41: 'Fragment of the Hydra',
				42: 'Fragment of the Pheonix', 43: 'Fragment of the Minotaur', 43: 'Fragment of the Chimera', 45: 'Apprentice Sextant', 46: 'Journeyman Sextant', 47: 'Master Sextant'}

# Temporary list to store exchange data for database insertion
data = []
http = urllib3.PoolManager()

# Get the start time of the scrape
start_time = dt.datetime.now()
print('PoE Trade Scrap started at: ', start_time)

# For each currency
for want in currencies:
	# Get the ratio to other currencies
	for have in currencies:
		if want == have:
			continue

		# Get the HTML Source
		url = 'http://currency.poe.trade/search?league=Breach&online=x&want=' + str(want) + '&have=' + str(have)
		response = http.request('GET', url)

		# Parse the HTML Source
		soup = BeautifulSoup(response.data, 'html.parser')

		# Get all of the buy and sell values
		for i in soup.findAll("div", {"data-sellvalue": True}):
			bv = float(i.get("data-buyvalue"))
			sv = float(i.get("data-sellvalue"))

			# Bring the ratio down to 1 unit of currency
			if bv >= sv:
				bv = round((bv / sv), 3)
				sv = 1
			else:
				sv = round((sv / bv), 3)
				bv = 1

			# Append them to the data array
			data.append([dt.datetime.now(), True, currencies[have], bv, currencies[want], sv])

		# Test print
		if data:
			print('Exchanges found...')
			print('Example: ', data[0])
		else:
			print('No exchanges found')

		# Insert into the database
		print('Adding to database...')

		# Clear price ratio list
		data = []

	break

end_time = dt.datetime.now()

print('PoE Trade Scrap ended at: ', start_time)
print('Time to scrap: ', (end_time - start_time))
