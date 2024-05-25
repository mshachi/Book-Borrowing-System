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
from reservebook import ReserveBookDialog
from returnbook import ReturnBookDialog


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
            self.transactionstable = self.ui.transactionstable
            self.deletebook = self.ui.deletebookbtn
            self.deletecustomer = self.ui.deletecustomerbtn
            self.customersearch = self.ui.customersearch
            self.booksearch = self.ui.booksearch
            self.transactionssearch = self.ui.transactionsearch

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
            
            self.ui.transactioncbox.currentTextChanged.connect(self.filter_transactions)

            # Disable delete buttons initially
            self.deletebook.setEnabled(False)
            self.deletecustomer.setEnabled(False)


            # Connect search bar text changed signals
            self.booksearch.textChanged.connect(self.filter_books)
            self.customersearch.textChanged.connect(self.filter_customers)

            # Connect table selection changes to methods
            self.booktable.itemSelectionChanged.connect(self.book_selection_changed)
            self.customertable.itemSelectionChanged.connect(self.customer_selection_changed)

            # Connect table double-click events to methods
            self.transactionstable.cellDoubleClicked.connect(self.show_transaction_info_dialog)
            self.booktable.cellDoubleClicked.connect(self.show_book_info_dialog)
            self.customertable.cellDoubleClicked.connect(self.show_customer_info_dialog)

            # Initialize the UI
            self.show_home()

            # Initialize the database
            self.init_database()

            # Load books and customers
            self.load_books()
            self.load_customers()

            self.load_transactions()

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
            print("Error occurred: 2", e)

    def update_book_dialog(self):
        try:
            dialog = QtWidgets.QDialog()
            ui = editbookDialog()
            ui.setupUi(dialog)
            dialog.exec()
        except Exception as e:
            print("Error occurred: 4", e)

    # functionalities under home tab
    def rent_book_dialog(self):
        try:
            dialog = QtWidgets.QDialog()
            ui = RentBookDialog()
            ui.setupUi(dialog)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_transactions()
        except Exception as e:
            print("Error occurred: 3", e)

    def return_book_dialog(self):
        try:
            dialog = QtWidgets.QDialog()
            ui = ReturnBookDialog()
            ui.setupUi(dialog)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_transactions()
                self.load_books()
        except Exception as e:
            print("Error occurred: 5", e)

    def reserve_book_dialog(self):
        try:
            dialog = QtWidgets.QDialog()
            ui = ReserveBookDialog()
            ui.setupUi(dialog)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_transactions()
        except Exception as e:
            print("Error occurred: 6", e)

    # functionalities under customer tab
    def add_customer_dialog(self):
        try:
            dialog = QtWidgets.QDialog()
            ui = addCustomerDialog()
            ui.setupUi(dialog)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                customer_info = ui.get_customer_info()
                self.add_customer_to_db(customer_info)
            self.load_customers()
        except Exception as e:
            print("Error occurred: 6", e)

    def update_customer_dialog(self):
        try:
            dialog = QtWidgets.QDialog()
            ui = editCustomerDialog()
            ui.setupUi(dialog)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                customer_info = ui.get_customer_info()
                self.update_customer_in_db(customer_info)
            self.load_customers()
        except Exception as e:
            print("Error occurred: 7", e)

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
                          ISBN TEXT,
                          Title TEXT,
                          Author TEXT,
                          Category TEXT,
                          Status TEXT,
                          RentalFee REAL,
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
    
  

    def update_book_dialog(self):
        
        selected_row = self.booktable.currentRow()
        if selected_row < 0:
                QMessageBox.warning(self, "Warning", "Please select a book to edit.")
                return

        book_id_item = self.booktable.item(selected_row, 0)  # Assuming CustomerID is the first column
        if not book_id_item:
                QMessageBox.warning(self, "Warning", "Invalid book selected.")
                return
        
        book_id = book_id_item.text()

            # Fetch customer data from database
        book_data = self.get_book_data_from_db(book_id)
                

        if not book_data:
                QMessageBox.warning(self, "Warning", "Could not fetch book data.")
                return
            
        dialog = QtWidgets.QDialog()
        ui = editbookDialog()
        ui.setupUi(dialog)
        ui.load_book_data(book_data)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                updated_book_info = list(ui.get_book_info())
                updated_book_info.append(book_id)
                print(updated_book_info)
                self.update_book_in_db(updated_book_info)
            except Exception as e:
                print("Error occurred here at line 325: ", e)

    def get_book_data_from_db(self, book_id):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute('SELECT ISBN, Title, Author, Category, RentalFee, Description, Cover_Image FROM books WHERE BookID = ?', (book_id,))
            book = c.fetchone()
            conn.close()

            if book:
                return {
                'ISBN': book[0],
                'Title':  book[1],
                'Author': book[2],
                'Category': book[3],
                'RentalFee': str(book[4]),
                'Description': book[5],
                'Cover_Image': book[6],
                }
            
            print("i am executed", book)
            return None
        except sqlite3.Error as e:
            print("An error occurred:", e)
            return None
        
    def update_book_in_db(self, book_info):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute('''
                UPDATE books
                SET ISBN = ?, Title = ?, Author = ?, Category = ?, RentalFee = ?, Description = ?, Cover_Image = ?
                WHERE BookID = ?
            ''', (book_info))
            
            conn.commit()
            conn.close()
            self.load_books()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error updating Book: {e}")

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
        # Connect to the database
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()

                # Execute the SQL query to insert a new customer
                cursor.execute(
                    "INSERT INTO customers (Name, Gender, PhoneNumber, ValidIdPath) VALUES (?, ?, ?, ?)",
                    customer_info)
                print("SUCCESS!")
                # Commit the transaction
                conn.commit()

        except sqlite3.Error as e:
            # Display an error message if an error occurs
            print(f"Error adding customer: {e}")


    def update_customer_dialog(self):
        try:
            selected_row = self.customertable.currentRow()
            if selected_row < 0:
                QMessageBox.warning(self, "Warning", "Please select a customer to edit.")
                return

            customer_id_item = self.customertable.item(selected_row, 0)  # Assuming CustomerID is the first column
            if not customer_id_item:
                QMessageBox.warning(self, "Warning", "Invalid customer selected.")
                return

            customer_id = customer_id_item.text()

            # Fetch customer data from database
            customer_data = self.get_customer_data_from_db(customer_id)
            if not customer_data:
                QMessageBox.warning(self, "Warning", "Could not fetch customer data.")
                return

            dialog = QtWidgets.QDialog()
            ui = editCustomerDialog()
            ui.setupUi(dialog)
            ui.load_customer_data(customer_data)

            if dialog.exec() == QDialog.DialogCode.Accepted:
                updated_customer_info = ui.get_customer_info()
                updated_customer_info['CustomerID'] = customer_id
                self.update_customer_in_db(updated_customer_info)
        except Exception as e:
            print("Error occurred: 1", e)

    def get_customer_data_from_db(self, customer_id):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute('SELECT Name, Gender, PhoneNumber, ValidIdPath FROM customers WHERE CustomerID = ?', (customer_id,))
            customer = c.fetchone()
            conn.close()

            if customer:
                return {
                    'Name': customer[0],
                    'Gender': customer[1],
                    'PhoneNumber': customer[2],
                    'ValidIdPath': customer[3]
                }
            return None
        except sqlite3.Error as e:
            print("An error occurred:", e)
            return None

    def update_customer_in_db(self, customer_info):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute('''
                UPDATE customers
                SET Name = ?, Gender = ?, PhoneNumber = ?, ValidIdPath = ?
                WHERE CustomerID = ?
            ''', (customer_info['Name'], customer_info['Gender'], customer_info['PhoneNumber'], customer_info['ValidIdPath'], customer_info['CustomerID']))

            conn.commit()
            conn.close()
            self.load_customers()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error updating customer: {e}")

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

    def show_book_info_dialog(self, row, column):
        book_id = self.booktable.item(row, 0).text()
        book_info = self.get_book_info(book_id)
        if book_info:
            info_dialog = InfoDialog(book_info, 'book')
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

    def show_customer_info_dialog(self, row, column):
        customer_id = self.customertable.item(row, 0).text()
        customer_info = self.get_customer_info(customer_id)
        if customer_info:
            info_dialog = InfoDialog(customer_info, 'customer')
            info_dialog.exec()

    def filter_books(self, text):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()

            query = f"SELECT * FROM books WHERE Title LIKE '%{text}%' OR RentalFee LIKE '%{text}%' OR Author LIKE '%{text}%' OR Category LIKE '%{text}%' OR Status LIKE '%{text}%'"
            c.execute(query)
            books = c.fetchall()

            self.booktable.setRowCount(len(books))
            for row_idx, row_data in enumerate(books):
                for col_idx, col_data in enumerate(row_data):
                    self.booktable.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            conn.close()
        except sqlite3.Error as e:
            print("An error occurreddddd:", e)

    def filter_customers(self, text):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()

            query = f"SELECT * FROM customers WHERE Name LIKE '%{text}%' OR Gender LIKE '%{text}%' OR CustomerID LIKE '%{text}%'"
            c.execute(query)
            customers = c.fetchall()

            self.customertable.setRowCount(len(customers))
            for row_idx, row_data in enumerate(customers):
                for col_idx, col_data in enumerate(row_data):
                    self.customertable.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            conn.close()
        except sqlite3.Error as e:
            print("An error occurred:", e)

    def load_transactions(self):
        try:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()

            # Fetch data from rentals table
            c.execute('SELECT RentalDate, "Rented", Title, Name FROM rentals INNER JOIN books ON rentals.BookID = books.BookID INNER JOIN customers ON rentals.CustomerID = customers.CustomerID')
            rentals_data = c.fetchall()
            print("Rentals Data:", rentals_data)

            # Fetch data from returns table
            c.execute('SELECT ReturnDate, "Returned", Title, Name FROM returns INNER JOIN books ON returns.BookID = books.BookID INNER JOIN customers ON returns.CustomerID = customers.CustomerID')
            returns_data = c.fetchall()
            print("Returns Data:", returns_data)

            # Fetch data from reserve table
            c.execute('SELECT ReservationDate, "Reserved", Title, Name FROM reserve INNER JOIN books ON reserve.BookID = books.BookID INNER JOIN customers ON reserve.CustomerID = customers.CustomerID')
            reserve_data = c.fetchall()
            print("Reserve Data:", reserve_data)

            # Combine all data
            self.all_data = rentals_data + returns_data + reserve_data  # Store all data

            # Sort the data by date
            self.all_data.sort(key=lambda x: x[0])

            # Initially, display all data
            self.filter_transactions()

            conn.close()
        except sqlite3.Error as e:
            print("An error occurred:", e)
    
    def show_transaction_info_dialog(self,row, column):
        transaction_data = [self.ui.transactionstable.item(row, col).text() for col in range(self.ui.transactionstable.columnCount())]
    
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()

                if transaction_data[1] == "Rented" or transaction_data[1] == "Returned":
                    # Fetch book title and customer name
                    cursor.execute("SELECT books.Title, customers.Name FROM books INNER JOIN customers ON books.BookID = ? AND customers.CustomerID = ?", (transaction_data[2], transaction_data[3]))
                    book_customer_data = cursor.fetchone()
                    
                    if book_customer_data:
                        book_title, customer_name = book_customer_data
                        transaction_data[2] = book_title
                        transaction_data[3] = customer_name
                
                # Create the info dialog
                info_dialog = InfoDialog(transaction_data, 'transaction')
                info_dialog.exec()

        except sqlite3.Error as e:
            print("Error retrieving transaction information:", e)

    def filter_transactions(self):
        filter_text = self.ui.transactioncbox.currentText()

        if filter_text == "All":
            filtered_data = self.all_data
        elif filter_text == "Rentals":
            filtered_data = [data for data in self.all_data if data[1] == "Rented"]
        elif filter_text == "Returns":
            filtered_data = [data for data in self.all_data if data[1] == "Returned"]
        elif filter_text == "Reservations":
            filtered_data = [data for data in self.all_data if data[1] == "Reserved"]

        self.ui.transactionstable.setRowCount(len(filtered_data))
        for row_idx, row_data in enumerate(filtered_data):
            for col_idx, col_data in enumerate(row_data):
                self.ui.transactionstable.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            
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
            rental_fee_label = QtWidgets.QLabel(f"Rental Fee: {info[6]}")
            description_label = QtWidgets.QLabel(f"Description: {info[7]}")
            description_label.setWordWrap(True)  # Enable word wrapping for the description label

            book_info_layout.addWidget(title_label)
            book_info_layout.addWidget(author_label)
            book_info_layout.addWidget(category_label)
            book_info_layout.addWidget(status_label)
            book_info_layout.addWidget(rental_fee_label)
            book_info_layout.addWidget(description_label)

            if info[8]:
                cover_image_label = QtWidgets.QLabel()
                pixmap = QtGui.QPixmap(info[8])
                cover_image_label.setPixmap(pixmap.scaled(500, 500, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
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
                id_image_label.setPixmap(pixmap.scaled(500, 500, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                customer_info_layout.addWidget(id_image_label)

            layout.addLayout(customer_info_layout)

        elif info_type == 'transaction':
            transaction_info_layout = QtWidgets.QVBoxLayout()
            for item in info:
                label = QtWidgets.QLabel(item)
                transaction_info_layout.addWidget(label)

            # Fetch fees based on transaction type
            if info[1] == 'Rented' or info[1] == 'Returned':
                fee_type = 'RentalFee'
            elif info[1] == 'Reserved':
                fee_type = 'ReservationFee'

            try:
                with sqlite3.connect("library.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT {fee_type} FROM {'returns' if info[1] == 'Returned' else 'rentals' if info[1] == 'Rented' else 'reserve'} WHERE {'ReturnID' if info[1] == 'Returned' else 'RentalID' if info[1] == 'Rented' else 'ReserveID'} = ?", (info[0],))
                    fee = cursor.fetchone()
                    if fee:
                        fee_label = QtWidgets.QLabel(f"Fee: {fee[0]}")
                        transaction_info_layout.addWidget(fee_label)
            except sqlite3.Error as e:
                print("Error retrieving fee information:", e)

            layout.addLayout(transaction_info_layout)

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
