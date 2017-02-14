from bs4 import BeautifulSoup
import urllib
import re

# Dictionary of all the currencies for poe.trade
currencies = {1: 'Orb of Alteration', 2: 'Orb of Fusing', 3: 'Orb of Alchemy', 4: 'Chaos Orb', 5: 'Gemcutter\'s Prism', 6: 'exalted',
              7: 'Chromatic Orb', 8: 'Jeweler\'s Orb', 9: 'Orb of Chance', 10: 'Cartographer\'s Chisel', 11: 'Orb of Scouring', 12: 'Blessed Orb',
              13: 'Orb of Regret', 14: 'Regal Orb', 15: 'Divine Orb', 16: 'Vaal Orb', 17: 'Scroll of Wisdom', 18: 'Portal Scroll', 19: 'Armourer\'s Scrap',
              20: 'Blacksmith\'s Whetstone', 21: 'Glassblower\'s Bauble', 22: 'Orb of Transmutation', 23: 'Orb of Augmentation', 24: 'Mirror of Kalandra',
              25: 'Eternal Orb', 26: 'Perandus Coins', 35: 'Silver Coin', 27: 'Sacrifice at Dusk', 28: 'Sacrifice at Midnight', 29: 'Sacrifice at Dawn', 30: 'Sacrifice at Noon',
              31: 'Mortal Grief', 32: 'Mortal Rage', 33: 'Mortal Hope', 34: 'Mortal Ignorance', 40: 'Offering to the Godess', 41: 'Fragment of the Hydra',
              42: 'Fragment of the Pheonix', 43: 'Fragment of the Minotaur', 43: 'Fragment of the Chimera', 45: 'Apprentice Sextant', 46: 'Journeyman Sextant', 47: 'Master Sextant'}

# Temporary list to store price ratios
prices = []

# For each currency
for want in currencies:
    # Get the ratio to other currencies
    for have in currencies:
        if want == have:
            continue
        # Get the HTML Source
        filehandle = urllib.request.urlopen(
            'http://currency.poe.trade/search?league=Breach&online=x&want=' + str(want) + '&have=' + str(have))

        # Parse the HTML Source
        soup = BeautifulSoup(filehandle.read(), 'html.parser')

        # Get all of the buy and sell values and add them to the prices array
        for i in soup.findAll("div", {"data-sellvalue": True}):
            prices.append([i.get("data-buyvalue"), i.get("data-sellvalue")])

        # Test print
        print('Have: ', currencies[have], '\nWant: ', currencies[want])
        if prices:
            print(prices[0])
        # Clear price ratio list
        prices = []

                # Get the HTML Source
        filehandle = urllib.request.urlopen(
            'http://currency.poe.trade/search?league=Breach&online=x&want=' + str(have) + '&have=' + str(want))

        # Parse the HTML Source
        soup = BeautifulSoup(filehandle.read(), 'html.parser')

        # Get all of the buy and sell values and add them to the prices array
        for i in soup.findAll("div", {"data-sellvalue": True}):
            prices.append([i.get("data-buyvalue"), i.get("data-sellvalue")])

        # Test print
        print('Have: ', currencies[want], '\nWant: ', currencies[have])
        if prices:
            print(prices[0])
        # Clear price ratio list
        prices = []
