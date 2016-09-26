import unittest

from APIreader import *
from IllegalArgumentException import *

class TestAPIreader(unittest.TestCase):

	#test constructor does not throw error, and trains initialized as empty dictionary
	def testConstructor(self):
		r = APIreader()
		self.assertEqual({}, r.getTrains())

	#test that API is online - that APIget() and APIupdate() do not throw errors
	def testAPIget(self):
		r = APIreader()
		get = r.APIget()
		r.APIupdate(get)

		self.assertNotEqual({}, r.getTrains()) #check that trains is no longer empty

	#test that APIget throws an error if a bad query is made
	def testAPIgetBadQuery(self):
		r = APIreader()
		r.route = 'nosuchroute'
		
		with self.assertRaises(IllegalArgumentException):
			r.APIget()

	#test that APIget throws an error if a bad API key is used
	def testAPIgetBadAPIKey(self):
		r = APIreader()
		r.apikey = 'thisisabadkey'

		with self.assertRaises(IllegalArgumentException):
			r.APIget()

	#test that APIupdate() parses the given json file correctly
	def testAPIupdate(self):
		r = APIreader()
		# sample json returned by APIget()
		# train info is:
		# id 			lon 		lat 		bearing 	timestamp
		# 5445C7F5		-71.00684 	42.23014 	170 		1463147191
		# 5445C8E6 		-71.00551 	42.25203 	150 		1463147182
		# 5445CE93 		-71.05206 	42.31602 	170 		1463147125
		# 5445CE94 		-71.05712 	42.34256 	175 		1463147194
		# 5445CEB6 		-71.06498 	42.28869 	160 		1463147122
		# 5445C8F8 		-71.10831 	42.36804 	125 		1463147173
		# 5445C88A 		-71.05724 	42.34064 	175 		1463147169
		# 5445CB89 		-71.11895 	42.38826 	180 		1463147178
		# 5445CEDE 		-71.06265 	42.35648 	130 		1463147128
		# 5445CE4A 		-71.14054 	42.39618 	265 		1463147055 
		# 5445CEF3 		-71.1203 	42.3796 	185 		1463147180
		# 5445CE97 		-71.14054 	42.39621 	265 		1463146868
		# 5445C496 		-71.124 	42.39679 	285 		1463147182
		# 5445BC46 		-71.11936 	42.38416 	0 			1463147183
		# 5445CEF5 		-71.12732 	42.39762 	275 		1463147190
		# 5445C898 		-71.10626	42.36703 	310 		1463147126
		# 5445CE99 		-71.11586 	42.37246 	330 		1463147102
		# 5445C888 		-71.08088 	42.36203 	275 		1463147182
		# 5445CE9B 		-71.09416 	42.36316 	275 		1463147140
		# 5445CB88 		-71.05536 	42.35266 	290 		1463147097 
		# 5445CE9A 		-71.06548 	42.35792 	310 		1463147192
		# 5445B54E 		-71.0546 	42.30663 	10 			1463147155
		# 5445CE96 		-71.03228	42.27878 	345 		1463147186
		# 5445A600 		-71.05697 	42.33022 	0 			1463147121
		# 5445CF55 		-71.00386 	42.22515 	330 		1463147181
		# 5445CF46 		-71.06448 	42.28643 	330 		1463147178
		j = {
			  "mode": [
			    {
			      "route_type": "1",
			      "mode_name": "Subway",
			      "route": [
			        {
			          "route_id": "Red",
			          "route_name": "Red Line",
			          "direction": [
			            {
			              "direction_id": "0",
			              "direction_name": "Southbound",
			              "trip": [
			                {
			                  "trip_id": "30454164",
			                  "trip_name": "8:40 am from Alewife to Braintree",
			                  "trip_headsign": "Braintree",
			                  "vehicle": {
			                    "vehicle_id": "5445C7F5",
			                    "vehicle_lat": "42.23014",
			                    "vehicle_lon": "-71.00684",
			                    "vehicle_bearing": "170",
			                    "vehicle_timestamp": "1463147191"
			                  }
			                },
			                {
			                  "trip_id": "30453729",
			                  "trip_name": "8:43 am from Alewife to Braintree",
			                  "trip_headsign": "Braintree",
			                  "vehicle": {
			                    "vehicle_id": "5445C8E6",
			                    "vehicle_lat": "42.25203",
			                    "vehicle_lon": "-71.00551",
			                    "vehicle_bearing": "150",
			                    "vehicle_timestamp": "1463147182"
			                  }
			                },
			                {
			                  "trip_id": "30453730",
			                  "trip_name": "8:50 am from Alewife to Braintree",
			                  "trip_headsign": "Braintree",
			                  "vehicle": {
			                    "vehicle_id": "5445CE93",
			                    "vehicle_lat": "42.31602",
			                    "vehicle_lon": "-71.05206",
			                    "vehicle_bearing": "170",
			                    "vehicle_timestamp": "1463147125"
			                  }
			                },
			                {
			                  "trip_id": "30453731",
			                  "trip_name": "8:59 am from Alewife to Braintree",
			                  "trip_headsign": "Braintree",
			                  "vehicle": {
			                    "vehicle_id": "5445CE94",
			                    "vehicle_lat": "42.34256",
			                    "vehicle_lon": "-71.05712",
			                    "vehicle_bearing": "175",
			                    "vehicle_timestamp": "1463147194"
			                  }
			                },
			                {
			                  "trip_id": "30453631",
			                  "trip_name": "9:03 am from Alewife to Ashmont - Outbound",
			                  "trip_headsign": "Ashmont",
			                  "vehicle": {
			                    "vehicle_id": "5445CEB6",
			                    "vehicle_lat": "42.28869",
			                    "vehicle_lon": "-71.06498",
			                    "vehicle_bearing": "160",
			                    "vehicle_timestamp": "1463147122"
			                  }
			                },
			                {
			                  "trip_id": "30453732",
			                  "trip_name": "9:07 am from Alewife to Braintree",
			                  "trip_headsign": "Braintree",
			                  "vehicle": {
			                    "vehicle_id": "5445C8F8",
			                    "vehicle_lat": "42.36804",
			                    "vehicle_lon": "-71.10831",
			                    "vehicle_bearing": "125",
			                    "vehicle_timestamp": "1463147173"
			                  }
			                },
			                {
			                  "trip_id": "30453611",
			                  "trip_name": "9:12 am from Alewife to Ashmont - Outbound",
			                  "trip_headsign": "Ashmont",
			                  "vehicle": {
			                    "vehicle_id": "5445C88A",
			                    "vehicle_lat": "42.34064",
			                    "vehicle_lon": "-71.05724",
			                    "vehicle_bearing": "175",
			                    "vehicle_timestamp": "1463147169"
			                  }
			                },
			                {
			                  "trip_id": "30453733",
			                  "trip_name": "9:16 am from Alewife to Braintree",
			                  "trip_headsign": "Braintree",
			                  "vehicle": {
			                    "vehicle_id": "5445CB89",
			                    "vehicle_lat": "42.38826",
			                    "vehicle_lon": "-71.11895",
			                    "vehicle_bearing": "180",
			                    "vehicle_timestamp": "1463147178"
			                  }
			                },
			                {
			                  "trip_id": "30453612",
			                  "trip_name": "9:20 am from Alewife to Ashmont - Outbound",
			                  "trip_headsign": "Ashmont",
			                  "vehicle": {
			                    "vehicle_id": "5445CEDE",
			                    "vehicle_lat": "42.35648",
			                    "vehicle_lon": "-71.06265",
			                    "vehicle_bearing": "130",
			                    "vehicle_timestamp": "1463147128"
			                  }
			                },
			                {
			                  "trip_id": "30453734",
			                  "trip_name": "9:24 am from Alewife to Braintree",
			                  "trip_headsign": "Braintree",
			                  "vehicle": {
			                    "vehicle_id": "5445CE4A",
			                    "vehicle_lat": "42.39618",
			                    "vehicle_lon": "-71.14054",
			                    "vehicle_bearing": "265",
			                    "vehicle_timestamp": "1463147055"
			                  }
			                },
			                {
			                  "trip_id": "30453613",
			                  "trip_name": "9:29 am from Alewife to Ashmont - Outbound",
			                  "trip_headsign": "Ashmont",
			                  "vehicle": {
			                    "vehicle_id": "5445CEF3",
			                    "vehicle_lat": "42.3796",
			                    "vehicle_lon": "-71.1203",
			                    "vehicle_bearing": "185",
			                    "vehicle_timestamp": "1463147180"
			                  }
			                },
			                {
			                  "trip_id": "30453614",
			                  "trip_name": "9:37 am from Alewife to Ashmont - Outbound",
			                  "trip_headsign": "Ashmont",
			                  "vehicle": {
			                    "vehicle_id": "5445CE97",
			                    "vehicle_lat": "42.39621",
			                    "vehicle_lon": "-71.14054",
			                    "vehicle_bearing": "265",
			                    "vehicle_timestamp": "1463146868"
			                  }
			                }
			              ]
			            },
			            {
			              "direction_id": "1",
			              "direction_name": "Northbound",
			              "trip": [
			                {
			                  "trip_id": "30453788",
			                  "trip_name": "8:41 am from Braintree to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445C496",
			                    "vehicle_lat": "42.39679",
			                    "vehicle_lon": "-71.124",
			                    "vehicle_bearing": "285",
			                    "vehicle_timestamp": "1463147182"
			                  }
			                },
			                {
			                  "trip_id": "30453789",
			                  "trip_name": "8:50 am from Braintree to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445BC46",
			                    "vehicle_lat": "42.38416",
			                    "vehicle_lon": "-71.11936",
			                    "vehicle_bearing": "0",
			                    "vehicle_timestamp": "1463147183"
			                  }
			                },
			                {
			                  "trip_id": "30453606",
			                  "trip_name": "8:56 am from Ashmont - Inbound to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445CEF5",
			                    "vehicle_lat": "42.39762",
			                    "vehicle_lon": "-71.12732",
			                    "vehicle_bearing": "275",
			                    "vehicle_timestamp": "1463147190"
			                  }
			                },
			                {
			                  "trip_id": "30453790",
			                  "trip_name": "8:58 am from Braintree to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445C898",
			                    "vehicle_lat": "42.36703",
			                    "vehicle_lon": "-71.10626",
			                    "vehicle_bearing": "310",
			                    "vehicle_timestamp": "1463147126"
			                  }
			                },
			                {
			                  "trip_id": "30453607",
			                  "trip_name": "9:04 am from Ashmont - Inbound to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445CE99",
			                    "vehicle_lat": "42.37246",
			                    "vehicle_lon": "-71.11586",
			                    "vehicle_bearing": "330",
			                    "vehicle_timestamp": "1463147102"
			                  }
			                },
			                {
			                  "trip_id": "30453791",
			                  "trip_name": "9:07 am from Braintree to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445C888",
			                    "vehicle_lat": "42.36203",
			                    "vehicle_lon": "-71.08088",
			                    "vehicle_bearing": "275",
			                    "vehicle_timestamp": "1463147182"
			                  }
			                },
			                {
			                  "trip_id": "30453608",
			                  "trip_name": "9:13 am from Ashmont - Inbound to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445CE9B",
			                    "vehicle_lat": "42.36316",
			                    "vehicle_lon": "-71.09416",
			                    "vehicle_bearing": "275",
			                    "vehicle_timestamp": "1463147140"
			                  }
			                },
			                {
			                  "trip_id": "30453792",
			                  "trip_name": "9:16 am from Braintree to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445CB88",
			                    "vehicle_lat": "42.35266",
			                    "vehicle_lon": "-71.05536",
			                    "vehicle_bearing": "290",
			                    "vehicle_timestamp": "1463147097"
			                  }
			                },
			                {
			                  "trip_id": "30453609",
			                  "trip_name": "9:22 am from Ashmont - Inbound to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445CE9A",
			                    "vehicle_lat": "42.35792",
			                    "vehicle_lon": "-71.06548",
			                    "vehicle_bearing": "310",
			                    "vehicle_timestamp": "1463147192"
			                  }
			                },
			                {
			                  "trip_id": "30453870",
			                  "trip_name": "9:25 am from Braintree to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445B54E",
			                    "vehicle_lat": "42.30663",
			                    "vehicle_lon": "-71.0546",
			                    "vehicle_bearing": "10",
			                    "vehicle_timestamp": "1463147155"
			                  }
			                },
			                {
			                  "trip_id": "30453793",
			                  "trip_name": "9:30 am from Braintree to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445CE96",
			                    "vehicle_lat": "42.27878",
			                    "vehicle_lon": "-71.03228",
			                    "vehicle_bearing": "345",
			                    "vehicle_timestamp": "1463147186"
			                  }
			                },
			                {
			                  "trip_id": "30453610",
			                  "trip_name": "9:31 am from Ashmont - Inbound to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445A600",
			                    "vehicle_lat": "42.33022",
			                    "vehicle_lon": "-71.05697",
			                    "vehicle_bearing": "0",
			                    "vehicle_timestamp": "1463147121"
			                  }
			                },
			                {
			                  "trip_id": "30453794",
			                  "trip_name": "9:39 am from Braintree to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445CF55",
			                    "vehicle_lat": "42.22515",
			                    "vehicle_lon": "-71.00386",
			                    "vehicle_bearing": "330",
			                    "vehicle_timestamp": "1463147181"
			                  }
			                },
			                {
			                  "trip_id": "30453632",
			                  "trip_name": "9:44 am from Ashmont - Inbound to Alewife",
			                  "trip_headsign": "Alewife",
			                  "vehicle": {
			                    "vehicle_id": "5445CF46",
			                    "vehicle_lat": "42.28643",
			                    "vehicle_lon": "-71.06448",
			                    "vehicle_bearing": "330",
			                    "vehicle_timestamp": "1463147178"
			                  }
			                }
			              ]
			            }
			          ]
			        }
			      ]
			    }
			  ]
			}
		r.APIupdate(j)

		trains = r.getTrains()
		ids = ['5445C7F5',
				'5445C8E6',
				'5445CE93',
				'5445CE94',
				'5445CEB6',
				'5445C8F8',
				'5445C88A',
				'5445CB89',
				'5445CEDE',
				'5445CE4A',
				'5445CEF3',
				'5445CE97',
				'5445C496',
				'5445BC46',
				'5445CEF5',
				'5445C898',
				'5445CE99',
				'5445C888',
				'5445CE9B',
				'5445CB88',
				'5445CE9A',
				'5445B54E',
				'5445CE96',
				'5445A600',
				'5445CF55',
				'5445CF46']

		self.assertEqual(set(trains.keys()), set(ids))

		# check that entries are populated correctly 
		self.assertEqual([-71.00684, 42.23014,	170,	1463147191] , trains['5445C7F5'])
		self.assertEqual([-71.00551, 42.25203,	150,	1463147182] , trains['5445C8E6'])
		self.assertEqual([-71.05206, 42.31602,	170,	1463147125] , trains['5445CE93'])
		self.assertEqual([-71.05712, 42.34256,	175,	1463147194] , trains['5445CE94'])
		self.assertEqual([-71.06498, 42.28869,	160,	1463147122] , trains['5445CEB6'])
		self.assertEqual([-71.10831, 42.36804,	125,	1463147173] , trains['5445C8F8'])
		self.assertEqual([-71.05724, 42.34064,	175,	1463147169] , trains['5445C88A'])
		self.assertEqual([-71.11895, 42.38826,	180,	1463147178] , trains['5445CB89'])
		self.assertEqual([-71.06265, 42.35648,	130,	1463147128] , trains['5445CEDE'])
		self.assertEqual([-71.14054, 42.39618,	265,	1463147055] , trains['5445CE4A'])
		self.assertEqual([-71.1203 , 42.3796 ,	185,	1463147180] , trains['5445CEF3'])
		self.assertEqual([-71.14054, 42.39621,	265,	1463146868] , trains['5445CE97'])
		self.assertEqual([-71.124  , 42.39679,	285,	1463147182] , trains['5445C496'])
		self.assertEqual([-71.11936, 42.38416,	0  ,	1463147183] , trains['5445BC46'])
		self.assertEqual([-71.12732, 42.39762,	275,	1463147190] , trains['5445CEF5'])
		self.assertEqual([-71.10626, 42.36703,	310,	1463147126] , trains['5445C898'])
		self.assertEqual([-71.11586, 42.37246,	330,	1463147102] , trains['5445CE99'])
		self.assertEqual([-71.08088, 42.36203,	275,	1463147182] , trains['5445C888'])
		self.assertEqual([-71.09416, 42.36316,	275,	1463147140] , trains['5445CE9B'])
		self.assertEqual([-71.05536, 42.35266,	290,	1463147097] , trains['5445CB88'])
		self.assertEqual([-71.06548, 42.35792,	310,	1463147192] , trains['5445CE9A'])
		self.assertEqual([-71.0546 , 42.30663,	10 ,	1463147155] , trains['5445B54E'])
		self.assertEqual([-71.03228, 42.27878,	345,	1463147186] , trains['5445CE96'])
		self.assertEqual([-71.05697, 42.33022,	0  ,	1463147121] , trains['5445A600'])
		self.assertEqual([-71.00386, 42.22515,	330,	1463147181] , trains['5445CF55'])
		self.assertEqual([-71.06448, 42.28643,	330,	1463147178] , trains['5445CF46'])
		
		
if __name__ == '__main__':
	unittest.main()
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		