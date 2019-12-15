# --- Anh Tran --- #
# This file gives a basic GUI to help user to test out commands, plotting the position of the agents in real time.
 
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph.opengl as gl
import numpy as np

import time
from threading import Timer

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cf_drone_interface import cf_control

class PlotWindow(QDialog):
	"""docstring for PlotWindow"""
	def __init__(self, *args, **kwargs):
		super(PlotWindow, self).__init__(*args, **kwargs)

		uic.loadUi('plotter.ui', self)

		self.gl_widget.setWindowTitle('Multi-agent Plotter')
		self.addAxis()
		self.gl_widget.addItem(gl.GLGridItem()) # Add the grid to the plot

		# Initialise mesh item to represent an agent
		md = gl.MeshData.sphere(rows=5, cols=5, radius=0.25)
		self.agent_mesh = gl.GLMeshItem(meshdata=md, smooth=False, drawFaces=False, drawEdges=True, edgeColor=(1,1,1,1))

		self.gl_widget.addItem(self.agent_mesh)

		self.startplotButton.clicked.connect(self.update_plot)

		self.prev_x = 0
		self.prev_y = 0
		self.prev_z = 0


	def show_plotter(self):
		self.show()
		self.gl_widget.show()

	def addAxis(self):
		x_axis = gl.GLLinePlotItem()
		y_axis = gl.GLLinePlotItem()
		z_axis = gl.GLLinePlotItem()

		x_line = np.array([[0,0,0],[10,0,0]])
		y_line = np.array([[0,0,0],[0,10,0]])
		z_line = np.array([[0,0,0],[0,0,10]])

		x_color = np.array([255,0,0,0.75])
		y_color = np.array([0,255,0,0.75])
		z_color = np.array([0,0,255,0.75])

		width = 2
		mode = 'lines'

		x_axis.setData(pos=x_line, color=x_color, width=width, antialias=True, mode=mode)
		y_axis.setData(pos=y_line, color=y_color, width=width, antialias=True, mode=mode)
		z_axis.setData(pos=z_line, color=z_color, width=width, antialias=True, mode=mode)

		self.gl_widget.addItem(x_axis)
		self.gl_widget.addItem(y_axis)
		self.gl_widget.addItem(z_axis)

	def add_agent(self, crazyflie):
		self.cf = crazyflie

	def update_plot(self):
		dx = (self.cf.x - self.prev_x)*3
		dy = (self.cf.y - self.prev_y)*3
		dz = (self.cf.z - self.prev_z)*3

		self.prev_x = self.cf.x
		self.prev_y = self.cf.y
		self.prev_z = self.cf.z

		self.agent_mesh.translate(dx,dy,dz)
		# self.agent_mesh.translate(1,1,1,local=True)
		print(f"\n[dx, dy, dz]: [{dx},{dy},{dz}]")

		Timer(0.1,self.update_plot).start()

class CommWindow(QMainWindow):
	"""docstring for MainWindow"""
	def __init__(self, *args, **kwargs):
		super(CommWindow, self).__init__(*args, **kwargs)
		
		self.setWindowTitle("Multiagent Communication")
		uic.loadUi('crazyflie_multiagent.ui', self)

		self.PlotWindow = PlotWindow()

		self.cfs = []
		self.selected_cf = None
		
		self.btn_exit.clicked.connect(self.btn_exit_clicked)
		self.btn_scan.clicked.connect(self.btn_scan_clicked)
		self.btn_connectall.clicked.connect(self.btn_connect_all_clicked)
		self.btn_snd_cmd.clicked.connect(self.btn_snd_cmd_clicked)
		self.btn_snd_pos_cmd.clicked.connect(self.btn_snd_pos_cmd_clicked)
		self.action3D_visualiser.triggered.connect(self.open_visualiser)

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
			self.PlotWindow.add_agent(self.selected_cf)

	def comboDrones_index_changed(self):
		self.selected_cf = cfs[self.combobox_drone.currentIndex()]
		self.PlotWindow.add_agent(self.selected_cf)

	def btn_snd_pos_cmd_clicked(self):
		x = float(self.edit_x.text())
		y = float(self.edit_y.text())
		z = float(self.edit_z.text())
		yaw = float(self.edit_yaw.text())

		self.selected_cf.set_position_command_param(x, y, z, yaw)
		self.selected_cf.send_position_command()

	def btn_snd_cmd_clicked(self):
		roll = int(self.edit_roll.text())
		pitch = int(self.edit_pitch.text())
		yawrate = int(self.edit_yawrate.text())
		thrust = int(self.edit_thrust.text())

		self.selected_cf.new_command = 1
		self.selected_cf.set_control_command_param(roll, pitch, yawrate, thrust)
		self.selected_cf.send_control_command()

	def open_visualiser(self):
		# self.PlotWindow.show()
		self.PlotWindow.show_plotter()

if __name__ == "__main__":
	# Initialize the low-level drivers
	cflib.crtp.init_drivers(enable_debug_driver=False)

	app = QApplication(sys.argv)

	window = CommWindow()

	window.show()	
	app.exec_()

