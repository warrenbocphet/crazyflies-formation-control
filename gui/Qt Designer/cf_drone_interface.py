import time
from threading import Timer

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig

class cf_control():
	"""docstring for cf_control"""
	def __init__(self, uri):
		self._cf = Crazyflie(rw_cache='./cache')

		# Define callback function variable
		self._cf.connected.add_callback(self._connected)
		self._cf.disconnected.add_callback(self._disconnected)
		self._cf.connection_failed.add_callback(self._connection_failed)
		self._cf.connection_lost.add_callback(self._connection_lost)

		self.is_connected = False
		self.new_command = 0
		print('Connecting to %s' % uri)
		self._cf.open_link(uri)
		
		self.roll_cmd = 0
		self.pitch_cmd = 0
		self.yaw_cmd = 0
		self.thrust_cmd = 0

		self.x_cmd = 0
		self.y_cmd = 0
		self.z_cmd = 0

		self.x = 0
		self.y = 0
		self.z = 0

	def _connected(self, uri):
		print(f"Connected to {uri}")
		self.is_connected = True

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

	# Connection callback
	def _connection_failed(self, uri, msg):
		print(f"Connection to {uri} failed: {msg}.")

	def _connection_lost(self, uri, msg):
		print(f"Connection to {uri} lost: {msg}.")

	def _disconnected(self, uri):
		print(f"Disconnect from {uri}.")
		self.is_connected = False

	def set_control_command_param(self, roll, pitch, yaw, thrust):
		self.roll_cmd = roll
		self.pitch_cmd = pitch
		self.yaw_cmd = yaw
		self.thrust_cmd = thrust # thrust should be between 10001 -> 60000

	def send_control_command(self):
		if (self.new_command == 1):
			self._cf.commander.send_setpoint(0, 0, 0, 0)
			self.new_command = 0
			
		self._cf.commander.send_setpoint(self.roll_cmd, self.pitch_cmd, self.yaw_cmd, self.thrust_cmd)
		Timer(0.1,self.send_control_command).start()

	def set_position_command_param(self, x, y, z, yaw):
		self.x_cmd = x
		self.y_cmd = y
		self.z_cmd = z
		self.yaw_cmd = yaw

	def send_position_command(self):

		self._cf.commander.send_position_setpoint(self.x_cmd, self.y_cmd, self.z_cmd, self.yaw_cmd)
		Timer(0.1,self.send_control_command).start()

	def close_link(self):
		self._cf.close_link()

	def _ramp_motors(self):
		thrust_mult = 1
		thrust_step = 500
		thrust = 20000
		pitch = 0
		roll = 0
		yawrate = 0

		# Unlock startup thrust protection
		self._cf.commander.send_setpoint(0, 0, 0, 0)

		while thrust >= 20000:
			self._cf.commander.send_setpoint(roll, pitch, yawrate, thrust)
			time.sleep(0.1)
			if thrust >= 25000:
				thrust_mult = -1
			thrust += thrust_step * thrust_mult
		self._cf.commander.send_setpoint(0, 0, 0, 0)
		# Make sure that the last packet leaves before the link is closed
		# since the message queue is not flushed before closing
		time.sleep(0.1)
		self._cf.close_link()

	# Logging data connect
	def error_callback(self, logconf, msg):
		print(f"Error when logging {logconf.name}: {msg}")

	def dataReceived_callback(self, timestamp, data, logconf):
		self.x = data["stateEstimate.x"]
		self.y = data["stateEstimate.y"]
		self.z = data["stateEstimate.z"]