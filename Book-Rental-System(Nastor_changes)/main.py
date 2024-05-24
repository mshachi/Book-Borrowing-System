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
                          RentalDueDate TEXT,
                          OverdueFee INTEGER,
                          FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
                          FOREIGN KEY (BookID) REFERENCES books(BookID),
                          FOREIGN KEY (RentalDueDate) REFERENCES rentals(RentalDueDate))''')

            # Create the reserve table
            c.execute('''CREATE TABLE IF NOT EXISTS reserve
                         (ReserveID INTEGER PRIMARY KEY AUTOINCREMENT,
                          CustomerID INTEGER,
                          BookID INTEGER,
                          ReservationDate TEXT,
                          ReservationFee REAL,
                          FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
                          FOREIGN KEY (BookID) REFERENCES books(BookID))''')

            # Commit the changes and close the connection
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def add_book_to_db(self, book_info):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()

            c.execute('''INSERT INTO books (ISBN, Title, Author, Category, Status, RentalFee, Description, Cover_Image)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', book_info)

            conn.commit()
            conn.close()

            self.load_books()
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def update_book_in_db(self, book_info):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()

            c.execute('''UPDATE books
                         SET ISBN = ?, Title = ?, Author = ?, Category = ?, Status = ?, RentalFee = ?, Description = ?, Cover_Image = ?
                         WHERE BookID = ?''', book_info)

            conn.commit()
            conn.close()

            self.load_books()
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def load_books(self):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()

            c.execute('SELECT * FROM books')
            books = c.fetchall()

            self.booktable.setRowCount(len(books))
            for row_idx, row_data in enumerate(books):
                for col_idx, col_data in enumerate(row_data):
                    self.booktable.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            conn.close()
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def add_customer_to_db(self, customer_info):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()

            c.execute('''INSERT INTO customers (Name, Gender, PhoneNumber, ValidIdPath)
                         VALUES (?, ?, ?, ?)''', customer_info)

            conn.commit()
            conn.close()

            self.load_customers()
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def update_customer_in_db(self, customer_info):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()

            c.execute('''UPDATE customers
                         SET Name = ?, Gender = ?, PhoneNumber = ?, ValidIdPath = ?
                         WHERE CustomerID = ?''', customer_info)

            conn.commit()
            conn.close()

            self.load_customers()
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def load_customers(self):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()

            c.execute('SELECT * FROM customers')
            customers = c.fetchall()

            self.customertable.setRowCount(len(customers))
            for row_idx, row_data in enumerate(customers):
                for col_idx, col_data in enumerate(row_data):
                    self.customertable.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            conn.close()
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def show_book_info_dialog(self):
        selected_row = self.booktable.currentRow()
        book_details = []
        headers = ['BookID', 'ISBN', 'Title', 'Author', 'Category', 'Status', 'Rental Fee', 'Description', 'Cover Image']
        for col in range(self.booktable.columnCount()):
            item = self.booktable.item(selected_row, col)
            if item:
                book_details.append((headers[col], item.text()))

        dialog = InfoDialog("Book Information", book_details)
        dialog.exec()

    def show_customer_info_dialog(self):
        selected_row = self.customertable.currentRow()
        customer_details = []
        headers = ['CustomerID', 'Name', 'Gender', 'Phone Number', 'Valid ID Path']
        for col in range(self.customertable.columnCount()):
            item = self.customertable.item(selected_row, col)
            if item:
                customer_details.append((headers[col], item.text()))

        dialog = InfoDialog("Customer Information", customer_details)
        dialog.exec()


class InfoDialog(QtWidgets.QDialog):
    def __init__(self, title, details):
        super().__init__()
        self.setWindowTitle(title)
        self.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #333;
                padding: 5px 0;
            }
            QDialog {
                background-color: #f5f5f5;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            QVBoxLayout {
                padding: 20px;
            }
        """)

        layout = QtWidgets.QVBoxLayout()

        # Optional: Add a title label with different styling
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #444; margin-bottom: 15px;")
        layout.addWidget(title_label)

        for header, detail in details:
            if header in ['Cover Image', 'Valid ID Path']:
                label = QtWidgets.QLabel(header + ":")
                layout.addWidget(label)
                image_label = QtWidgets.QLabel()
                pixmap = QtGui.QPixmap(detail)
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(500, 500, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                    image_label.setPixmap(pixmap)
                else:
                    image_label.setText("Image not found")
                layout.addWidget(image_label)
            else:
                label = QtWidgets.QLabel(f"{header}: {detail}")
                layout.addWidget(label)

        # Add a close button at the bottom
        close_button = QtWidgets.QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 10px 20px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

class ConfirmationDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Confirmation")

        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel(message)
        layout.addWidget(label)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Yes | QtWidgets.QDialogButtonBox.StandardButton.No)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
