from PyQt6 import QtCore, QtGui, QtWidgets

from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1064, 780)
        MainWindow.setStyleSheet("background:rgb(72, 72, 72);")
        
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.headerFrame = QtWidgets.QFrame(self.centralwidget)
        self.headerFrame.setGeometry(QtCore.QRect(0, 0, 1064, 70))
        self.headerFrame.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.headerFrame.setObjectName("headerFrame")
        
        self.homebutton = QtWidgets.QPushButton(self.headerFrame)
        self.homebutton.setGeometry(QtCore.QRect(20, 20, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.homebutton.setFont(font)
        self.homebutton.setStyleSheet("""
            QPushButton {
                background-color: rgb(72, 72, 72);
                color: rgb(255, 255, 255);
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(100, 100, 100);
            }
        """)
        self.homebutton.setObjectName("homebutton")
        
        self.bookbutton = QtWidgets.QPushButton(self.headerFrame)
        self.bookbutton.setGeometry(QtCore.QRect(260, 20, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.bookbutton.setFont(font)
        self.bookbutton.setStyleSheet("""
            QPushButton {
                background-color: rgb(72, 72, 72);
                color: rgb(255, 255, 255);
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(100, 100, 100);
            }
        """)
        self.bookbutton.setObjectName("bookbutton")
        
        self.customerbutton = QtWidgets.QPushButton(self.headerFrame)
        self.customerbutton.setGeometry(QtCore.QRect(500, 20, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.customerbutton.setFont(font)
        self.customerbutton.setStyleSheet("""
            QPushButton {
                background-color: rgb(72, 72, 72);
                color: rgb(255, 255, 255);
                border: none;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(100, 100, 100);
            }
        """)
        self.customerbutton.setObjectName("customerbutton")
        
        self.label = QtWidgets.QLabel(self.headerFrame)
        self.label.setGeometry(QtCore.QRect(765, 13, 301, 51))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(90)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white;")
        self.label.setObjectName("label")
        
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(20, 80, 1031, 691))
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.stackedWidget.setObjectName("stackedWidget")
        
        self.home = QtWidgets.QWidget()
        self.home.setObjectName("home")
        self.transactionstable = QtWidgets.QTableWidget(parent=self.home)
        self.transactionstable.setGeometry(QtCore.QRect(10, 50, 870, 627))
        self.transactionstable.setObjectName("transactionstable")
        self.transactionstable.setColumnCount(4)
        self.transactionstable.setRowCount(0)
        self.transactionstable.setHorizontalHeaderLabels(["Date", "Action", "Book ID", "Book Title", "Customer Name"])
        self.transactionstable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.transactionstable.setStyleSheet("""
            QTableWidget {
                color: white;
            }
        """)
        
        
        self.rentbtn = QtWidgets.QPushButton(parent=self.home)
        self.rentbtn.setGeometry(QtCore.QRect(890, 0, 131, 301))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.rentbtn.setFont(font)
        self.rentbtn.setStyleSheet("""
            QPushButton {
                background-color: rgb(6, 217, 66);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(50, 255, 100);
            }
        """)
        self.rentbtn.setObjectName("rentbtn")
        
        self.returnbtn = QtWidgets.QPushButton(parent=self.home)
        self.returnbtn.setGeometry(QtCore.QRect(890, 310, 131, 221))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.returnbtn.setFont(font)
        self.returnbtn.setStyleSheet("""
            QPushButton {
                background-color: rgb(10, 40, 147);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(50, 100, 255);
            }
        """)
        self.returnbtn.setObjectName("returnbtn")
        
        self.reservebtn = QtWidgets.QPushButton(parent=self.home)
        self.reservebtn.setGeometry(QtCore.QRect(890, 540, 131, 141))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.reservebtn.setFont(font)
        self.reservebtn.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 174, 61);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(255, 200, 100);
            }
        """)
        self.reservebtn.setObjectName("reservebtn")
        
        self.transactioncbox = QtWidgets.QComboBox(parent=self.home)
        self.transactioncbox.setGeometry(QtCore.QRect(10, 1, 161, 31))
        self.transactioncbox.setStyleSheet("""
            QComboBox {
                background: rgb(72, 72, 72);
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background: rgb(50, 50, 50);
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
        """)
        self.transactioncbox.setObjectName("transactioncbox")
        
        self.transactionsearch = QtWidgets.QLineEdit(parent=self.home)
        self.transactionsearch.setPlaceholderText("Search Transaction")
        self.transactionsearch.setGeometry(QtCore.QRect(180, 1, 701, 31))
        self.transactionsearch.setStyleSheet("""
            QLineEdit {
                background: rgb(72, 72, 72);
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
        """)
        self.transactionsearch.setObjectName("transactionsearch")
        
        self.stackedWidget.addWidget(self.home)
        
        self.book = QtWidgets.QWidget()
        self.book.setObjectName("book")
        self.booktable = QtWidgets.QTableWidget(parent=self.book)
        self.booktable.setGeometry(QtCore.QRect(10, 50, 870, 627))
        self.booktable.setObjectName("booktable")
        self.booktable.setColumnCount(7)
        self.booktable.setRowCount(0)
        self.booktable.setHorizontalHeaderLabels(["Book ID", "ISBN", "Title", "Author", "Category", "Status", "Rental Fee"])
        self.booktable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.booktable.setStyleSheet("""
            QTableWidget {
                color: white;
            }
        """)
        
        self.addbookbtn = QtWidgets.QPushButton(parent=self.book)
        self.addbookbtn.setGeometry(QtCore.QRect(890, 0, 131, 381))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.addbookbtn.setFont(font)
        self.addbookbtn.setStyleSheet("""
            QPushButton {
                background-color: rgb(6, 217, 66);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(50, 255, 100);
            }
        """)
        self.addbookbtn.setObjectName("addbookbtn")
        
        self.deletebookbtn = QtWidgets.QPushButton(parent=self.book)
        self.deletebookbtn.setGeometry(QtCore.QRect(890, 580, 131, 101))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.deletebookbtn.setFont(font)
        self.deletebookbtn.setStyleSheet("""
            QPushButton {
                background-color: rgb(200, 46, 18);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(255, 50, 50);
            }
        """)
        self.deletebookbtn.setObjectName("deletebookbtn")
        
        self.updatebookbtn = QtWidgets.QPushButton(parent=self.book)
        self.updatebookbtn.setGeometry(QtCore.QRect(890, 390, 131, 181))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.updatebookbtn.setFont(font)
        self.updatebookbtn.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 174, 61);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(255, 200, 100);
            }
        """)
        self.updatebookbtn.setObjectName("updatebookbtn")
        
        self.bookcbox = QtWidgets.QComboBox(parent=self.book)
        self.bookcbox.setGeometry(QtCore.QRect(10, 1, 161, 31))
        self.bookcbox.setStyleSheet("""
            QComboBox {
                background: rgb(72, 72, 72);
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background: rgb(50, 50, 50);
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
        """)
        self.bookcbox.setObjectName("bookcbox")
        
        self.booksearch = QtWidgets.QLineEdit(parent=self.book)
        self.booksearch.setPlaceholderText("Search Book")
        self.booksearch.setGeometry(QtCore.QRect(180, 1, 701, 31))
        self.booksearch.setStyleSheet("""
            QLineEdit {
                background: rgb(72, 72, 72);
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
        """)
        self.booksearch.setObjectName("booksearch")
        
        self.stackedWidget.addWidget(self.book)
        
        self.customer = QtWidgets.QWidget()
        self.customer.setObjectName("customer")
        self.customertable = QtWidgets.QTableWidget(parent=self.customer)
        self.customertable.setGeometry(QtCore.QRect(10, 50, 870, 627))
        self.customertable.setObjectName("customertable")
        self.customertable.setColumnCount(4)
        self.customertable.setRowCount(0)
        self.customertable.setHorizontalHeaderLabels(["Customer ID", "Name", "Gender", "Phone Number"])
        self.customertable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.customertable.setStyleSheet("""
            QTableWidget {
                color: white;
            }
        """)
        
        self.addcustomerbtn = QtWidgets.QPushButton(parent=self.customer)
        self.addcustomerbtn.setGeometry(QtCore.QRect(890, 0, 131, 381))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.addcustomerbtn.setFont(font)
        self.addcustomerbtn.setStyleSheet("""
            QPushButton {
                background-color: rgb(6, 217, 66);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(50, 255, 100);
            }
        """)
        self.addcustomerbtn.setObjectName("addcustomerbtn")
        
        self.updatecustomerbtn = QtWidgets.QPushButton(parent=self.customer)
        self.updatecustomerbtn.setGeometry(QtCore.QRect(890, 390, 131, 181))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.updatecustomerbtn.setFont(font)
        self.updatecustomerbtn.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 174, 61);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(255, 200, 100);
            }
        """)
        self.updatecustomerbtn.setObjectName("updatecustomerbtn")
        
        self.deletecustomerbtn = QtWidgets.QPushButton(parent=self.customer)
        self.deletecustomerbtn.setGeometry(QtCore.QRect(890, 580, 131, 101))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.deletecustomerbtn.setFont(font)
        self.deletecustomerbtn.setStyleSheet("""
            QPushButton {
                background-color: rgb(200, 46, 18);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(255, 50, 50);
            }
        """)
        self.deletecustomerbtn.setObjectName("deletecustomerbtn")
        
        self.customercbox = QtWidgets.QComboBox(parent=self.customer)
        self.customercbox.setGeometry(QtCore.QRect(10, 1, 161, 31))
        self.customercbox.setStyleSheet("""
            QComboBox {
                background: rgb(72, 72, 72);
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background: rgb(50, 50, 50);
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
        """)
        self.customercbox.setObjectName("customercbox")
        
        self.customersearch = QtWidgets.QLineEdit(parent=self.customer)
        self.customersearch.setPlaceholderText("Search Customer")
        self.customersearch.setGeometry(QtCore.QRect(180, 1, 701, 31))
        self.customersearch.setStyleSheet("""
            QLineEdit {
                background: rgb(72, 72, 72);
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
        """)
        self.customersearch.setObjectName("customersearch")
        
        self.stackedWidget.addWidget(self.customer)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1064, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)  # Set initial page to "Transactions"
        self.updateButtonStyles(0)  # Highlight the Transactions button by default
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.homebutton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.bookbutton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.customerbutton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        
        self.stackedWidget.currentChanged.connect(self.updateButtonStyles)

     
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.homebutton.setText(_translate("MainWindow", "Home"))
        self.bookbutton.setText(_translate("MainWindow", "Book"))
        self.customerbutton.setText(_translate("MainWindow", "Customer"))
        self.label.setText(_translate("MainWindow", "Book Rent System"))
        self.rentbtn.setText(_translate("MainWindow", "Rent"))
        self.returnbtn.setText(_translate("MainWindow", "Return"))
        self.reservebtn.setText(_translate("MainWindow", "Reserve"))
        self.addbookbtn.setText(_translate("MainWindow", "Add Book"))
        self.deletebookbtn.setText(_translate("MainWindow", "Delete Book"))
        self.updatebookbtn.setText(_translate("MainWindow", "Update Book"))
        self.addcustomerbtn.setText(_translate("MainWindow", "Add Customer"))
        self.updatecustomerbtn.setText(_translate("MainWindow", "Update Customer"))
        self.deletecustomerbtn.setText(_translate("MainWindow", "Delete Customer"))

    def updateButtonStyles(self, index):
        default_style = """
        QPushButton {
                background-color: rgb(72, 72, 72);
                color:rgb(255, 255, 255);
                border: none;
                padding: 10px;
                }
        QPushButton:hover {
                background-color: rgb(100, 100, 100);
        }
        """
        active_style = """
        QPushButton {
                background-color: rgb(50, 50, 50);
                color:rgb(255, 255, 255);
                border: none;
                padding: 10px;
        }
        """
        self.homebutton.setStyleSheet(default_style)
        self.bookbutton.setStyleSheet(default_style)
        self.customerbutton.setStyleSheet(default_style)
                
        if index == 0:
                self.homebutton.setStyleSheet(active_style)
        elif index == 1:
                self.bookbutton.setStyleSheet(active_style)
        elif index == 2:
                self.customerbutton.setStyleSheet(active_style)
