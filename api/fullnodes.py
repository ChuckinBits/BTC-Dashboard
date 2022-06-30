import config
import json
import requests
from urllib.request import urlopen
from json import loads

def nodes():
	status = 0
	try:
		node_url = 'https://luke.dashjr.org/programs/bitcoin/files/charts/data/uainfo.json'
		node_api_request = urlopen(node_url).read()
		nodes = loads(node_api_request)

		listening = 0
		unreachable = 0
		sat = "Satoshi"

		for key, value in nodes.items():
			if sat in key:
				listening = value['listening'] + listening
				unreachable = value['est_unreachable'] + unreachable
		config.totalnodes = listening + unreachable
		print("Updated Full Nodes")
		config.nodeserror = 0
	except:
		try:
			urltest = requests.get(node_url)
			status = urltest.status_code
			urltest.close()
			config.nodeserror = 1
			print("Error reading Nodes. Status code: " + str(status))
		except:
			config.nodeserror = 2
			print("Nodes Connection Refused ")
	if config.nodeserror == 1:
		config.ne1 = "Nodes "
		config.ne2 = ""
	elif config.nodeserror == 2:
		config.ne1 = ""
		config.ne2 = "Nodes "
	else:
		config.ne1 = ""
		config.ne2 = ""
