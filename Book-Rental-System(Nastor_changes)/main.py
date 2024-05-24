import sqlite3
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon

from mainwindow_v2 import Ui_MainWindow
from addbook import addBookDialog
from rentbook import RentBookDialog
from editbook import editbookDialog
from addcustomer import addCustomerDialog
from editcustomer import editCustomerDialog
from reservebook import ReserveDialog
from returnbook import ReturnDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        try:
            # Initialize the UI from a separate UI file
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

            # Connect UI elements to class variables
            self.homebutton = self.ui.homebutton
            self.bookbutton = self.ui.bookbutton
            self.customerbutton = self.ui.customerbutton
            self.stackedWidget = self.ui.stackedWidget
            self.booktable = self.ui.booktable
            self.customertable = self.ui.customertable
            self.deletebook = self.ui.deletebookbtn
            self.deletecustomer = self.ui.deletecustomerbtn

            # Connect button click events to methods
            self.homebutton.clicked.connect(self.show_home)
            self.bookbutton.clicked.connect(self.show_books)
            self.customerbutton.clicked.connect(self.show_customers)

            # Connect the Add Book button to the addBookDialog slot
            self.ui.addbookbtn.clicked.connect(self.add_book_dialog)
            self.ui.addcustomerbtn.clicked.connect(self.add_customer_dialog)
            self.ui.rentbtn.clicked.connect(self.rent_book_dialog)
            self.ui.returnbtn.clicked.connect(self.return_book_dialog)
            self.ui.reservebtn.clicked.connect(self.reserve_book_dialog)
            self.ui.updatebookbtn.clicked.connect(self.update_book_dialog)
            self.ui.updatecustomerbtn.clicked.connect(self.update_customer_dialog)
            self.deletebook.clicked.connect(self.delete_book_confirmation)
            self.deletecustomer.clicked.connect(self.delete_customer_confirmation)

            # Disable delete buttons initially
            self.deletebook.setEnabled(False)
            self.deletecustomer.setEnabled(False)

            # Connect table selection changes to methods
            self.booktable.itemSelectionChanged.connect(self.book_selection_changed)
            self.customertable.itemSelectionChanged.connect(self.customer_selection_changed)

            # Connect table double-click events to methods
            self.booktable.cellDoubleClicked.connect(self.show_book_info_dialog)
            self.customertable.cellDoubleClicked.connect(self.show_customer_info_dialog)

            # Initialize the UI
            self.show_home()

            # Initialize the database
            self.init_database()

            # Load books and customers
            self.load_books()
            self.load_customers()

        except Exception as e:
            print("An error occurred during initialization:", e)

    def book_selection_changed(self):
        # Enable the delete book button if a row is selected
        self.deletebook.setEnabled(self.booktable.selectionModel().hasSelection())

    def customer_selection_changed(self):
        # Enable the delete customer button if a row is selected
        self.deletecustomer.setEnabled(self.customertable.selectionModel().hasSelection())

    def show_home(self):
        # Set the current index of the stacked widget to show the home page
        self.stackedWidget.setCurrentIndex(0)

    def show_books(self):
        # Set the current index of the stacked widget to show the books page
        self.stackedWidget.setCurrentIndex(1)

    def show_customers(self):
        # Set the current index of the stacked widget to show the customers page
        self.stackedWidget.setCurrentIndex(2)

    # functionalities under book page
    def add_book_dialog(self):
        dialog = QtWidgets.QDialog()
        try:
            ui = addBookDialog()
            ui.setupUi(dialog)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                book_info = ui.get_book_info()
                self.add_book_to_db(book_info)
        except Exception as e:
            print("Error occurred:", e)

    def update_book_dialog(self):
        try:
            dialog = QtWidgets.QDialog()
            ui = editbookDialog()
            ui.setupUi(dialog)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                book_info = ui.get_book_info()
                self.update_book_in_db(book_info)
        except Exception as e:
            print("Error occurred:", e)

    # functionalities under home tab
    def rent_book_dialog(self):
        try:
            dialog = QtWidgets.QDialog()
            ui = RentBookDialog()
            ui.setupUi(dialog)
            dialog.exec()
        except Exception as e:
            print("Error occurred:", e)

    def return_book_dialog(self):
        try:
            dialog = QtWidgets.QDialog()
            ui = ReturnDialog()
            ui.setupUi(dialog)
            dialog.exec()
        except Exception as e:
            print("Error occurred:", e)

    def reserve_book_dialog(self):
        try:
            dialog = QtWidgets.QDialog()
            ui = ReserveDialog()
            ui.setupUi(dialog)
            dialog.exec()
        except Exception as e:
            print("Error occurred:", e)

    # functionalities under customer tab
    def add_customer_dialog(self):
        try:
            dialog = QtWidgets.QDialog()
            ui = addCustomerDialog()
            ui.setupUi(dialog)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                customer_info = ui.get_customer_info()
                self.add_customer_to_db(customer_info)
        except Exception as e:
            print("Error occurred:", e)

    def update_customer_dialog(self):
        try:
            dialog = QtWidgets.QDialog()
            ui = editCustomerDialog()
            ui.setupUi(dialog)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                customer_info = ui.get_customer_info()
                self.update_customer_in_db(customer_info)
        except Exception as e:
            print("Error occurred:", e)

    def delete_book_confirmation(self):
        selected_row = self.booktable.currentRow()
        book_id_item = self.booktable.item(selected_row, 0)  # Assuming BookID is the first column
        if book_id_item:
            book_id = book_id_item.text()
            confirmation_dialog = ConfirmationDialog("Are you sure you want to delete this book?")
            if confirmation_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                self.delete_book_from_db(book_id)
                self.load_books()

    def delete_customer_confirmation(self):
        selected_row = self.customertable.currentRow()
        customer_id_item = self.customertable.item(selected_row, 0)  # Assuming CustomerID is the first column
        if customer_id_item:
            customer_id = customer_id_item.text()
            confirmation_dialog = ConfirmationDialog("Are you sure you want to delete this customer?")
            if confirmation_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                self.delete_customer_from_db(customer_id)
                self.load_customers()

    def delete_book_from_db(self, book_id):
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM books WHERE BookID = ?", (book_id,))
                conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error deleting book: {e}")

    def delete_customer_from_db(self, customer_id):
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM customers WHERE CustomerID = ?", (customer_id,))
                conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error deleting customer: {e}")

    def init_database(self):
        try:
            # Connect to the SQLite database (or create it if it doesn't exist)
            conn = sqlite3.connect('library.db')
            c = conn.cursor()

            # Create the customers table
            c.execute('''CREATE TABLE IF NOT EXISTS customers
                         (CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
                          Name TEXT,
                          Gender TEXT,
                          PhoneNumber TEXT,
                          ValidIdPath TEXT)''')

            # Create the books table
            c.execute('''CREATE TABLE IF NOT EXISTS books
                         (BookID INTEGER PRIMARY KEY AUTOINCREMENT,
                          ISBN INTEGER,
                          Title TEXT,
                          Author TEXT,
                          Category TEXT,
                          Status TEXT,
                          RentalFee INTEGER,
                          Description TEXT,
                          Cover_Image TEXT)''')

            # Create the rentals table
            c.execute('''CREATE TABLE IF NOT EXISTS rentals
                         (RentalID INTEGER PRIMARY KEY AUTOINCREMENT,
                          CustomerID INTEGER,
                          BookID INTEGER,
                          RentalDate TEXT,
                          RentalDueDate TEXT,
                          RentalFee INTEGER,
                          FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
                          FOREIGN KEY (BookID) REFERENCES books(BookID))''')

            # Create the returns table
            c.execute('''CREATE TABLE IF NOT EXISTS returns
                         (ReturnID INTEGER PRIMARY KEY AUTOINCREMENT,
                          CustomerID INTEGER,
                          BookID INTEGER,
                          ReturnDate TEXT,
                          PenaltyFee INTEGER,
                          FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
                          FOREIGN KEY (BookID) REFERENCES books(BookID))''')

            # Create the reservations table
            c.execute('''CREATE TABLE IF NOT EXISTS reservations
                         (ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
                          CustomerID INTEGER,
                          BookID INTEGER,
                          ReservationDate TEXT,
                          ReservationStatus TEXT,
                          FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
                          FOREIGN KEY (BookID) REFERENCES books(BookID))''')

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error initializing database: {e}")

    def add_book_to_db(self, book_info):
        try:
            with sqlite3.connect('library.db') as conn:
                cursor = conn.cursor()

                cursor.execute('''INSERT INTO books (ISBN, Title, Author, Category, Status, RentalFee, Description, Cover_Image)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', book_info)

                conn.commit()
                self.load_books()  # Reload books after adding a new one
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error adding book to database: {e}")

    def add_customer_to_db(self, customer_info):
        try:
            with sqlite3.connect('library.db') as conn:
                cursor = conn.cursor()

                cursor.execute('''INSERT INTO customers (Name, Gender, PhoneNumber, ValidIdPath)
                                 VALUES (?, ?, ?, ?)''', customer_info)

                conn.commit()
                self.load_customers()  # Reload customers after adding a new one
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error adding customer to database: {e}")

    def load_books(self):
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT BookID, Title, Author, Category, Status, RentalFee, Description FROM books")
                books = cursor.fetchall()

            self.booktable.setRowCount(0)  # Clear existing rows

            for row_number, row_data in enumerate(books):
                self.booktable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.booktable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error loading books: {e}")

    def load_customers(self):
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT CustomerID, Name, Gender, PhoneNumber FROM customers")
                customers = cursor.fetchall()

            self.customertable.setRowCount(0)  # Clear existing rows

            for row_number, row_data in enumerate(customers):
                self.customertable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.customertable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error loading customers: {e}")

    def show_book_info_dialog(self, row, column):
        book_id = self.booktable.item(row, 0).text()
        book_info = self.get_book_info(book_id)
        if book_info:
            info_dialog = InfoDialog(book_info, 'book')
            info_dialog.exec()

    def show_customer_info_dialog(self, row, column):
        customer_id = self.customertable.item(row, 0).text()
        customer_info = self.get_customer_info(customer_id)
        if customer_info:
            info_dialog = InfoDialog(customer_info, 'customer')
            info_dialog.exec()

    def get_book_info(self, book_id):
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM books WHERE BookID = ?", (book_id,))
                book_info = cursor.fetchone()
                return book_info
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error retrieving book info: {e}")
            return None

    def get_customer_info(self, customer_id):
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM customers WHERE CustomerID = ?", (customer_id,))
                customer_info = cursor.fetchone()
                return customer_info
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error retrieving customer info: {e}")
            return None

class ConfirmationDialog(QtWidgets.QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmation")
        self.setFixedSize(300, 100)

        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel(message)
        self.label.setWordWrap(True)

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Yes | QtWidgets.QDialogButtonBox.StandardButton.No)

        layout.addWidget(self.label)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

class InfoDialog(QtWidgets.QDialog):
    def __init__(self, info, info_type):
        super().__init__()
        self.setWindowTitle("More Information")

        layout = QtWidgets.QVBoxLayout()

        if info_type == 'book':
            book_info_layout = QtWidgets.QVBoxLayout()
            title_label = QtWidgets.QLabel(f"Title: {info[2]}")
            author_label = QtWidgets.QLabel(f"Author: {info[3]}")
            category_label = QtWidgets.QLabel(f"Category: {info[4]}")
            status_label = QtWidgets.QLabel(f"Status: {info[5]}")
            description_label = QtWidgets.QLabel(f"Rental Fee: {info[7]}")
            rental_fee_label = QtWidgets.QLabel(f"Description: {info[6]}")

            book_info_layout.addWidget(title_label)
            book_info_layout.addWidget(author_label)
            book_info_layout.addWidget(category_label)
            book_info_layout.addWidget(status_label)
            book_info_layout.addWidget(description_label)
            book_info_layout.addWidget(rental_fee_label)

            if info[8]:
                cover_image_label = QtWidgets.QLabel()
                pixmap = QtGui.QPixmap(info[8])
                cover_image_label.setPixmap(pixmap.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                book_info_layout.addWidget(cover_image_label)

            layout.addLayout(book_info_layout)

        elif info_type == 'customer':
            customer_info_layout = QtWidgets.QVBoxLayout()
            name_label = QtWidgets.QLabel(f"Name: {info[1]}")
            gender_label = QtWidgets.QLabel(f"Gender: {info[2]}")
            phone_label = QtWidgets.QLabel(f"Phone Number: {info[3]}")

            customer_info_layout.addWidget(name_label)
            customer_info_layout.addWidget(gender_label)
            customer_info_layout.addWidget(phone_label)

            if info[4]:
                id_image_label = QtWidgets.QLabel()
                pixmap = QtGui.QPixmap(info[4])
                id_image_label.setPixmap(pixmap.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                customer_info_layout.addWidget(id_image_label)

            layout.addLayout(customer_info_layout)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.setWindowTitle('Library Management System')
    window.show()
    app.exec()
