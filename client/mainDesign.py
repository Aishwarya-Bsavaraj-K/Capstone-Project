# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CaptchaGame(object):
    def setupUi(self, CaptchaGame):
        CaptchaGame.setObjectName("CaptchaGame")
        CaptchaGame.resize(897, 642)
        self.loginPage = QtWidgets.QWidget()
        self.loginPage.setObjectName("loginPage")
        self.label = QtWidgets.QLabel(self.loginPage)
        self.label.setGeometry(QtCore.QRect(38, 70, 101, 20))
        self.label.setStyleSheet("font-weight:bold;font-size:15px;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.loginPage)
        self.label_2.setGeometry(QtCore.QRect(40, 130, 101, 20))
        self.label_2.setStyleSheet("font-weight:bold;font-size:15px;")
        self.label_2.setObjectName("label_2")
        self.usernameBox = QtWidgets.QLineEdit(self.loginPage)
        self.usernameBox.setGeometry(QtCore.QRect(160, 61, 191, 31))
        self.usernameBox.setObjectName("usernameBox")
        self.passwordBox = QtWidgets.QLineEdit(self.loginPage)
        self.passwordBox.setGeometry(QtCore.QRect(160, 120, 191, 31))
        self.passwordBox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordBox.setObjectName("passwordBox")
        self.loginButton = QtWidgets.QPushButton(self.loginPage)
        self.loginButton.setGeometry(QtCore.QRect(240, 200, 111, 41))
        self.loginButton.setStyleSheet("background:#2e2e2e;color:#fefefe;font-weight:bold;font-size:20px;")
        self.loginButton.setObjectName("loginButton")
        self.label_3 = QtWidgets.QLabel(self.loginPage)
        self.label_3.setGeometry(QtCore.QRect(140, 10, 201, 20))
        self.label_3.setObjectName("label_3")
        CaptchaGame.addWidget(self.loginPage)
        self.mainGamePage = QtWidgets.QWidget()
        self.mainGamePage.setObjectName("mainGamePage")
        self.questionLabel = QtWidgets.QLabel(self.mainGamePage)
        self.questionLabel.setGeometry(QtCore.QRect(260, 20, 341, 20))
        self.questionLabel.setObjectName("questionLabel")
        self.tableWidget = QtWidgets.QTableWidget(self.mainGamePage)
        self.tableWidget.setGeometry(QtCore.QRect(110, 290, 601, 351))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.selectFileButton = QtWidgets.QPushButton(self.mainGamePage)
        self.selectFileButton.setGeometry(QtCore.QRect(500, 70, 161, 41))
        self.selectFileButton.setObjectName("selectFileButton")
        self.fileNameBox = QtWidgets.QLineEdit(self.mainGamePage)
        self.fileNameBox.setGeometry(QtCore.QRect(120, 70, 371, 41))
        self.fileNameBox.setObjectName("fileNameBox")
        self.uploadButton = QtWidgets.QPushButton(self.mainGamePage)
        self.uploadButton.setGeometry(QtCore.QRect(369, 140, 121, 41))
        self.uploadButton.setObjectName("uploadButton")
        CaptchaGame.addWidget(self.mainGamePage)

        self.retranslateUi(CaptchaGame)
        QtCore.QMetaObject.connectSlotsByName(CaptchaGame)

    def retranslateUi(self, CaptchaGame):
        _translate = QtCore.QCoreApplication.translate
        CaptchaGame.setWindowTitle(_translate("CaptchaGame", "StackedWidget"))
        self.label.setText(_translate("CaptchaGame", "Username"))
        self.label_2.setText(_translate("CaptchaGame", "Password"))
        self.loginButton.setText(_translate("CaptchaGame", "Login"))
        self.label_3.setText(_translate("CaptchaGame", "Client login TPA"))
        self.questionLabel.setText(_translate("CaptchaGame", "Welcome"))
        self.selectFileButton.setText(_translate("CaptchaGame", "Select File"))
        self.uploadButton.setText(_translate("CaptchaGame", "Upload"))

