import sys
import os
import pyqtgraph as pg
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

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
		
		self.roll = 0
		self.pitch = 0
		self.yaw = 0
		self.thrust = 0

	def _connected(self, uri):
		print(f"Connected to {uri}")
		# self._cf.commander.send_setpoint(0, 0, 0, 0) # Unlock startup thrust protection
		self.is_connected = True

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
		if (self.new_command == 1):
			self._cf.commander.send_setpoint(0, 0, 0, 0)
			self.new_command = 0
			
		self._cf.commander.send_setpoint(self.roll, self.pitch, self.yaw, self.thrust)
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

class Window(QWidget):
	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50, 50, 500, 300)
		self.setWindowTitle("Crazyflie Multi Agent")
		scriptDir = os.path.dirname(os.path.realpath(__file__))
		self.setWindowIcon(QIcon(scriptDir + '/media/uoa_logo.png'))
		self.home()		

	def home(self):
		btn_quit = QtGui.QPushButton("Quit", self)

		btn_quit.clicked.connect(self.btn_quit_clicked)

		btn_quit.resize(btn_quit.sizeHint())
		btn_quit.move(100,100)

		self.show()

	def btn_quit_clicked(self):
		print("Program closed.")
		sys.exit()

def main():
	app = QApplication(sys.argv)

	GUI = Window()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()