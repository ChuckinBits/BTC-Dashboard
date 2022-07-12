import config
#import datetime
import feedparser
import requests
#import time
from urllib.request import urlopen

def nobsbitcoin():
	status = 0
	try:
		config.news = feedparser.parse('https://rss.app/feeds/a7pA7KDznTPqIyqR.xml')
		print("NoBSBitcoin Feed Refreshed")
	except:
		try:
			urltest = requests.get(news_url)
			status = urltest.status_code
			urltest.close()
			config.bserror = 1
			print("Error Reading NoBSBitcoin. Status code: " + str(status))
		except:
			config.nobserror = 2
			print("NoBSBitcoin Connection Refused ")
	if config.nobserror == 1:
		config.nobs1 = "NoBSBitcoin "
		config.nobs2 = ""
	elif config.nobserror == 2:
		config.nobs1 = ""
		config.nobs2 = "NoBSBitcoin "
	else:
		config.nobs1 = ""
		config.nobs2 = ""