import logging
import time
from threading import Timer

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig

"""
-Anh Tran-

This test is used to test the link between host computer and the crazyflies.
The script initialises the link and then "logging" the (x,y,z) and (vx,vy,vz)
on the screen.

"""

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

class cf_logging:

	def __init__(self, uri):
		self._cf = Crazyflie(rw_cache='./cache')

		# Define callback function variable
		self._cf.connected.add_callback(self._connected)
		self._cf.disconnected.add_callback(self._disconnected)
		self._cf.connection_failed.add_callback(self._connection_failed)
		self._cf.connection_lost.add_callback(self._connection_lost)

		print('Connecting to %s' % uri)
		self._cf.open_link(uri)

		self.is_connected = True

	def _connected(self, uri):
		print(f"Connected to {uri}")

		self._lg_stateEstimate = LogConfig(name="StateEstimation", period_in_ms=10)
		self._lg_stateEstimate.add_variable('stateEstimate.x', 'float')
		self._lg_stateEstimate.add_variable('stateEstimate.y', 'float')
		self._lg_stateEstimate.add_variable('stateEstimate.z', 'float')
		self._lg_stateEstimate.add_variable('stateEstimate.vx', 'float')
		self._lg_stateEstimate.add_variable('stateEstimate.vy', 'float')
		self._lg_stateEstimate.add_variable('stateEstimate.vz', 'float')

		try:
			self._cf.log.add_config(self._lg_stateEstimate)
			self._lg_stateEstimate.data_received_cb.add_callback(self.dataReceived_callback)
			self._lg_stateEstimate.error_cb.add_callback(self.error_callback)

			self._lg_stateEstimate.start()

		except KeyError as e:
			print(f"Could not start log config, {e} not found in TOC")

		except AttributeError:
			print('Could not add Stabilizer log config, bad configuration.')

		# Start a timer to disconnect in 5 seconds
		# Timer(5, self._cf.close_link).start()

	# Connection callback
	def _connection_failed(self, uri, msg):
		print(f"Connection to {uri} failed: {msg}.")

	def _connection_lost(self, uri, msg):
		print(f"Connection to {uri} lost: {msg}.")

	def _disconnected(self, uri):
		print(f"Disconnect from {uri}.")
		self.is_connected = False

	# Logging data connect
	def error_callback(self, logconf, msg):
		print(f"Error when logging {logconf.name}: {msg}")

	def dataReceived_callback(self, timestamp, data, logconf):
		x = data["stateEstimate.x"]
		y = data["stateEstimate.y"]
		z = data["stateEstimate.z"]
		print(f"\n\nX: {x}")
		print(f"\nY: {y}")
		print(f"\nZ: {z}")


def main():
	# Initialize the low-level drivers
	cflib.crtp.init_drivers(enable_debug_driver=False)

	# Scan for Crazyflies and use the first one found
	print('Scanning interfaces for Crazyflies...')
	available = cflib.crtp.scan_interfaces()

	print('Crazyflies found:')
	for i in available:
		print(i[0])

	if len(available) > 0:
		crazyflie_logger = cf_logging(available[0][0])

		while crazyflie_logger.is_connected:
			time.sleep(1)
	else:
		print('No Crazyflies found, cannot run example')

if __name__ == '__main__':
	main()