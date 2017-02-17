from bs4 import BeautifulSoup
from DBConnector import DBConnector
import os
import urllib3
import datetime as dt


class PoeTradeScraper:

	def __init__(self, league):

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
		47: 'Master Sextant'
		}

		#League for data scraping
		self.league = league

		# Temporary list to store exchange data for database insertion
		self.data=[]
		
		# HTTP handle for requests and responses
		self.http=urllib3.PoolManager()

		# Setup the log file for this session
		dir_path = os.path.dirname(os.path.realpath(__file__))
		self.log = open(dir_path+'/logs/'+dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'_log.txt','w')

		# Init DB class with the DB info
		self.db = DBConnector('the_warehouse', 'poecurrency', 'poecurrency', self.log)
		self.table_info=["poe_currency_"+self.league,"(time, exchange, have_name, have_value, want_name, want_value, ratio_h_w, ratio_w_h)", "(%s, %s, %s, %s, %s, %s, %s, %s)"]

	def __del__(self):
		self.log.close()

	def scrape(self):
		# Get the start time of the scrape
		start_time = dt.datetime.now()
		# Write to log and console
		self.log.write('PoE Trade Scrape started at: '+str(start_time))
		self.log.write('\n------------------------------------------------------\n')
		print('\nPoE Trade Scrape started at: ', start_time)

		#Connect to DB
		print('Connecting to DB...')
		self.db.connect()

		# For each currency
		for want in self.currencies:
		    # Get the ratio to other currencies
			for have in self.currencies:
				if want == have:
					continue

				# Get the HTML Source
				url = 'http://currency.poe.trade/search?league='+self.league+'&online=x&want=' + str(want) + '&have=' + str(have)
				response = self.http.request('GET', url)

				# Parse the HTML Source
				soup = BeautifulSoup(response.data, 'html.parser')

				first = True
				# Get all of the buy and sell values
				for i in soup.findAll("div", {"data-sellvalue": True}):
					hv = float(i.get("data-buyvalue"))
					wv = float(i.get("data-sellvalue"))

					ratio_h_w = round((wv / hv), 3)
					ratio_w_h = round((hv / wv), 3)

					# Logic to discard bogus or inverted ratios by using first ratio as a base
					# If this is the first ratio, check if it is greater or less than 1
					if first and ratio_h_w >= 1:
						# If greater than 1, we want to make sure all ratios greater than one are stored
						rc = 1
						first = False
					elif first:
						# If less than 1, we want to make sure all ratios less than one are stored
						rc = 0
						first = False

					# All the rest of the ratios
					# If ratio is less than 1 and rc == 1, then we skip this ratio
					if ratio_h_w < 1 and rc == 1:
						continue
					# If ratio is greater than 1 and rc == 0, then we skip this ratio
					elif ratio_h_w > 1 and rc == 0:
						continue

					# Append them to the data array
					self.data.append([start_time, True, self.currencies[have], hv, self.currencies[want], wv, ratio_h_w, ratio_w_h])

				# Exchanges found and example
				if self.data:
					print('Have: ', self.currencies[have], ' Want: ', self.currencies[want])
					print('Exchanges found...')
					print('Example: ', self.data[0])
				else:
					print('Have: ', self.currencies[have], ' Want: ', self.currencies[want])
					print('No exchanges found')
					self.data.append([start_time, False, self.currencies[have], 0, self.currencies[want], 0, 0, 0])

				# Insert into the database
				print('Calling DB connector...')
				self.db.insert(self.table_info,self.data)

				# Update log on completion of currency type
				self.log.write('\n'+self.currencies[want]+' exchanges completed.')
				# Clear price ratio list
				self.data = []

		# End time of the scrape
		end_time = dt.datetime.now()

		# Write to log and console
		self.log.write('\n------------------------------------------------------\n')
		self.log.write('\nPoE Trade Scrape started at: '+str(start_time))
		self.log.write('\nPoE Trade Scrape ended at: '+ str(start_time))
		self.log.write('\nTime to scrape: '+str((end_time - start_time)))

		print('\nPoE Trade Scrape started at: ', start_time)
		print('PoE Trade Scrape ended at: ', start_time)
		print('Time to scrape: ', (end_time - start_time))
