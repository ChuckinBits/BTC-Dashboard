import config
import time
import threading
from api.alternative import alt
from api.bitstamp import bitstamp
from api.mempool import mempoolspace
from api.ml1 import ml1
from api.fullnodes import nodes
from api.blockchair import blockchair
from api.coingecko import coingecko
from api.nobsbitcoin import nobsbitcoin

ml1start = altstart = bitstampstart = blockchairstart = coingeckostart = mempoolstart = nodestart = nobsstart = time.time()

def initialCall():
	bitstamp()
	coingecko()
	mempoolspace()
	blockchair()
	alt()
	nodes()
	ml1()
	nobsbitcoin()

def apiCall():
	global ml1start, altstart, bitstampstart, blockchairstart, coingeckostart, mempoolstart, nodestart, nobsstart
	config.refreshtime = config.new_refreshtime
	global bitstamp_thread, coingecko_thread, mempool_thread, blockchair_thread, alt_thread, nobs_thread, nodes_thread, ml1_thread, merge_thread

	try:
		if merge_thread.is_alive() == True:
			print("Merge Thread is Alive")
			merge_thread.join()
		else:
			pass
	except NameError:
		pass
	print('Starting threads for API data')
	#Free API Requests Limit Enforcement
	# Bitstamp allows 800 calls per minute	
	if time.time() - bitstampstart > 0.1:
		bitstamp_thread = threading.Thread(target=bitstamp, name="Bitstamp")
		bitstamp_thread.start()
		bitstampstart = time.time()

	# Coingecko allows 100 calls per minute
	if time.time() - coingeckostart > 1:
		coingecko_thread = threading.Thread(target=coingecko, name="CoinGecko")
		coingecko_thread.start()
		coingeckostart = time.time()

	#Mempool allows 200 calls per minute
	if time.time() - mempoolstart > 2:
		mempool_thread = threading.Thread(target=mempoolspace, name="Mempool")
		mempool_thread.start()
		mempoolstart = time.time()

	#Blockchair allows 1 call per minute
	if time.time() - blockchairstart > 60:
		blockchair_thread = threading.Thread(target=blockchair, name="BlockChair")
		blockchair_thread.start()
		blockchairstart = time.time()
			
	# Alternative updates their data every 5 minutes
	# However Alternative allows 60 calls per minute
	# Set to 2.5 minutes so it will reasonably catch changes without needlessy spamming
	if time.time() - altstart > 150:
		alt_thread = threading.Thread(target=alt, name="Alternative")
		alt_thread.start()
		altstart = time.time()
	# NoBSBitcoin unknown limit, set to 5 minutes to be safe 
	if time.time() - nobsstart > 300:
		nobs_thread = threading.Thread(target=nobsbitcoin, name="NoBSBitcoin")
		nobs_thread.start()
		nobsstart = time.time()
	
	# Nodes unknown API Limit, set to 5 minutes to be safe
	if time.time() - nodestart > 300:
		nodes_thread = threading.Thread(target=nodes, name="Nodes")
		nodes_thread.start()
		nodestart = time.time()

	# 1ML unknown API Limit, set to 5 minutes to be safe
	if time.time() - ml1start > 300:
		ml1_thread = threading.Thread(target=ml1, name="ML1")
		ml1_thread.start()
		ml1start = time.time()
	
	if config.refreshtime < 30000:
		merge_thread = threading.Thread(target=threads_check, name="MergeThread")
		merge_thread.start()
	else:
		threads_check()

def threads_check():
	try:
		if bitstamp_thread.is_alive() == True:
			#print("Bitstamp Thread is Alive")
			#config.bitstamp_dead = False
			bitstamp_thread.join()
			#print("Bitstamp Thread Joined")
		else:
			pass
			#config.bitstamp_dead = True
	except NameError:
		pass
		#config.bitstamp_dead = True
	try:
		if coingecko_thread.is_alive() == True:
			#print("CoinGecko Thread is Alive")
			coingecko_thread.join()
		else:
			pass
			#print("CoinGecko Thread is Dead")
			#cgt = False
	except NameError:
		pass
		#cgt = False
	try:
		if mempool_thread.is_alive() == True:	
			#print("Mempool Thread is Alive")
			mempool_thread.join()
		else:
			pass
			#print("Mempool Thread is Dead")
			#mpt = False
	except NameError:
		pass
		#mpt = False
	try:
		if blockchair_thread.is_alive() == True:
			#print("Blockchair Thread is Alive")
			blockchair_thread.join()
		else:
			pass
			#print("Blockchair Thread is Dead")
			#bct = False
	except NameError:
		pass
		#bct = False
	try:
		if alt_thread.is_alive() == True:
			#print("Alt Thread is Alive")
			alt_thread.join()
		else:
			pass
			#print("Alt Thread is Dead")
	except NameError:
		pass
		#altt = False
	try:
		if nobs_thread.is_alive() == True:
			#print("NoBS Thread is Alive")
			nobs_thread.join()
		else:
			pass
			#print("NoBS Thread is Dead")
			#nobst = False
	except NameError:
		pass
		#nobst = False
	try:
		if nodes_thread.is_alive() == True:
			#print("Nodes Thread is Alive")
			nodes_thread.join()
		else:
			pass
			#print("Nodes Thread is Dead")
			#nt = False
	except NameError:
		pass
		#nt = False
	try:
		if ml1_thread.is_alive() == True:
			#print("ML1 Thread is Alive")
			ml1_thread.join()
		else:
			pass
			#print("ML1 Thread is Dead")
			#ml1t = False
	except NameError:
		pass
	print("All Threads Joined")
	#print(threading.enumerate())