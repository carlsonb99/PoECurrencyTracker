import sys
from PoeTradeScraper import PoeTradeScraper


def main(league):
	# Create the PoeTradeScraper object
	pts = PoeTradeScraper(league)

	# Start the scrape
	pts.scrape()

if __name__ == "__main__":
    main(sys.argv[1])