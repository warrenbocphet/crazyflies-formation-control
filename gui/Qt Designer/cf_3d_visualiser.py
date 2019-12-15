import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph.opengl as gl
import numpy as np

import time
from threading import Timer

import logging
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig

# logging.basicConfig(level=logging.ERROR)

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

        self.x = 0
        self.y = 0
        self.z = 0

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
        self.x = data["stateEstimate.x"]
        self.y = data["stateEstimate.y"]
        self.z = data["stateEstimate.z"]

class Plotter():
    def setupPlotter(self):
        # print("Setting up plotter")
        self.gl_widget = gl.GLViewWidget()
        self.gl_widget.setWindowTitle('Multi-agent Plotter')

        self.gl_widget.addItem(gl.GLGridItem()) # Add the grid to the plot

        self.addAxis()

        # Initialise mesh item to represent an agent
        md = gl.MeshData.sphere(rows=5, cols=5, radius=0.25)
        self.agent_mesh = gl.GLMeshItem(meshdata=md, smooth=False, drawFaces=False, drawEdges=True, edgeColor=(1,1,1,1))

        self.gl_widget.addItem(self.agent_mesh)

        self.prev_x = 0
        self.prev_y = 0
        self.prev_z = 0

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

    def show_me(self):
        self.gl_widget.show()

    def setupcf(self):
        # Scan for Crazyflies and use the first one found
        print('Scanning interfaces for Crazyflies...')
        available = cflib.crtp.scan_interfaces()
        print('Crazyflies found:')
        for i in available:
            print(i[0])

        if len(available) > 0:
            self.cf = cf_logging(available[0][0])

            while (not self.cf.is_connected):
                time.sleep(1)

        else:
            print('No Crazyflies found :(')    

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

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    # Initialize the low-level drivers
    # cflib.crtp.init_drivers(enable_debug_driver=False)

    app = QtWidgets.QApplication(sys.argv)

    qt_plotter = Plotter()
    # qt_plotter.setupcf()
    qt_plotter.setupPlotter()
    qt_plotter.show_me()

    # qt_plotter.update_plot()

    sys.exit(app.exec_())

