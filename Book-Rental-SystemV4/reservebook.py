import sqlite3

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog, QCalendarWidget, QMessageBox


class ReserveBookDialog(QDialog):  # Inherit from QDialog
    def __init__(self):
        super().__init__()
        self.dialog = self  # Properly initialize the dialog
        self.setupUi(self)

    def setupUi(self, ReserveDialog):
        self.dialog = ReserveDialog
        ReserveDialog.setObjectName("ReserveDialog")
        ReserveDialog.resize(609, 326)
        ReserveDialog.setStyleSheet("background:rgb(72, 72, 72)")
        self.label_5 = QtWidgets.QLabel(parent=ReserveDialog)
        self.label_5.setGeometry(QtCore.QRect(90, 104, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color:white;")
        self.label_5.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=ReserveDialog)
        self.label_6.setGeometry(QtCore.QRect(40, 200, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color:white;")
        self.label_6.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(parent=ReserveDialog)
        self.label_7.setGeometry(QtCore.QRect(28, 154, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color:white;")
        self.label_7.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.bookscbox = QtWidgets.QComboBox(parent=ReserveDialog)
        self.bookscbox.setGeometry(QtCore.QRect(180, 74, 371, 22))
        self.bookscbox.setStyleSheet(" background: white; color: black;")
        self.bookscbox.setObjectName("bookscbox")
        self.Confirm = QtWidgets.QPushButton(parent=ReserveDialog)
        self.Confirm.setGeometry(QtCore.QRect(70, 260, 221, 40))
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
        self.label_4 = QtWidgets.QLabel(parent=ReserveDialog)
        self.label_4.setGeometry(QtCore.QRect(120, 70, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:white;")
        self.label_4.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.rentfeefield = QtWidgets.QLineEdit(parent=ReserveDialog)
        self.rentfeefield.setGeometry(QtCore.QRect(180, 205, 371, 22))
        self.rentfeefield.setStyleSheet(" background: white; color:black;;")
        self.rentfeefield.setFrame(False)
        self.rentfeefield.setObjectName("rentfeefield")
        self.reservedate = QtWidgets.QPushButton(parent=ReserveDialog)
        self.reservedate.setGeometry(QtCore.QRect(180, 150, 371, 40))
        font = QtGui.QFont()
        font.setFamily("Nirmala UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.reservedate.setFont(font)
        self.reservedate.setStyleSheet("QPushButton {\n"
                                       "                background-color: rgb(255, 170, 0);\n"
                                       "                color: white;\n"
                                       "                border: none;\n"
                                       "                border-radius: 5px;\n"
                                       "                padding: 10px;\n"
                                       "            }\n"
                                       "            QPushButton:hover {\n"
                                       "                background-color: rgb(255, 196, 78);\n"
                                       "            }")
        self.reservedate.setFlat(False)
        self.reservedate.setObjectName("reservedate")
        self.Cancel = QtWidgets.QPushButton(parent=ReserveDialog)
        self.Cancel.setGeometry(QtCore.QRect(320, 260, 231, 40))
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
        self.customercbox = QtWidgets.QComboBox(parent=ReserveDialog)
        self.customercbox.setGeometry(QtCore.QRect(180, 110, 371, 22))
        self.customercbox.setStyleSheet(" background: white; color:black;")
        self.customercbox.setObjectName("customercbox")
        self.frame = QtWidgets.QFrame(parent=ReserveDialog)
        self.frame.setGeometry(QtCore.QRect(-10, 0, 641, 61))
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
        self.label.setGeometry(QtCore.QRect(220, 4, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:white;")
        self.label.setObjectName("label")

        self.retranslateUi(ReserveDialog)
        QtCore.QMetaObject.connectSlotsByName(ReserveDialog)

        # Connect buttons to functions
        self.reservedate.clicked.connect(self.select_reserve_date)
        self.Confirm.clicked.connect(self.ConfirmReserve)
        self.Cancel.clicked.connect(self.dialog.close)

        self.populate_books()
        self.populate_customers()

    def retranslateUi(self, ReserveDialog):
        _translate = QtCore.QCoreApplication.translate
        ReserveDialog.setWindowTitle(_translate("ReserveDialog", "Reserve Book"))
        self.label_5.setText(_translate("ReserveDialog", "Customer:"))
        self.label_6.setText(_translate("ReserveDialog", "Reservation Fee:"))
        self.label_7.setText(_translate("ReserveDialog", "Reservation Date:"))
        self.Confirm.setText(_translate("ReserveDialog", "Confirm"))
        self.label_4.setText(_translate("ReserveDialog", "Books:"))
        self.reservedate.setText(_translate("ReserveDialog", "Date of Reservation"))
        self.Cancel.setText(_translate("ReserveDialog", "Cancel"))
        self.label.setText(_translate("ReserveDialog", "Reserve Book"))

    def populate_books(self):
        try:
            # Connect to the database
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            # Fetch book titles from the books table with Status "Rented"
            cursor.execute("SELECT Title FROM books")
            books = cursor.fetchall()

            # Populate the bookscbox combobox with the fetched titles
            for book in books:
                self.bookscbox.addItem(book[0])

            # Close the database connection
            conn.close()
        except sqlite3.Error as e:
            print("An error occurred while populating books:", e)

    def populate_customers(self):
        try:
            # Connect to the database
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            # Fetch customer names from the customers table
            cursor.execute("SELECT Name FROM customers")
            customers = cursor.fetchall()

            # Populate the customer combobox with the fetched names
            for customer in customers:
                self.customercbox.addItem(customer[0])

            # Close the database connection
            conn.close()
        except sqlite3.Error as e:
            print("An error occurred while populating customers:", e)

    def select_reserve_date(self):
        try:
            # Create a calendar dialog
            calendar_dialog = QDialog()
            calendar_dialog.setWindowTitle("Select Reservation Date")
            calendar = QCalendarWidget(calendar_dialog)
            calendar.setGeometry(10, 10, 400, 250)

            # Create a button to confirm the date selection
            select_button = QtWidgets.QPushButton("Select Date", calendar_dialog)
            select_button.setGeometry(150, 270, 100, 30)
            select_button.clicked.connect(lambda: self.on_reservedate_selected(calendar, calendar_dialog))

            # Show the calendar dialog
            calendar_dialog.exec()
        except Exception as e:
            print(e)

    def on_reservedate_selected(self, calendar, dialog):
        # Get the selected date from the calendar widget
        selected_date = calendar.selectedDate()

        # If no date is selected, return without setting the button text
        if not selected_date.isValid():
            return

        # Format the selected date as a string
        formatted_date = selected_date.toString(QtCore.Qt.DateFormat.ISODate)

        # Set the selected date as the text of the due date button
        self.reservedate.setText(formatted_date)

        # Store the selected reservation date in a class variable for later use
        self.selected_reserve_date = formatted_date

        # Close the dialog
        dialog.accept()

    def ConfirmReserve(self):
        book_title = self.bookscbox.currentText()
        customer_name = self.customercbox.currentText()
        reserve_date = getattr(self, 'selected_reserve_date', None)
        reserve_fee = self.rentfeefield.text()

        if reserve_date is None:
            QMessageBox.warning(self.dialog, "Error", "Reservation date is not selected")
            return

        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

                        # Get Book ID and Customer ID
            cursor.execute("SELECT BookID FROM books WHERE Title = ?", (book_title,))
            book_id_result = cursor.fetchone()
            if book_id_result is None:
                QMessageBox.warning(self.dialog, "Error", "Book not found")
                conn.close()
                return
            book_id = book_id_result[0]

            cursor.execute("SELECT CustomerID FROM customers WHERE Name = ?", (customer_name,))
            customer_id_result = cursor.fetchone()
            if customer_id_result is None:
                QMessageBox.warning(self.dialog, "Error", "Customer not found")
                conn.close()
                return
            customer_id = customer_id_result[0]

            # Insert the reservation record
            cursor.execute(
                "INSERT INTO reserve (CustomerId, BookId, ReservationDate, ReservationFee) VALUES (?, ?, ?, ?)",
                (customer_id, book_id, reserve_date, reserve_fee))

            cursor.execute("SELECT Status FROM books WHERE BookID = ?", (book_id,))
            book_status_result = cursor.fetchone()
            if book_status_result[0] == 'Available':
                # Update the status of the book to 'Reserved'
                cursor.execute("UPDATE books SET Status = 'Reserved' WHERE BookID = ?", (book_id,))

            conn.commit()
            conn.close()
            self.dialog.accept()
            QMessageBox.information(self.dialog, "Reserve Book",
                                     f"Reserved by {customer_name} on {reserve_date} with reservation fee {reserve_fee}")
        except sqlite3.Error as e:
            print("Error reserving book:", e)
            QMessageBox.critical(self.dialog, "Error", f"Error reserving book: {e}")
