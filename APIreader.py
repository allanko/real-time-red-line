import math, requests, threading

from IllegalArgumentException import *
from time import sleep

class APIreader(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

		self.__trains = {}
		self.api_lock = threading.RLock()

		self.apikey = 'GwqjDwWhr0-t3m91D7T1Qw'
		self.route = 'Red'
		self.dataformat = 'json'

	def getTrains(self):
		self.api_lock.acquire() # start conditional critical region
		trains = self.__trains
		self.api_lock.release() # end conditional critical region

		return trains

	def APIget(self):
		# queries the API and gets the json file through vehiclesbyroutes query
		# separated from APIupdate, so APIupdate can be tested separately from the API call
		query = 'http://realtime.mbta.com/developer/api/v2/vehiclesbyroutes?api_key='+self.apikey+'&routes='+self.route+'&format='+self.dataformat

		resp = requests.get(query)
		if resp.status_code != 200:
			raise IllegalArgumentException('API error: {}'.format(resp.status_code))
		elif resp.json() == {}:
			raise IllegalArgumentException('empty file returned - maybe you made a bad query?')

		return resp.json()

	def APIupdate(self, resp):
		# takes resp, where resp is returned by APIget(), and updates self.__trains

		trains = {}

		for d in resp['mode'][0]['route'][0]['direction']:
			for v in d['trip']:
				vid = v['vehicle']['vehicle_id']
				lon = float(v['vehicle']['vehicle_lon'])
				lat = float(v['vehicle']['vehicle_lat'])
				bearing = float(v['vehicle']['vehicle_bearing'])
				timestamp = int(v['vehicle']['vehicle_timestamp'])

				trains[vid] = [lon, lat, bearing, timestamp]

		self.api_lock.acquire() #start conditional critical region
		self.__trains = trains
		self.api_lock.release() #end conditional critical region

	def run(self):
		
		t = 0

		while t < 100: # run for 100 seconds
			self.APIupdate(self.APIget())
			sleep(10)
			t += 10
