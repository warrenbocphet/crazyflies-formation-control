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
		self.selected_cf = None

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(488, 393)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("../media/uoa_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		MainWindow.setWindowIcon(icon)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName("gridLayout")
		self.btn_scan = QtWidgets.QPushButton(self.centralwidget)
		self.btn_scan.setObjectName("btn_scan")
		self.gridLayout.addWidget(self.btn_scan, 0, 0, 1, 1)
		self.combobox_drone = QtWidgets.QComboBox(self.centralwidget)
		self.combobox_drone.setObjectName("combobox_drone")
		self.gridLayout.addWidget(self.combobox_drone, 0, 1, 1, 1)
		spacerItem = QtWidgets.QSpacerItem(3, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem, 0, 2, 1, 2)
		spacerItem1 = QtWidgets.QSpacerItem(97, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem1, 0, 4, 1, 2)
		self.label_roll = QtWidgets.QLabel(self.centralwidget)
		self.label_roll.setObjectName("label_roll")
		self.gridLayout.addWidget(self.label_roll, 0, 6, 1, 1)
		self.edit_roll = QtWidgets.QLineEdit(self.centralwidget)
		self.edit_roll.setObjectName("edit_roll")
		self.gridLayout.addWidget(self.edit_roll, 0, 7, 1, 1)
		self.btn_connectall = QtWidgets.QPushButton(self.centralwidget)
		self.btn_connectall.setObjectName("btn_connectall")
		self.gridLayout.addWidget(self.btn_connectall, 1, 0, 1, 1)
		spacerItem2 = QtWidgets.QSpacerItem(89, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem2, 1, 1, 1, 2)
		spacerItem3 = QtWidgets.QSpacerItem(97, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem3, 1, 3, 1, 2)
		self.label_pitch = QtWidgets.QLabel(self.centralwidget)
		self.label_pitch.setObjectName("label_pitch")
		self.gridLayout.addWidget(self.label_pitch, 1, 6, 1, 1)
		self.edit_pitch = QtWidgets.QLineEdit(self.centralwidget)
		self.edit_pitch.setObjectName("edit_pitch")
		self.gridLayout.addWidget(self.edit_pitch, 1, 7, 1, 1)
		spacerItem4 = QtWidgets.QSpacerItem(81, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem4, 2, 0, 1, 1)
		spacerItem5 = QtWidgets.QSpacerItem(89, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem5, 2, 1, 1, 2)
		spacerItem6 = QtWidgets.QSpacerItem(91, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem6, 2, 4, 1, 1)
		self.label_yawrate = QtWidgets.QLabel(self.centralwidget)
		self.label_yawrate.setObjectName("label_yawrate")
		self.gridLayout.addWidget(self.label_yawrate, 2, 6, 1, 1)
		self.edit_yawrate = QtWidgets.QLineEdit(self.centralwidget)
		self.edit_yawrate.setObjectName("edit_yawrate")
		self.gridLayout.addWidget(self.edit_yawrate, 2, 7, 1, 1)
		spacerItem7 = QtWidgets.QSpacerItem(81, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem7, 3, 0, 1, 1)
		spacerItem8 = QtWidgets.QSpacerItem(89, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem8, 3, 1, 1, 2)
		spacerItem9 = QtWidgets.QSpacerItem(91, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem9, 3, 4, 1, 1)
		self.label_thrust = QtWidgets.QLabel(self.centralwidget)
		self.label_thrust.setObjectName("label_thrust")
		self.gridLayout.addWidget(self.label_thrust, 3, 6, 1, 1)
		self.edit_thrust = QtWidgets.QLineEdit(self.centralwidget)
		self.edit_thrust.setObjectName("edit_thrust")
		self.gridLayout.addWidget(self.edit_thrust, 3, 7, 1, 1)
		spacerItem10 = QtWidgets.QSpacerItem(179, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem10, 4, 0, 1, 3)
		spacerItem11 = QtWidgets.QSpacerItem(91, 22, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem11, 4, 4, 1, 1)
		self.btn_snd_cmd = QtWidgets.QPushButton(self.centralwidget)
		self.btn_snd_cmd.setObjectName("btn_snd_cmd")
		self.gridLayout.addWidget(self.btn_snd_cmd, 4, 5, 1, 3)
		self.btn_exit = QtWidgets.QPushButton(self.centralwidget)
		self.btn_exit.setAutoFillBackground(False)
		self.btn_exit.setObjectName("btn_exit")
		self.gridLayout.addWidget(self.btn_exit, 5, 0, 1, 1)
		spacerItem12 = QtWidgets.QSpacerItem(89, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem12, 5, 1, 1, 2)
		spacerItem13 = QtWidgets.QSpacerItem(273, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem13, 5, 4, 1, 4)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menuBar = QtWidgets.QMenuBar(MainWindow)
		self.menuBar.setGeometry(QtCore.QRect(0, 0, 488, 22))
		self.menuBar.setObjectName("menuBar")
		MainWindow.setMenuBar(self.menuBar)

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

		self.btn_exit.clicked.connect(self.btn_exit_clicked)
		self.btn_scan.clicked.connect(self.btn_scan_clicked)
		self.btn_connectall.clicked.connect(self.btn_connect_all_clicked)
		self.btn_snd_cmd.clicked.connect(self.btn_snd_cmd_clicked)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Crazyflie Multiagent"))
		self.btn_scan.setText(_translate("MainWindow", "Scan"))
		self.label_roll.setText(_translate("MainWindow", "Roll"))
		self.btn_connectall.setText(_translate("MainWindow", "Connect all"))
		self.label_pitch.setText(_translate("MainWindow", "Pitch"))
		self.label_yawrate.setText(_translate("MainWindow", "Yaw rate"))
		self.label_thrust.setText(_translate("MainWindow", "Thrust"))
		self.btn_snd_cmd.setText(_translate("MainWindow", "Send command"))
		self.btn_exit.setText(_translate("MainWindow", "EXIT"))

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

	def btn_connect_all_clicked(self):
		for i in range(len(self.radio_items)):
			cf = cf_control(self.radio_items[i])
			self.cfs.append(cf)
			while(cf.is_connected == False):
				continue
			cf = None

		if (len(self.cfs) > 0):
			self.selected_cf = self.cfs[0]

	def comboDrones_index_changed(self):
		self.selected_cf = cfs[self.combobox_drone.currentIndex()]

	def btn_snd_cmd_clicked(self):
		roll = int(self.edit_roll.text())
		pitch = int(self.edit_pitch.text())
		yawrate = int(self.edit_yawrate.text())
		thrust = int(self.edit_thrust.text())

		self.selected_cf.new_command = 1
		self.selected_cf.set_control_command_param(roll, pitch, yawrate, thrust)
		self.selected_cf.send_control_command()

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
