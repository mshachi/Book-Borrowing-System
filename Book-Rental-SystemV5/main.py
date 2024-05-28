import sqlite3
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon


from PyQt6.QtCore import QDate, QTimer
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
        self.dialog = self
        super().__init__()

        try:
            # Initialize the UI from a separate UI file
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

            self.status_update_timer = QTimer()

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
            self.transactionssearch.textChanged.connect(self.filter_transactions)
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

            
            # Set up a timer to run the update_book_statuses function every day (86400000 ms = 24 hours)
            self.status_update_timer = QTimer(self)
            self.status_update_timer.timeout.connect(self.update_book_reservations)
            try:
                self.status_update_timer.start(86400000)  # 24 hours in milliseconds
            except Exception as e:
                print("Error nasad  diri: ",e)

            # Initialize the UI
            self.show_home()

            # Initialize the database
            self.init_database()

            try:
                # Load books and customers
                self.load_books()
                self.load_customers()
                self.load_transactions()
        
                #self.insert_dummy_books()
                #self.insert_dummy_customers()
            except Exception as e:
                print("ERROR DITO PO: ",e)
            
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
                self.load_books()
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
        book_id_item = self.booktable.item(selected_row, 0)         
        book_status_item = self.booktable.item(selected_row,5) 
        book_status = book_status_item.text()
        if book_id_item:
            if book_status == "Rented" or "Reserved":
                QMessageBox.critical(self, "Book can't be deleted", f"The book is still being rented/reserved")
                return
            
            book_id = book_id_item.text()
            confirmation_dialog = ConfirmationDialog("Are you sure you want to delete this book?")
            if confirmation_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                self.delete_book_from_db(book_id)
                self.load_books()
                self.load_transactions()

    def delete_customer_confirmation(self):
        selected_row = self.customertable.currentRow()
        customer_id_item = self.customertable.item(selected_row, 0)  
        if customer_id_item:
            customer_id = customer_id_item.text()
            confirmation_dialog = ConfirmationDialog("Are you sure you want to delete this customer?")
            if confirmation_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                self.delete_customer_from_db(customer_id)
                self.load_customers()
                self.load_transactions()

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

    def update_book_reservations(self):
        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            # Get the current date (for testing purposes)
            # Comment this line for real usage
            #specific_date = QtCore.QDate(2024, 6, 6)
            #current_date = specific_date.toString(QtCore.Qt.DateFormat.ISODate)

            # Uncomment this line for real usage
            current_date = QtCore.QDate.currentDate().toString(QtCore.Qt.DateFormat.ISODate)

            # Fetch all reservations where the reservation date is less than the current date
            cursor.execute("""
                SELECT r.BookId, b.Status
                FROM reserve r
                JOIN books b ON r.BookId = b.BookID
                WHERE r.ReservationDate < ?
            """, (current_date,))

            expired_reservations = cursor.fetchall()

            # Update the status of each expired reserved book to 'Available'
            for book_id, status in expired_reservations:
                if status == 'Reserved':
                    cursor.execute("UPDATE books SET Status = 'Available' WHERE BookID = ?", (book_id,))

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print("Error updating book statuses:", e)


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
            
            query = f"SELECT * FROM customers WHERE Name LIKE '%{text}%' OR Gender LIKE '%{text}%' OR CustomerID LIKE '%{text}%' OR "
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

    def insert_dummy_customers(self):
        print("ITS WORKING")
        data = [
            {"Name": "John Doe", "Gender": "Male", "PhoneNumber": "123-456-7890",
             "ValidIdPath": "No Id"},
            {"Name": "Jane Smith", "Gender": "Female", "PhoneNumber": "987-654-3210",
             "ValidIdPath": "No Id"},
            {"Name": "Michael Johnson", "Gender": "Male", "PhoneNumber": "456-789-0123",
             "ValidIdPath": "No Id"},
            {"Name": "Emily Davis", "Gender": "Female", "PhoneNumber": "789-012-3456",
             "ValidIdPath": "No Id"},
            {"Name": "Robert Brown", "Gender": "Male", "PhoneNumber": "234-567-8901",
             "ValidIdPath": "No Id"},
            {"Name": "Amanda Wilson", "Gender": "Female", "PhoneNumber": "901-234-5678",
             "ValidIdPath": "No Id"},
            {"Name": "William Martinez", "Gender": "Male", "PhoneNumber": "345-678-9012",
             "ValidIdPath": "No Id"},
            {"Name": "Jessica Taylor", "Gender": "Female", "PhoneNumber": "678-901-2345",
             "ValidIdPath": "No Id"},
            {"Name": "Daniel Anderson", "Gender": "Male", "PhoneNumber": "012-345-6789",
             "ValidIdPath": "No Id"},
            {"Name": "Sarah Miller", "Gender": "Female", "PhoneNumber": "567-890-1234",
             "ValidIdPath": "No Id"},
            {"Name": "Christopher Lee", "Gender": "Male", "PhoneNumber": "890-123-4567",
             "ValidIdPath": "No Id"},
            {"Name": "Megan Garcia", "Gender": "Female", "PhoneNumber": "345-678-9012",
             "ValidIdPath": "No Id"},
            {"Name": "Josephine Clark", "Gender": "Female", "PhoneNumber": "901-234-5678",
             "ValidIdPath": "No Id"},
            {"Name": "Andrew Young", "Gender": "Male", "PhoneNumber": "234-567-8901",
             "ValidIdPath": "No Id"},
            {"Name": "Lauren Lopez", "Gender": "Female", "PhoneNumber": "789-012-3456",
             "ValidIdPath": "No Id"},
            {"Name": "Justin Hall", "Gender": "Male", "PhoneNumber": "456-789-0123",
             "ValidIdPath": "No Id"},
            {"Name": "Rebecca Scott", "Gender": "Female", "PhoneNumber": "123-456-7890",
             "ValidIdPath": "No Id"},
            {"Name": "Tyler Adams", "Gender": "Male", "PhoneNumber": "987-654-3210",
             "ValidIdPath": "No Id"},
            {"Name": "Hannah Baker", "Gender": "Female", "PhoneNumber": "654-321-0987",
             "ValidIdPath": "No Id"},
            {"Name": "Brandon Thomas", "Gender": "Male", "PhoneNumber": "321-098-7654",
             "ValidIdPath": "No Id"}
        ]

        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            for customer in data:
                cursor.execute(
                    "INSERT OR IGNORE INTO customers (Name, Gender, PhoneNumber, ValidIdPath) VALUES (?, ?, ?, ?)",
                    (customer["Name"], customer["Gender"], customer["PhoneNumber"],
                     customer["ValidIdPath"]))

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print("Error:", e)  # Print the error
            QMessageBox.critical(None, "Database Error", f"An error occurred: {e}")

    def insert_dummy_books(self):
        data = [
            {"BookID": 1, "ISBN": "978-3-16-148410-0", "Title": "The Great Adventure", "Author": "John Smith",
             "Category": "Adventure", "Status": "Available", "RentalFee": 10.99,
             "Description": "Epic journey through unknown lands", "Cover_Image": "No cover image"},
            {"BookID": 2, "ISBN": "978-0-12-345678-9", "Title": "Mystery of the Old House", "Author": "Jane Doe",
             "Category": "Mystery", "Status": "Available", "RentalFee": 9.99,
             "Description": "Intriguing plot set in a haunted mansion", "Cover_Image": "No cover image"},
            {"BookID": 3, "ISBN": "978-1-23-456789-0", "Title": "Science Fiction Stories", "Author": "Albert Newman",
             "Category": "Science Fiction", "Status": "Available", "RentalFee": 12.99,
             "Description": "Visions of the future and beyond", "Cover_Image": "No cover image"},
            {"BookID": 4, "ISBN": "978-2-98-765432-1", "Title": "Learning Python", "Author": "Emily Clark",
             "Category": "Education", "Status": "Available", "RentalFee": 15.99,
             "Description": "Your guide to mastering Python programming", "Cover_Image": "No cover image"},
            {"BookID": 5, "ISBN": "978-3-01-234567-8", "Title": "Historical Tales", "Author": "George Brown",
             "Category": "Historical Fiction", "Status": "Available", "RentalFee": 11.99,
             "Description": "Journeys to the past filled with adventure", "Cover_Image": "No cover image"},
            {"BookID": 6, "ISBN": "978-4-01-234567-8", "Title": "Culinary Arts", "Author": "Hannah Lee",
             "Category": "Cookbooks", "Status": "Available", "RentalFee": 13.99,
             "Description": "Delicious recipes from around the world", "Cover_Image": "No cover image"},
            {"BookID": 7, "ISBN": "978-5-01-234567-8", "Title": "The Horror Night", "Author": "Irene Green",
             "Category": "Horror", "Status": "Available", "RentalFee": 14.99,
             "Description": "A spine-chilling journey into darkness", "Cover_Image": "No cover image"},
            {"BookID": 8, "ISBN": "978-6-01-234567-8", "Title": "Romantic Evenings", "Author": "Jack White",
             "Category": "Romance", "Status": "Available", "RentalFee": 10.49,
             "Description": "Love stories that warm the heart", "Cover_Image": "No cover image"},
            {"BookID": 9, "ISBN": "978-7-01-234567-8", "Title": "Comedy Kings", "Author": "Kelly Black",
             "Category": "Comedy", "Status": "Available", "RentalFee": 9.49,
             "Description": "Laughs and giggles guaranteed", "Cover_Image": "No cover image"},
            {"BookID": 10, "ISBN": "978-8-01-234567-8", "Title": "Epic Battles", "Author": "Liam Gray",
             "Category": "Epic", "Status": "Available", "RentalFee": 13.49,
             "Description": "Legendary clashes of heroes and villains", "Cover_Image": "No cover image"},
            {"BookID": 11, "ISBN": "978-9-01-234567-8", "Title": "Biography of Famous People", "Author": "Maria Brown",
             "Category": "Biography", "Status": "Available", "RentalFee": 14.49,
             "Description": "The lives of the extraordinary", "Cover_Image": "No cover image"},
            {"BookID": 12, "ISBN": "978-10-01-234567-8", "Title": "Economics for Beginners", "Author": "Nathan Green",
             "Category": "Economics", "Status": "Available", "RentalFee": 11.49,
             "Description": "Understanding the basics of economy", "Cover_Image": "No cover image"},
            {"BookID": 13, "ISBN": "978-11-01-234567-8", "Title": "Children's Fairy Tales", "Author": "Olivia White",
             "Category": "Children's", "Status": "Available", "RentalFee": 8.49,
             "Description": "Magical stories for young hearts", "Cover_Image": "No cover image"},
            {"BookID": 14, "ISBN": "978-12-01-234567-8", "Title": "Graphic Novels Collection", "Author": "Paul Smith",
             "Category": "Graphic Novels", "Status": "Available", "RentalFee": 16.49,
             "Description": "Artistic storytelling in images", "Cover_Image": "No cover image"},
            {"BookID": 15, "ISBN": "978-13-01-234567-8", "Title": "Folklore Legends", "Author": "Quincy Johnson",
             "Category": "Folklore", "Status": "Available", "RentalFee": 9.49,
             "Description": "Tales passed down through generations", "Cover_Image": "No cover image"},
            {"BookID": 16, "ISBN": "978-14-01-234567-8", "Title": "Classics Reimagined", "Author": "Rachel Brown",
             "Category": "Classics", "Status": "Available", "RentalFee": 12.49,
             "Description": "Reinterpretations of timeless classics", "Cover_Image": "No cover image"},
            {"BookID": 17, "ISBN": "978-15-01-234567-8", "Title": "Dystopian Future", "Author": "Steven Davis",
             "Category": "Dystopian", "Status": "Available", "RentalFee": 14.49,
             "Description": "Glimpses into bleak futures", "Cover_Image": "No cover image"}
        ]

        try:
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            for item in data:
                cursor.execute('''
                        INSERT OR IGNORE INTO books (BookID, ISBN, Title, Author, Category, Status, RentalFee, Description, Cover_Image)
                        VALUES (?, ?, ?, ?, ?, ?, ?,?, ?)
                    ''', (item["BookID"], item["ISBN"], item["Title"], item["Author"], item["Category"],
                          item["Status"], item["RentalFee"], item["Description"], item["Cover_Image"]))

            conn.commit()
            conn.close()

            
        except sqlite3.Error as e:
            QMessageBox.critical(self.dialog, "Database Error", f"An error occurred: {e}")

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

            if info[5] == "Reserved":
                conn = sqlite3.connect('library.db')
                c = conn.cursor()
                c.execute('SELECT reserve.ReservationDate FROM books JOIN reserve ON books.BookID = reserve.BookID;')
                reservationdate = c.fetchall()
                reservationdate_label = QtWidgets.QLabel(f"Reservation Date:{reservationdate}")
                
                book_info_layout.addWidget(reservationdate_label)

            if info[5] == "Rented":
                conn = sqlite3.connect('library.db')
                c = conn.cursor()
                c.execute('SELECT rentals.RentalDate, rentals.RentalDueDate FROM books JOIN rentals ON books.BookID = rentals.BookID ORDER BY RentalID DESC LIMIT 1;')
                rental_info = c.fetchone()
                if rental_info:
                    rentdate, rentdue = rental_info
                    rentdate_label = QtWidgets.QLabel(f"Rent Start Date: {rentdate}")
                    rentdue_label = QtWidgets.QLabel(f"Rent Due Date: {rentdue}")
                    book_info_layout.addWidget(rentdate_label)
                    book_info_layout.addWidget(rentdue_label)
                                               
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
        # ...

        elif info_type == 'transaction':
            transaction_info_layout = QtWidgets.QFormLayout()
            field_labels = ["Date", "Type", "Title", "Name"]  # Labels for the fields
            for label, data in zip(field_labels, info):
                transaction_info_layout.addRow(label, QtWidgets.QLabel(data))
            
            # Create a connection to the database
            conn = sqlite3.connect("library.db")
            c = conn.cursor()

            # Execute the SQL queries
            c.execute('SELECT rentalfee FROM rentals WHERE RentalDate = ?', (info[0],))
            rental_fee_result = c.fetchone()
            if rental_fee_result:
                rental_fee = rental_fee_result[0]
                transaction_info_layout.addRow("Rental Fee:", QtWidgets.QLabel(str(rental_fee)))
            
            c.execute('SELECT overduefee FROM returns WHERE ReturnDate = ?', (info[0],))
            overdue_fee_result = c.fetchone()
            if overdue_fee_result:
                overdue_fee = overdue_fee_result[0]
                transaction_info_layout.addRow("Overdue Fee:", QtWidgets.QLabel(str(overdue_fee)))
            
            c.execute('SELECT reservationfee FROM reserve WHERE reservationdate = ?', (info[0],))
            reservation_fee_result = c.fetchone()
            if reservation_fee_result:
                reservation_fee = reservation_fee_result[0]
                transaction_info_layout.addRow("Reservation Fee:", QtWidgets.QLabel(str(reservation_fee)))
            
            # Close the connection
            conn.close()

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
