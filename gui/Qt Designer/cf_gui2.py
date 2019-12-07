# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crazyflie_multiagent.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

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

class Ui_MainWindow(object):
	def initDrones(self):
		self.cfs = []

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(508, 315)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("../media/uoa_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		MainWindow.setWindowIcon(icon)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.btn_scan = QtWidgets.QPushButton(self.centralwidget)
		self.btn_scan.setGeometry(QtCore.QRect(9, 30, 91, 25))
		self.btn_scan.setObjectName("btn_scan")
		self.combobox_drone = QtWidgets.QComboBox(self.centralwidget)
		self.combobox_drone.setGeometry(QtCore.QRect(110, 30, 151, 25))
		self.combobox_drone.setObjectName("combobox_drone")
		self.btn_snd_cmd = QtWidgets.QPushButton(self.centralwidget)
		self.btn_snd_cmd.setGeometry(QtCore.QRect(360, 190, 112, 25))
		self.btn_snd_cmd.setObjectName("btn_snd_cmd")
		self.label_roll = QtWidgets.QLabel(self.centralwidget)
		self.label_roll.setGeometry(QtCore.QRect(300, 30, 67, 17))
		self.label_roll.setObjectName("label_roll")
		self.label_pitch = QtWidgets.QLabel(self.centralwidget)
		self.label_pitch.setGeometry(QtCore.QRect(300, 70, 67, 17))
		self.label_pitch.setObjectName("label_pitch")
		self.label_yawrate = QtWidgets.QLabel(self.centralwidget)
		self.label_yawrate.setGeometry(QtCore.QRect(300, 110, 67, 17))
		self.label_yawrate.setObjectName("label_yawrate")
		self.label_thrust = QtWidgets.QLabel(self.centralwidget)
		self.label_thrust.setGeometry(QtCore.QRect(300, 150, 67, 17))
		self.label_thrust.setObjectName("label_thrust")
		self.btn_exit = QtWidgets.QPushButton(self.centralwidget)
		self.btn_exit.setGeometry(QtCore.QRect(10, 260, 89, 25))
		self.btn_exit.setAutoFillBackground(False)
		self.btn_exit.setObjectName("btn_exit")
		self.input_roll = QtWidgets.QTextEdit(self.centralwidget)
		self.input_roll.setGeometry(QtCore.QRect(370, 20, 104, 31))
		self.input_roll.setObjectName("input_roll")
		self.input_pitch = QtWidgets.QTextEdit(self.centralwidget)
		self.input_pitch.setGeometry(QtCore.QRect(370, 60, 104, 31))
		self.input_pitch.setObjectName("input_pitch")
		self.input_yawrate = QtWidgets.QTextEdit(self.centralwidget)
		self.input_yawrate.setGeometry(QtCore.QRect(370, 100, 104, 31))
		self.input_yawrate.setObjectName("input_yawrate")
		self.input_thrust = QtWidgets.QTextEdit(self.centralwidget)
		self.input_thrust.setGeometry(QtCore.QRect(370, 140, 104, 31))
		self.input_thrust.setObjectName("input_thrust")
		self.btn_connectall = QtWidgets.QPushButton(self.centralwidget)
		self.btn_connectall.setGeometry(QtCore.QRect(10, 70, 91, 51))
		self.btn_connectall.setObjectName("btn_connectall")
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		self.btn_exit.clicked.connect(self.btn_exit_clicked)
		self.btn_scan.clicked.connect(self.btn_scan_clicked)
		self.btn_connectall.clicked.connect(self.btn_connect_all)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Crazyflie Multiagent"))
		self.btn_scan.setText(_translate("MainWindow", "Scan"))
		self.btn_snd_cmd.setText(_translate("MainWindow", "Send command"))
		self.label_roll.setText(_translate("MainWindow", "Roll"))
		self.label_pitch.setText(_translate("MainWindow", "Pitch"))
		self.label_yawrate.setText(_translate("MainWindow", "Yaw rate"))
		self.label_thrust.setText(_translate("MainWindow", "Thrust"))
		self.btn_exit.setText(_translate("MainWindow", "EXIT"))
		self.btn_connectall.setText(_translate("MainWindow", "Connect all"))

	def btn_exit_clicked(self):
		print("Program closed.")
		for i in range(len(self.cfs)):
			self.cfs[i]._cf.close_link()
		sys.exit()

	def btn_scan_clicked(self):
		# Scan for Crazyflies and use the first one found
		print('Scanning interfaces for Crazyflies...')
		available = cflib.crtp.scan_interfaces()

		if len(available) > 0:
			self.radio_items = [item[0] for item in available]
			self.combobox_drone.clear()
			self.combobox_drone.addItems(self.radio_items)
			print('Crazyflies found:')
			for i in available:
				print(i[0])

		else:
			print('No Crazyflies found :(')

	def btn_connect_all(self):
		for i in range(len(self.radio_items)):
			cf = cf_control(self.radio_items[i])
			self.cfs.append(cf)
			while(cf.is_connected == False):
				continue
			cf = None

	# def btn_send_cmd(self):



if __name__ == "__main__":
	# Initialize the low-level drivers
	cflib.crtp.init_drivers(enable_debug_driver=False)

	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	ui.initDrones()
	MainWindow.show()
	sys.exit(app.exec_())
