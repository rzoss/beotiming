import configparser
import datetime

config = configparser.ConfigParser()

class BeoConfig:
	
	# initialisierung
	def __init__(self):
		config.read('config.ini')
		config.sections()
		self.readConfig()
		
	def readConfig(self):
		# Default
		self.StartOrFinish = config['Default']['StartOrFinish']
		# WWAN (currently not used)
		
		# FTP
		self.FTPServer = config['FTP']['FTPServer']
		self.FTPUser = config['FTP']['FTPUsername']
		self.FTPPwd = config['FTP']['FTPPwd']
		
		# Route
		self.routeName = config['Route']['RouteName']
		self.route = [[config['Route']['RouteKey1'],config['Route']['RouteType1']],[config['Route']['RouteKey2'],config['Route']['RouteType2']],[config['Route']['RouteKey3'],config['Route']['RouteType3']]]
		self.timestamp = datetime.datetime.now()
		
	def updateConfig(self):
		self.readConfig()
		
	def isStart(self):
		if self.StartOrFinish == "0":
			return True
		else:
			return False
			
	def isFinish(self):
		if self.StartOrFinish == "1":
			return True
		else:
			return False
		
	def getFTPData(self):
		return (self.FTPServer, self.FTPUser, self.FTPPwd)
		
	def getRoute(self):
		return (self.route)
		
	def getRouteName(self):
		return (self.routeName)
		
		
		
