# Form implementation generated from reading ui file 'addcustomer.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.
import sqlite3

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QFileDialog, QMessageBox


class addCustomerDialog(object):
    def setupUi(self, Dialog):
        self.dialog = Dialog

        

        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 316)
        Dialog.setStyleSheet("background:rgb(72, 72, 72)")
        self.label_6 = QtWidgets.QLabel(parent=Dialog)
        self.label_6.setGeometry(QtCore.QRect(70, 110, 81, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:white;")
        self.label_6.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.openGLWidget = QOpenGLWidget(parent=Dialog)
        self.openGLWidget.setGeometry(QtCore.QRect(-220, 671, 300, 200))
        self.openGLWidget.setObjectName("openGLWidget")
        self.phonenumber = QtWidgets.QLineEdit(parent=Dialog)
        self.phonenumber.setGeometry(QtCore.QRect(160, 130, 201, 22))
        self.phonenumber.setStyleSheet(" background: white; color: black")
        self.phonenumber.setObjectName("phonenumber")
        self.Confirm = QtWidgets.QPushButton(parent=Dialog)
        self.Confirm.setGeometry(QtCore.QRect(100, 250, 221, 40))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Confirm.setFont(font)
        self.Confirm.setStyleSheet("QPushButton {\n"
                                   "                background-color: rgb(6, 217, 66);\n"
                                   "                color: white;\n"
                                   "                border: none;\n"
                                   "                border-radius: 5px;\n"
                                   "                padding: 10px;\n"
                                   "            }\n"
                                   "            QPushButton:hover {\n"
                                   "                background-color: rgb(50, 255, 100);\n"
                                   "            }")
        self.Confirm.setFlat(False)
        self.Confirm.setObjectName("Confirm")
        self.Cancel = QtWidgets.QPushButton(parent=Dialog)
        self.Cancel.setGeometry(QtCore.QRect(340, 250, 231, 40))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Cancel.setFont(font)
        self.Cancel.setStyleSheet("QPushButton {\n"
                                  "                background-color: rgb(200, 46, 18);\n"
                                  "                color: white;\n"
                                  "                border: none;\n"
                                  "                border-radius: 5px;\n"
                                  "                padding: 10px;\n"
                                  "            }\n"
                                  "            QPushButton:hover {\n"
                                  "                background-color: rgb(255, 100, 100);\n"
                                  "            }")
        self.Cancel.setObjectName("Cancel")
        self.label_5 = QtWidgets.QLabel(parent=Dialog)
        self.label_5.setGeometry(QtCore.QRect(370, 120, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color:white;")
        self.label_5.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.openpicbutton = QtWidgets.QPushButton(parent=Dialog)
        self.openpicbutton.setGeometry(QtCore.QRect(160, 190, 411, 31))
        self.openpicbutton.setStyleSheet("QPushButton {\n"
                                         "                                        background-color: rgb(72, 72, 72);\n"
                                         "                                        color:rgb(255, 255, 255);\n"
                                         "                                        border: none;\n"
                                         "                                        padding: 10px;\n"
                                         "                                        }\n"
                                         "QPushButton:hover {\n"
                                         "                                        background-color: rgb(100, 100, 100);\n"
                                         "                                        }")
        self.openpicbutton.setObjectName("openpicbutton")
        self.label_4 = QtWidgets.QLabel(parent=Dialog)
        self.label_4.setGeometry(QtCore.QRect(99, 81, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white;")
        self.label_4.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.namecustomer = QtWidgets.QLineEdit(parent=Dialog)
        self.namecustomer.setGeometry(QtCore.QRect(160, 86, 411, 22))
        self.namecustomer.setStyleSheet(" background: white; color:black;")
        self.namecustomer.setFrame(False)
        self.namecustomer.setObjectName("namecustomer")
        self.label_9 = QtWidgets.QLabel(parent=Dialog)
        self.label_9.setGeometry(QtCore.QRect(40, 180, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_9.setStyleSheet("color:white;")
        self.label_9.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName("label_9")
        self.comboBox = QtWidgets.QComboBox(parent=Dialog)
        self.comboBox.setGeometry(QtCore.QRect(450, 130, 121, 22))
        self.comboBox.setStyleSheet("background-color: white; color: black;")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(["Male", "Female", "Other"])

        self.frame = QtWidgets.QFrame(parent=Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 641, 61))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setBold(True)
        font.setWeight(75)
        self.frame.setFont(font)
        self.frame.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(230, 0, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:white;")
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Connect the openpicbutton to a slot
        self.openpicbutton.clicked.connect(self.open_file_dialog)

        # Connect the Confirm button to the confirm_add_customer slot
        self.Confirm.clicked.connect(self.dialog.accept)
        self.Cancel.clicked.connect(self.dialog.close)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_6.setText(_translate("Dialog", "Phone Number:"))
        self.Confirm.setText(_translate("Dialog", "Confirm"))
        self.Cancel.setText(_translate("Dialog", "Cancel"))
        self.label_5.setText(_translate("Dialog", "Gender:"))
        self.openpicbutton.setText(_translate("Dialog", "Select Picture"))
        self.label_4.setText(_translate("Dialog", "Name:"))
        self.label_9.setText(_translate("Dialog", "Valid ID Photo:"))
        self.label.setText(_translate("Dialog", "Add Customer"))

        # Function to gather user input and add a new customer to the database

    def get_customer_info(self):
        print("Adding customer...")
        # Get the values from the input fields
        name = self.namecustomer.text()
        gender = self.comboBox.currentText()
        phone_number = self.phonenumber.text()
        valid_id_path = self.openpicbutton.text()  # Assuming this holds the path to the selected image

        # Perform validation checks
        if not name.strip() or not phone_number.strip() or not valid_id_path.strip():
            QMessageBox.critical(self.dialog, "Error", "Please fill in all fields.")
            return

        # Prepare the data to be inserted into the database
        customer_info = (name, gender, phone_number, valid_id_path)

        return customer_info

    def open_file_dialog(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self.dialog, "Select Book Cover", "",
                                                       "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
            if file_path:
                self.openpicbutton.setText(file_path)
        except FileNotFoundError as e:
            print("File not found:", e)
        except Exception as e:
            print("Error Occurred:", e)