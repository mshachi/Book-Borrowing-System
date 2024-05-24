from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import sqlite3
import sys

class addBookDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(590, 564)
        Dialog.setStyleSheet("background:rgb(72, 72, 72)")
        self.Confirm = QtWidgets.QPushButton(parent=Dialog)
        self.Confirm.setGeometry(QtCore.QRect(90, 500, 221, 40))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Confirm.setFont(font)
        self.Confirm.setStyleSheet("QPushButton {\n"
                                   "background-color: rgb(6, 217, 66);\n"
                                   "color: white;\n"
                                   "border: none;\n"
                                   "border-radius: 5px;\n"
                                   "padding: 10px;\n"
                                   "}\n"
                                   "QPushButton:hover {\n"
                                   "background-color: rgb(50, 255, 100);\n"
                                   "}")
        self.Confirm.setFlat(False)
        self.Confirm.setObjectName("Confirm")
        self.Cancel = QtWidgets.QPushButton(parent=Dialog)
        self.Cancel.setGeometry(QtCore.QRect(330, 500, 231, 40))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.Cancel.setFont(font)
        self.Cancel.setStyleSheet("QPushButton {\n"
                                  "background-color: rgb(200, 46, 18);\n"
                                  "color: white;\n"
                                  "border: none;\n"
                                  "border-radius: 5px;\n"
                                  "padding: 10px;\n"
                                  "}\n"
                                  "QPushButton:hover {\n"
                                  "background-color: rgb(255, 100, 100);\n"
                                  "}")
        self.Cancel.setObjectName("Cancel")
        self.label_4 = QtWidgets.QLabel(parent=Dialog)
        self.label_4.setGeometry(QtCore.QRect(80, 80, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white;")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=Dialog)
        self.label_5.setGeometry(QtCore.QRect(90, 120, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color:white;")
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=Dialog)
        self.label_6.setGeometry(QtCore.QRect(70, 160, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:white;")
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(parent=Dialog)
        self.label_7.setGeometry(QtCore.QRect(40, 260, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color:white;")
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(parent=Dialog)
        self.label_8.setGeometry(QtCore.QRect(28, 360, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_8.setStyleSheet("color:white;")
        self.label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.bookdesc = QtWidgets.QTextEdit(parent=Dialog)
        self.bookdesc.setGeometry(QtCore.QRect(150, 260, 411, 101))
        self.bookdesc.setAutoFillBackground(False)
        self.bookdesc.setStyleSheet("background: white")
        self.bookdesc.setObjectName("bookdesc")
        self.isbnlineedit = QtWidgets.QLineEdit(parent=Dialog)
        self.isbnlineedit.setGeometry(QtCore.QRect(150, 84, 411, 22))
        self.isbnlineedit.setStyleSheet("background: white")
        self.isbnlineedit.setFrame(False)
        self.isbnlineedit.setObjectName("isbnlineedit")
        self.titlelineedit = QtWidgets.QLineEdit(parent=Dialog)
        self.titlelineedit.setGeometry(QtCore.QRect(150, 126, 411, 22))
        self.titlelineedit.setStyleSheet("background: white")
        self.titlelineedit.setObjectName("titlelineedit")
        self.authorlineedit = QtWidgets.QLineEdit(parent=Dialog)
        self.authorlineedit.setGeometry(QtCore.QRect(150, 170, 411, 22))
        self.authorlineedit.setStyleSheet("background: white")
        self.authorlineedit.setObjectName("authorlineedit")
        self.bookbasefee = QtWidgets.QLineEdit(parent=Dialog)
        self.bookbasefee.setGeometry(QtCore.QRect(150, 379, 411, 22))
        self.bookbasefee.setStyleSheet("background: white")
        self.bookbasefee.setObjectName("bookbasefee")
        self.label_9 = QtWidgets.QLabel(parent=Dialog)
        self.label_9.setGeometry(QtCore.QRect(30, 430, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_9.setStyleSheet("color:white;")
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName("label_9")
        self.openGLWidget = QOpenGLWidget(parent=Dialog)
        self.openGLWidget.setGeometry(QtCore.QRect(-230, 670, 300, 200))
        self.openGLWidget.setObjectName("openGLWidget")
        self.openpicbutton = QtWidgets.QPushButton(parent=Dialog)
        self.openpicbutton.setGeometry(QtCore.QRect(150, 440, 411, 31))
        self.openpicbutton.setStyleSheet("QPushButton {\n"
                                        "background-color: rgb(72, 72, 72);\n"
                                        "color:rgb(255, 255, 255);\n"
                                        "border: none;\n"
                                        "padding: 10px;\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "background-color: rgb(100, 100, 100);\n"
                                        "}")
        self.openpicbutton.setObjectName("openpicbutton")
        self.frame = QtWidgets.QFrame(parent=Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 591, 61))
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
        self.label.setGeometry(QtCore.QRect(230, 0, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:white;")
        self.label.setObjectName("label")
        self.categorybox = QtWidgets.QComboBox(parent=Dialog)
        self.categorybox.setGeometry(QtCore.QRect(150, 210, 231, 31))
        self.categorybox.setStyleSheet("background: white")
        self.categorybox.setObjectName("categorybox")

        genres = [
            "Action", "Adventure", "Anthology", "Art",
            "Biography", "Business",
            "Children's", "Classics", "Comedy", "Comics", "Contemporary", "Cookbooks", "Crime",
            "Drama", "Dystopian",
            "Economics", "Education", "Epic", "Essays",
            "Fairy Tale", "Fantasy", "Fiction", "Folklore",
            "Graphic Novels", "Gothic",
            "Historical Fiction", "History", "Horror", "Humor",
            "Inspirational", "Instructional",
            "Journalism",
            "Kids", "Knowledge",
            "Literary Fiction", "Literature",
            "Memoir", "Mystery", "Mythology",
            "Non-fiction",
            "Occult", "Outdoors",
            "Paranormal", "Philosophy", "Photography", "Poetry", "Political", "Psychology",
            "Queer Literature",
            "Realistic Fiction", "Reference", "Religion", "Romance",
            "Satire", "Science", "Science Fiction", "Self-help", "Short Stories", "Spiritual", "Sports", "Suspense",
            "Technology", "Thriller", "Travel", "True Crime",
            "Urban Fantasy",
            "Vampire", "Veterinary",
            "War", "Western",
            "Young Adult",
            "Zombie"
        ]

        self.categorybox.addItems(genres)

        self.label_10 = QtWidgets.QLabel(parent=Dialog)
        self.label_10.setGeometry(QtCore.QRect(60, 210, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color:white;")
        self.label_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_10.setObjectName("label_10")


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Connect the buttons to their respective slots
        self.Confirm.clicked.connect(Dialog.accept)
        self.Cancel.clicked.connect(Dialog.reject)
        self.openpicbutton.clicked.connect(self.open_file_dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Confirm.setText(_translate("Dialog", "Confirm"))
        self.Cancel.setText(_translate("Dialog", "Cancel"))
        self.label_4.setText(_translate("Dialog", "ISBN:"))
        self.label_5.setText(_translate("Dialog", "Title:"))
        self.label_6.setText(_translate("Dialog", "Author:"))
        self.label_7.setText(_translate("Dialog", "Description:"))
        self.label_8.setText(_translate("Dialog", "Base Rent Fee:"))
        self.bookdesc.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                   "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                   "p, li { white-space: pre-wrap; }\n"
                                                   "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.13913pt; font-weight:400; font-style:normal;\">\n"
                                                   "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.13913pt;\"><br /></p></body></html>"))
        self.label_9.setText(_translate("Dialog", "Book Cover:"))
        self.openpicbutton.setText(_translate("Dialog", "Select Picture"))
        self.label.setText(_translate("Dialog", "Add Book"))
        self.label_10.setText(_translate("Dialog", "Category:"))

    def open_file_dialog(self):
        try:
                file_path, _ = QFileDialog.getOpenFileName(None, "Select Book Cover", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
                if file_path:
                        self.openpicbutton.setText(file_path)
        except Exception as e:
                print("Error Occurred:", e)

    def get_book_info(self):
        ISBN = self.isbnlineedit.text()
        Title = self.titlelineedit.text()
        Author = self.authorlineedit.text()
        Category = self.categorybox.currentText()
        Status = "Available"
        Description = self.bookdesc.toPlainText()
        if self.openpicbutton != "Select Picture":
            Cover_image = self.openpicbutton.text()
        else:
             Cover_image = "No Image Available"
        try:
            bookbasefee = float(self.bookbasefee.text())
        except ValueError:
            bookbasefee = 0.0
        return ISBN, Title, Author, Category, Status, Description, bookbasefee, Cover_image

    def confirm_add_book(self):
        book_details = self.get_book_info()
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO books (BookId, Title, Author, Category, Status, RentalFee, Description, Cover_Image) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    book_details)
                conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error adding book: {e}")
    
    
