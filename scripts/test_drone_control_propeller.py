import time
from threading import Timer

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig

"""
- Anh Tran -
This script try to control the propeller of the crazyflie.

"""

class cf_control():
	"""docstring for cf_control"""
	def __init__(self, uri):
		self._cf = Crazyflie(rw_cache='./cache')

		# Define callback function variable
		self._cf.connected.add_callback(self._connected)
		self._cf.disconnected.add_callback(self._disconnected)
		self._cf.connection_failed.add_callback(self._connection_failed)
		self._cf.connection_lost.add_callback(self._connection_lost)

		print('Connecting to %s' % link_uri)
		self._cf.open_link(link_uri)

		self.is_connected = True
		
		self.roll = 0
		self.pitch = 0
		self.yaw = 0
		self.thrust = 0

	def _connected(self, uri):
		print(f"Connected to {uri}")

	# Connection callback
	def _connection_failed(self, uri, msg):
		print(f"Connection to {uri} failed: {msg}.")

	def _connection_lost(self, uri, msg):
		print(f"Connection to {uri} lost: {msg}.")

	def _disconnected(self, uri):
		print(f"Disconnect from {uri}.")
		self.is_connected = False

	def set_control_command_param(self, roll, pitch, yaw, thrust):
		self.roll = roll
		self.pitch = pitch
		self.yaw = yaw
		self.thrust = thrust # thrust should be between 10001 -> 60000

	def send_control_command(self):
		self._cf.commander.send_setpoint(self.roll, self.pitch, self.yaw, self.thrust)
		Timer(0.01,self.send_control_command).start()

	def close_link(self):
		self._cf.close_link()

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
		cf = Crazyflie(rw_cache='./cache')

		while (cf.is_connected):
			try:
				print("\nType in the command")
				roll = float(input("Roll: "))
				pitch = float(input("Pitch: "))
				yaw = float(input("Yaw: "))
				thrust = float(input("Thrust (10001 -> 60000): "))

				cf.set_control_command_param(roll, pitch, yaw, thrust)
				cf.send_control_command()
				
			except KeyboardInterrupt:
				cf.close_link()

	else:
		print('No Crazyflies found, cannot run example')

if __name__ == '__main__':
	main()