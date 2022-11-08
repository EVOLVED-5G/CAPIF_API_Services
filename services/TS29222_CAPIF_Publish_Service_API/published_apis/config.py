import yaml
import os

#Config class to get config
class Config:
	def __init__(self):
		self.cached = 0
		self.file="./config.yaml"
		self.my_config = {}

		stamp = os.stat(self.file).st_mtime
		if stamp != self.cached:
			self.cached = stamp
			f = open(self.file)
			self.my_config = yaml.safe_load(f)
			f.close()

	def getConfig(self):
		return self.my_config

	def chargeMQTTConfig(self, app):

		app.app.config['MQTT_BROKER_URL'] = self.my_config["mqtt"]["url"]  # use the free broker from HIVEMQ
		app.app.config['MQTT_BROKER_PORT'] =  self.my_config["mqtt"]["port"]  # default port for non-tls connection
		app.app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
		app.app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
		app.app.config['MQTT_KEEPALIVE'] =  self.my_config["mqtt"]["keepalive"]  # set the time interval for sending a ping to the broker to 5 seconds
		app.app.config['MQTT_TLS_ENABLED'] =  self.my_config["mqtt"]["tls"]  # set TLS to disabled for testing purposes

