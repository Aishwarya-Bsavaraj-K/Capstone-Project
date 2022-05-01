from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mainDesign import Ui_CaptchaGame
import sys
import aes_functions as aes
import os
import requests
import datetime
import hashlib


class Main(QStackedWidget):
	def __init__(self):
		super().__init__()
		self.stack = Ui_CaptchaGame()
		self.stack.setupUi(self)
		self.screens = {'loginPage':0,
						'mainPage':1}
		
		self.stack.loginButton.clicked.connect(self.login)
		self.stack.uploadButton.clicked.connect(self.encrypt_and_upload)
		self.stack.selectFileButton.clicked.connect(self.selectFile)
		self.stack.tableWidget.itemClicked.connect(self.handle_item_clicked)

		# self.key = 'hello 123'
		# self.aesEncryptor  = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')

		# self.uploadFile()

	def table_appender(self,widget, *args):

	    def set_columns(len, pos):
	        if pos == len-1:
	            widget.setItem(widget.rowCount()-1, pos, QTableWidgetItem(args[pos]))
	        else:
	            widget.setItem(widget.rowCount()-1, pos, QTableWidgetItem(args[pos]))
	            set_columns(len, pos+1)
	    widget.insertRow(widget.rowCount())
	    set_columns(widget.columnCount(), 0)

	def handle_item_clicked(self,tableItem):
		# print(help(tableItem.row))
		fileName = tableItem.text().split('.enc')[0]
		print(fileName)
		r = requests.get('http://localhost:5555/register/'+fileName)
		self.showMessage(r.text)
		
		# print(tableItem.column(1))


	def encrypt_and_upload(self):
		file = self.input_file_path
		print("file is ",file)
		num_blocks = aes.encrypt_file(file,chunksize=1024)
		m = hashlib.sha256()
		# # post_params = {'parameters': params}
		with open(file+'.enc','rb') as f:
			block = f.read()
			print(block)
			digest = hashlib.sha256(block).hexdigest()
			# print('digest is {}'.format(digest))
			print('digest is {}'.format(hashlib.sha256(block).hexdigest()))


		files = {'file': open(file+'.enc','rb')}
		url = "http://localhost:5000/upload"
		r = requests.post(url, data={'userId':1}, files=files)

		if (r.status_code == 200):
			r =requests.post("http://localhost:5555/audit",data={'userId':1,
																 'numBlocks':num_blocks,
																 'fileName':os.path.basename(self.input_file_path),
																 'fileHash':digest})
			self.table_appender(self.stack.tableWidget,'1',os.path.basename(self.input_file_path),'True','True')
			self.showMessage("Success")

		# file.?close() # close the BytesIO object


	def match_category(self,row,col):
		if self.current_category == self.game.images[row][col].category:
			self.showMessage("correct")
		else:
			self.showMessage("Wrong!!")
	def showMessage(self,msg):
		QMessageBox.information(self,"Message",msg)
		
	def login(self):
		username = self.stack.usernameBox.text()
		password = self.stack.passwordBox.text()
		if username == 'admin' and password=='admin':
			self.loadDataFromCloud()
			self.displayPage('mainPage')
		else:
			self.showMessage("Username/password invalid")

	def displayPage(self,page):
		self.setCurrentIndex(self.screens.get(page))

	def loadDataFromCloud(self):
		r =requests.get("http://localhost:5555/getUploads")
		# self.stack.tableWidget.horizontalHeaderItem().setTextAlignment(Qt.AlignHCenter)

		self.stack.tableWidget.setRowCount(len(r.json()['values']))
		self.stack.tableWidget.setColumnCount(4)
		self.stack.tableWidget.setHorizontalHeaderLabels("UserId;FileName;isValid;isResolved;".split(";"))

		print(r.json())

		for inx,row in enumerate(r.json()['values']):
			self.stack.tableWidget.insertRow(inx)
			self.stack.tableWidget.setItem(inx, 0,QTableWidgetItem(str(row['userId'])))
			self.stack.tableWidget.setItem(inx, 1,QTableWidgetItem(str(row['fileName'])))
			self.stack.tableWidget.setItem(inx, 2,QTableWidgetItem(str(row['isValid'])))
			self.stack.tableWidget.setItem(inx, 3,QTableWidgetItem(str(row['resolved'])))


			# # print(row)
			# for i,k in enumerate(row):
			# 	print(k)
			# 	self.stack.tableWidget.setItem(inx, i,QTableWidgetItem(str(row[k])))

    # # where c is the cursor
    # self.c.execute('''SELECT * FROM table ''')
    # rows = self.c.fetchall()



	def uploadDataToCloud(self):
		username = self.stack.usernameBox.text()
		password = self.stack.passwordBox.text()

	def selectFile(self):
		self.input_file_path = QFileDialog.getOpenFileName(self, 'Select a file to upload', os.path.join(os.getcwd()))[0]
		self.stack.fileNameBox.setText(self.input_file_path)
		# self.encrypt(self.input_file_path)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	main = Main()
	main.show()
	sys.exit(app.exec_())