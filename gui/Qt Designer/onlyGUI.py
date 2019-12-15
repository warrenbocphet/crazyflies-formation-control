# --- Anh Tran --- #
# This file gives a basic GUI to help user to test out commands, plotting the position of the agents in real time.
 
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph.opengl as gl

class MainWindow(QMainWindow):
	"""docstring for MainWindow"""
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		
		self.setWindowTitle("Multiagent Communication")
		uic.loadUi('crazyflie_multiagent.ui', self)

		self.gl_widget = gl.GLViewWidget()
		self.gl_widget.setWindowTitle('Multi-agent Plotter')

		self.gl_widget.addItem(gl.GLGridItem()) # Add the grid to the plot

		self.addAxis()

		# Initialise mesh item to represent an agent
		md = gl.MeshData.sphere(rows=5, cols=5, radius=0.25)
		self.agent_mesh = gl.GLMeshItem(meshdata=md, smooth=False, drawFaces=False, drawEdges=True, edgeColor=(1,1,1,1))

		self.gl_widget.addItem(self.agent_mesh)

		self.btn_exit.clicked.connect(self.btn_exit_clicked)
		self.action3D_visualiser.triggered.connect(self.open_visualiser)

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

	def btn_exit_clicked(self):
		print("Program closed.")
		sys.exit()

	def open_visualiser(self):
		print("Clicked!")
		self.gl_widget.show()

if __name__ == "__main__":
	# Initialize the low-level drivers
	app = QApplication(sys.argv)

	window = MainWindow()

	window.show()	
	app.exec_()
