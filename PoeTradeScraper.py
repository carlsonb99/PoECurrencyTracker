from bs4 import BeautifulSoup
from DBConnector import DBConnector
import urllib3
import datetime as dt


class PoeTradeScraper:

	def __init__(self):

		# Dictionary of all the currencies for poe.trade
		self.currencies={
		1: 'Orb of Alteration',
		2: 'Orb of Fusing',
		3: 'Orb of Alchemy',
		4: 'Chaos Orb',
		5: 'Gemcutter\'s Prism',
		6: 'Exalted Orb',
		7: 'Chromatic Orb',
		8: 'Jeweler\'s Orb', 
		9: 'Orb of Chance', 
		10: 'Cartographer\'s Chisel', 
		11: 'Orb of Scouring', 
		12: 'Blessed Orb',
		13: 'Orb of Regret', 
		14: 'Regal Orb', 
		15: 'Divine Orb', 
		16: 'Vaal Orb', 
		17: 'Scroll of Wisdom', 
		18: 'Portal Scroll', 
		19: 'Armourer\'s Scrap',
		20: 'Blacksmith\'s Whetstone', 
		21: 'Glassblower\'s Bauble', 
		22: 'Orb of Transmutation', 
		23: 'Orb of Augmentation', 
		24: 'Mirror of Kalandra',
		25: 'Eternal Orb', 
		26: 'Perandus Coins', 
		27: 'Sacrifice at Dusk', 
		28: 'Sacrifice at Midnight', 
		29: 'Sacrifice at Dawn', 
		30: 'Sacrifice at Noon',
		31: 'Mortal Grief', 
		32: 'Mortal Rage', 
		33: 'Mortal Hope', 
		34: 'Mortal Ignorance', 
		35: 'Silver Coin',
		40: 'Offering to the Godess', 
		41: 'Fragment of the Hydra',
		42: 'Fragment of the Pheonix', 
		43: 'Fragment of the Minotaur', 
		43: 'Fragment of the Chimera', 
		45: 'Apprentice Sextant', 
		46: 'Journeyman Sextant', 
		7: 'Master Sextant'
		}

		# Temporary list to store exchange data for database insertion
		self.data=[]
		
		# HTTP handle for requests and responses
		self.http=urllib3.PoolManager()

		#Init DB class with the DB info
		self.db = DBConnector('the_warehouse', 'poecurrency', 'poecurrency')
		self.table_info=["PoECurrency","(time, exchange, bv_name, bv_value, sv_name, sv_value)", "(%s, %s, %s, %s, %s, %s)"]

	def scrape(self):
		# Get the start time of the scrape
		start_time = dt.datetime.now()
		print('\nPoE Trade Scrap started at: ', start_time)

		#Connect to DB
		print('Connecting to db...')
		self.db.connect()

		# For each currency
		for want in self.currencies:
		    # Get the ratio to other currencies
			for have in self.currencies:
				if want == have:
					continue

				# Get the HTML Source
				url = 'http://currency.poe.trade/search?league=Breach&online=x&want=' + str(want) + '&have=' + str(have)
				response = self.http.request('GET', url)

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
					self.data.append([start_time, True, self.currencies[have], bv, self.currencies[want], sv])

				# Test print
				if self.data:
					print('Have: ', self.currencies[have], ' Want: ', self.currencies[want])
					print('Exchanges found...')
					print('Example: ', self.data[0])
				else:
					print('Have: ', self.currencies[have], ' Want: ', self.currencies[want])
					print('No exchanges found')
					self.data.append([start_time, False, self.currencies[have], 0, self.currencies[want], sv])

				# Insert into the database
				print('Adding to database...')
				self.db.insert(self.table_info,self.data)

				# Clear price ratio list
				self.data = []

			break

		end_time = dt.datetime.now()

		print('\nPoE Trade Scrap ended at: ', start_time)
		print('Time to scrap: ', (end_time - start_time))
