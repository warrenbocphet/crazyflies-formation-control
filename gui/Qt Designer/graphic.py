# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crazyflie_multiagent.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
