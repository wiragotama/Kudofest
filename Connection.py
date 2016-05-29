import json
from pprint import pprint
import pymongo
import socket
import time
import sys
import _thread
from _thread import *
import clientHandler
from clientHandler import *
import peerHandler
from peerHandler import *

class Server:
	TCP_IP_TRACKER = '167.205.32.46'
	TCP_PORT_TRACKER = 8000
	BUFFER_SIZE = 4096
	HOST = 'localhost'
	PORT = 5005		# non-previledged port
	client = pymongo.MongoClient('localhost', 27017)
	db = client.grandquest
	# worldMap = {}
	threads = []

	def __init__(self):
		Server.initDB()
		Server.joinTracker(self) #connect to sister server
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print ("Socket created")

		#bind socket to local host and port
		try:
			self.sock.bind((Server.HOST, Server.PORT))
		except socket.error as msg:
			print("Bind Failed")
			sys.exit()
		print("Socket bind compete")
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
		self.sock.listen(1)
		print("Socket now listening")

	def initDB():
		Server.db.users.remove({}) #asumsikan username unik, berisi juga inventory yang dimiliki masing2 user
		Server.db.servers.remove({})
		Server.db.onlineUsers.remove({})
		Server.db.marketplace.remove({})
		Server.db.inventoryMaster.remove({})
		Server.db.inventoryMaster.insert({"id": 0, "alias": "R11", "name": "honey", "count": 0})
		Server.db.inventoryMaster.insert({"id": 1, "alias": "R12", "name": "herbs", "count": 0})
		Server.db.inventoryMaster.insert({"id": 2, "alias": "R13", "name": "clay", "count": 0})
		Server.db.inventoryMaster.insert({"id": 3, "alias": "R14", "name": "mineral", "count": 0})
		Server.db.inventoryMaster.insert({"id": 4, "alias": "R21", "name": "potion", "count": 0})
		Server.db.inventoryMaster.insert({"id": 5, "alias": "R22", "name": "incense", "count": 0})
		Server.db.inventoryMaster.insert({"id": 6, "alias": "R23", "name": "gems", "count": 0})
		Server.db.inventoryMaster.insert({"id": 7, "alias": "R31", "name": "elixir", "count": 0})
		Server.db.inventoryMaster.insert({"id": 8, "alias": "R32", "name": "crystal", "count": 0})
		Server.db.inventoryMaster.insert({"id": 9, "alias": "R41", "name": "stone", "count": 0})
		#db untuk mixitem combination
		Server.db.mixitem.remove({})
		Server.db.mixitem.insert({"item1": 0, "item2": 1, "itemresult": 4})
		Server.db.mixitem.insert({"item1": 1, "item2": 2, "itemresult": 5})
		Server.db.mixitem.insert({"item1": 2, "item2": 3, "itemresult": 6})
		Server.db.mixitem.insert({"item1": 4, "item2": 5, "itemresult": 7})
		Server.db.mixitem.insert({"item1": 5, "item2": 6, "itemresult": 8})
		Server.db.mixitem.insert({"item1": 7, "item2": 8, "itemresult": 9})
		#db untuk offering
		#with open('map.json') as data_file:
		#    data = json.load(data_file)
		#pprint(data) #debug
		#Server.worldMap = data

	def joinTracker(self):
		message = '{\"method\": \"join\", \"ip\": \"'+ str(Server.TCP_IP_TRACKER) +'\", \"port\":' + str(Server.TCP_PORT_TRACKER) +'}'
		print(message)
		self.sockTracker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sockTracker.connect((Server.TCP_IP_TRACKER, Server.TCP_PORT_TRACKER))
		self.sockTracker.sendall(message.encode('UTF-8'))
		data = self.sockTracker.recv(Server.BUFFER_SIZE)

		if data.decode('UTF-8'):
			request = json.loads(data.decode('UTF-8'))
			print(request)
			if request['status'] == 'ok':
				Server.db.servers.remove({})
				for i, val in enumerate(request['value']):
					Server.db.servers.insert(val)
			elif request['status'] =='error':
				print(request['description'])

	def acceptClientConnection(self):
		conn, addr = self.sock.accept()
		print('Connected with:', addr[0] + ':' + str(addr[1]))

		token = "0"
		clientHandler = ClientHandler(Server.HOST, Server.db, token)
		thread = start_new_thread(clientHandler.clientThread, (conn, addr, ))

	def closeSocket():
		self.sock.close()
		self.sockTracker.close()
		#for thread in Server.threads:
		#	thread.join()

srv = Server()

while True:
	srv.acceptClientConnection()
srv.closeSocket()
