import sys
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
    QListWidget,
    QDialog,
    QComboBox,
    QTextEdit,
    QTabWidget,
    QDialogButtonBox,
    QFormLayout,
    QFileDialog, QCalendarWidget, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIcon, QPixmap
import sqlite3


# Dialog for adding a new book
class AddBookDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Book")
        layout = QVBoxLayout(self)

        # Input fields for author, title, category, description, and fee
        self.ISBN_input = QLineEdit(self)
        self.ISBN_input.setPlaceholderText("Enter ISBN code")
        layout.addWidget(self.ISBN_input)

        self.author_input = QLineEdit(self)
        self.author_input.setPlaceholderText("Enter author")
        layout.addWidget(self.author_input)

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Enter title")
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Category:"))
        category_layout = QVBoxLayout()
        layout.addLayout(category_layout)

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

        self.category_combo = QComboBox(self)
        self.category_combo.addItems(genres)
        category_layout.addWidget(self.category_combo)

        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("Enter description")
        layout.addWidget(self.description_input)

        self.fee_input = QLineEdit(self)
        self.fee_input.setPlaceholderText("Enter fee")
        layout.addWidget(self.fee_input)

        self.cover_image_button = QPushButton("Select Cover Image")
        self.cover_image_button.clicked.connect(self.select_cover_image)
        layout.addWidget(self.cover_image_button)

        self.cover_image_label = QLabel("No image selected")
        layout.addWidget(self.cover_image_label)

        # Buttons for adding and canceling
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    # Method to select an image for the book cover
    def select_cover_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Cover Image", "",
                                                   "Images (*.png *.xpm *.jpg);;All Files (*)")
        if file_name:
            self.cover_image_label.setText(file_name)

    # Method to get the entered book information
    def get_book_info(self):
        BookId = self.ISBN_input.text()
        Title = self.title_input.text()
        Author = self.author_input.text()
        Category = self.category_combo.currentText()
        Status = "Available"
        Description = self.description_input.toPlainText()
        Cover_image = self.cover_image_label.text()
        try:
            Rentalfee = float(self.fee_input.text())
        except ValueError:
            Rentalfee = 0.0
        return BookId, Author, Title, Category, Status, Description, Rentalfee, Cover_image


# Dialog for adding a new customer
class AddCustomerDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Customer")
        layout = QVBoxLayout(self)

        # Input fields for customer information
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter name")
        layout.addWidget(self.name_input)

        self.gender_combo = QComboBox(self)
        self.gender_combo.addItems(["Male", "Female", "Other"])
        layout.addWidget(self.gender_combo)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Enter phone number")
        layout.addWidget(self.phone_input)

        self.valid_id_button = QPushButton("Select Valid ID Image")
        self.valid_id_button.clicked.connect(self.select_valid_id_image)
        layout.addWidget(self.valid_id_button)

        self.valid_id_label = QLabel("No image selected")
        layout.addWidget(self.valid_id_label)

        # Buttons for adding and canceling
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    # Method to select an image for the valid ID
    def select_valid_id_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Valid ID Image", "",
                                                   "Images (*.png *.xpm *.jpg);;All Files (*)")
        if file_name:
            self.valid_id_label.setText(file_name)

    # Method to get the entered customer information
    def get_customer_info(self):
        CustomerId = self.generate_customer_id()
        Name = self.name_input.text()
        Gender = self.gender_combo.currentText()
        PhoneNumber = self.phone_input.text()
        ValidIdPath = self.valid_id_label.text()
        return CustomerId, Name, Gender, PhoneNumber, ValidIdPath

    def generate_customer_id(self):
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT CustomerId FROM customers ORDER BY CustomerId DESC LIMIT 1")
                result = cursor.fetchone()
                if result:
                    last_id = result[0]
                    # Extract the numeric part, increment it, and format back to Axx
                    numeric_part = int(last_id[1:])
                    new_numeric_part = numeric_part + 1
                    new_id = f"A{new_numeric_part:02d}"
                else:
                    # No existing IDs, start with A01
                    new_id = "A01"
                return new_id
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error generating customer ID: {e}")
            return None


# Dialog for displaying detailed book information
class BookInfoDialog(QDialog):
    def __init__(self, book_info, customers):
        super().__init__()
        self.setWindowTitle("Book Details")
        layout = QVBoxLayout(self)

        self.book_info = book_info

        # Form layout to display book details and customer selection
        form_layout = QFormLayout()

        for key, value in book_info.items():
            if key != "Cover Image":
                label = QLabel(key)
                form_layout.addRow(label, QLabel(str(value)))
            else:
                label = QLabel(key)
                image_label = QLabel(self)
                pixmap = QPixmap(value)
                image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
                form_layout.addRow(label, image_label)

        # Combo box for selecting a customer
        self.customer_combo = QComboBox(self)
        self.customer_combo.addItems(customers)
        form_layout.addRow("Select Customer:", self.customer_combo)

        layout.addLayout(form_layout)

        # Buttons for renting, returning, reserving, and canceling
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    # Method to handle renting a book
    def rent_book(self):
        selected_customer = self.customer_combo.currentText()
        if selected_customer:
            return selected_customer
        else:
            QMessageBox.warning(self, "Warning", "Please select a customer.")
            return None


# Dialog for displaying detailed customer information
class CustomerInfoDialog(QDialog):
    def __init__(self, customer_info):
        super().__init__()
        self.setWindowTitle("Customer Details")
        layout = QVBoxLayout(self)

        # Form layout to display customer details
        form_layout = QFormLayout()

        for key, value in customer_info.items():
            if key != "Valid ID":
                label = QLabel(key)
                form_layout.addRow(label, QLabel(str(value)))
            else:
                label = QLabel(key)
                image_label = QLabel(self)
                pixmap = QPixmap(value)
                image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
                form_layout.addRow(label, image_label)

        layout.addLayout(form_layout)

        # Buttons for closing the dialog
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)


# Dialog for displaying detailed book information and actions
class ActionDialog(QDialog):
    def __init__(self, book_info, bookId):
        super().__init__()
        self.setWindowTitle("Book Details and Actions")
        layout = QVBoxLayout(self)

        # Display book information
        form_layout = QFormLayout()
        for key, value in book_info.items():
            if key != "Cover Image":
                form_layout.addRow(QLabel(key), QLabel(str(value)))
            else:
                cover_image_label = QLabel(self)
                pixmap = QPixmap(value)
                cover_image_label.setPixmap(pixmap.scaled(100, 150, Qt.AspectRatioMode.KeepAspectRatio))
                form_layout.addRow(QLabel(key), cover_image_label)
        layout.addLayout(form_layout)

        # Buttons for actions
        button_layout = QHBoxLayout()

        rent_button = QPushButton("Rent")
        rent_button.clicked.connect(lambda: self.open_rent_dialog(bookId))  # Pass bookId here
        button_layout.addWidget(rent_button)

        return_button = QPushButton("Return")
        return_button.clicked.connect(self.open_return_dialog)
        button_layout.addWidget(return_button)

        reserve_button = QPushButton("Reserve")
        reserve_button.clicked.connect(self.open_reserve_dialog)
        button_layout.addWidget(reserve_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Store book information for later use
        self.book_info = book_info

    def open_rent_dialog(self, bookId):
        rent_dialog = RentDialog()
        if rent_dialog.exec() == QDialog.DialogCode.Accepted:
            customer_id, rental_date, due_date = rent_dialog.get_rent_info()

            # Assuming 'bookId' is available in the scope of this function
            # Calculate the number of days between rentalDate and rentalDueDate
            rental_date = datetime.strptime(rental_date, '%Y-%m-%d')
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
            days_between = (due_date - rental_date).days

            # You need to fetch the rental fee from the database based on the book ID
            # Replace 'rentalFee' with the actual way of fetching rental fee for the book
            rental_fee = self.get_rental_fee(bookId)

            # Calculates the final fee in terms of rent days
            final_rent_fee = days_between * rental_fee

            try:
                # Create connection to database
                conn = sqlite3.connect("library.db")
                c = conn.cursor()

                # Check if the book is available
                c.execute("SELECT Status FROM books WHERE BookId = ?", (bookId,))
                book_status = c.fetchone()
                if book_status is None:
                    QMessageBox.warning(self, "Error", "Book not found")
                    return
                if book_status[0] != 'Available':
                    QMessageBox.warning(self, "Error", "Book is not available")
                    return

                # Proceed to insert the rental record
                c.execute(
                    "INSERT INTO rentals (CustomerId, BookId, RentalDate, RentalDueDate, RentalFee) VALUES (?, ?, ?, ?, ?)",
                    (customer_id, bookId, rental_date, due_date, final_rent_fee))

                # Update the status of the book to 'rented'
                c.execute("UPDATE books SET Status = 'Rented' WHERE BookId = ?", (bookId,))

                conn.commit()
                conn.close()
                QMessageBox.information(self, "Rent Book", f"Rented by {customer_id} from {rental_date} to {due_date}")

            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Error renting book: {e}")

    def get_rental_fee(self, book_id):
        try:
            # Create connection to database
            conn = sqlite3.connect("library.db")
            c = conn.cursor()

            # Fetch the rental fee from the database based on the book ID
            c.execute("SELECT RentalFee FROM books WHERE BookId = ?", (book_id,))
            rental_fee = c.fetchone()[0]

            conn.close()
            return rental_fee

        except sqlite3.Error as e:
            print("Error fetching rental fee:", e)
            return None


    def open_return_dialog(self):
        return_dialog = ReturnDialog()
        if return_dialog.exec() == QDialog.DialogCode.Accepted:
            customer_id, return_date, overdue_fee = return_dialog.get_return_info()
            # Handle the return action with customer_id, return_date, overdue_fee
            QMessageBox.information(self, "Return Book", f"Returned by {customer_id} on {return_date} with overdue fee {overdue_fee}")

    def open_reserve_dialog(self):
        reserve_dialog = ReserveDialog()
        if reserve_dialog.exec() == QDialog.DialogCode.Accepted:
            customer_id, reservation_date, reservation_fee = reserve_dialog.get_reserve_info()
            # Handle the reserve action with customer_id, reservation_date, reservation_fee
            QMessageBox.information(self, "Reserve Book", f"Reserved by {customer_id} on {reservation_date} with reservation fee {reservation_fee}")


class RentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rent Book")
        layout = QVBoxLayout(self)

        self.customer_id_combobox = QComboBox(self)
        # Fetch names from the customer table in the database and add them as items to the combobox
        customer_names = self.get_customer_names()
        self.customer_id_combobox.addItems(customer_names)
        layout.addWidget(self.customer_id_combobox)

        self.rental_date_edit = QDateEdit(self)
        self.rental_date_edit.setCalendarPopup(True)
        self.rental_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.rental_date_edit.setDate(QDate.currentDate())  # Set initial date to today
        layout.addWidget(self.rental_date_edit)

        self.due_date_edit = QDateEdit(self)
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.due_date_edit.setDate(QDate.currentDate())  # Set initial date to today
        layout.addWidget(self.due_date_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    def get_rent_info(self):
        customer_id = self.customer_id_combobox.currentText()
        rental_date = self.rental_date_edit.date().toString("yyyy-MM-dd")
        due_date = self.due_date_edit.date().toString("yyyy-MM-dd")
        return customer_id, rental_date, due_date

    def get_customer_names(self):
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()

            # Execute a query to fetch names of customers from the customer table
            cursor.execute("SELECT Name FROM customers")

            # Fetch all the names from the query result
            customer_names = [row[0] for row in cursor.fetchall()]

            # Close the cursor and connection
            cursor.close()
            conn.close()

            return customer_names

        except sqlite3.Error as e:
            print("Error fetching customer names:", e)
            return []




class ReturnDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Return Book")
        layout = QVBoxLayout(self)

        self.customer_id_input = QLineEdit(self)
        self.customer_id_input.setPlaceholderText("Enter Customer ID")
        layout.addWidget(self.customer_id_input)

        self.return_date_input = QLineEdit(self)
        self.return_date_input.setPlaceholderText("Enter Return Date")
        layout.addWidget(self.return_date_input)

        self.overdue_fee_input = QLineEdit(self)
        self.overdue_fee_input.setPlaceholderText("Enter Overdue Fee")
        layout.addWidget(self.overdue_fee_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    def get_return_info(self):
        return self.customer_id_input.text(), self.return_date_input.text(), self.overdue_fee_input.text()


class ReserveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reserve Book")
        layout = QVBoxLayout(self)

        self.customer_id_input = QLineEdit(self)
        self.customer_id_input.setPlaceholderText("Enter Customer ID")
        layout.addWidget(self.customer_id_input)

        self.reservation_date_input = QLineEdit(self)
        self.reservation_date_input.setPlaceholderText("Enter Reservation Date")
        layout.addWidget(self.reservation_date_input)

        self.reservation_fee_input = QLineEdit(self)
        self.reservation_fee_input.setPlaceholderText("Enter Reservation Fee")
        layout.addWidget(self.reservation_fee_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    def get_reserve_info(self):
        return self.customer_id_input.text(), self.reservation_date_input.text(), self.reservation_fee_input.text()



# Main application window
class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Book Rental System")
        self.setGeometry(100, 100, 500, 400)
        self.setWindowIcon(QIcon('icon.png'))  # Optional: Set an application icon

        self.init_ui()
        self.init_database()

        self.load_books()
        self.load_customers()

    def init_database(self):
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS customers
                         (CustomerId TEXT PRIMARY KEY,
                          Name TEXT,
                          Gender TEXT,
                          PhoneNumber TEXT,
                          ValidIdPath)''')
        c.execute('''CREATE TABLE IF NOT EXISTS books
                        (BookId TEXT PRIMARY KEY,
                         Title TEXT,
                         Author TEXT, 
                         Category TEXT,
                         Status TEXT,
                         RentalFee INTEGER, 
                         Description TEXT,
                         Cover_Image TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS rentals
                        (CustomerId TEXT,
                         BookId TEXT,
                         RentalDate TEXT,
                         RentalDueDate TEXT,
                         RentalFee INTEGER,
                         FOREIGN KEY (CustomerId) REFERENCES customers(CustomerId),
                         FOREIGN KEY (BookId) REFERENCES books(BookId))''')

        c.execute('''CREATE TABLE IF NOT EXISTS returns
                        (CustomerId TEXT,
                         BookId TEXT,
                         ReturnDate TEXT,
                         RentalDueDate TEXT,
                         OverdueFee INTEGER,
                         FOREIGN KEY (CustomerId) REFERENCES customers(CustomerId),
                         FOREIGN KEY (BookId) REFERENCES books(BookId),
                         FOREIGN KEY (RentalDueDate) REFERENCES rentals(RentalDueDate))''')

        c.execute('''CREATE TABLE IF NOT EXISTS reserve
                        (CustomerId TEXT,
                         BookId TEXT,
                         ReservationDate TEXT,
                         ReservationFee REAL,
                         FOREIGN KEY (CustomerId) REFERENCES customers(CustomerId),
                         FOREIGN KEY (BookId) REFERENCES books(BookId))''')

        conn.commit()
        conn.close()


    # Method to initialize the UI
    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Tab widget to manage books and customers
        tab_widget = QTabWidget(self)
        layout.addWidget(tab_widget)

        # Tab for managing books
        book_tab = QWidget(self)
        tab_widget.addTab(book_tab, "Books")
        book_tab_layout = QVBoxLayout(book_tab)

        # Title label for book tab
        title_label = QLabel("Book Rental System - Books", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        book_tab_layout.addWidget(title_label)

        # Button for adding a new book
        button_layout = QHBoxLayout()
        add_book_button = QPushButton("Add Book", self)
        add_book_button.setToolTip("Add a new book to the library")
        add_book_button.clicked.connect(self.show_add_book_dialog)
        self.set_button_style(add_book_button)
        button_layout.addWidget(add_book_button)
        book_tab_layout.addLayout(button_layout)

        # Filter input for searching books
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter books by:", self)
        filter_layout.addWidget(filter_label)
        self.filter_type_combo = QComboBox(self)
        self.filter_type_combo.addItems(["Title", "Author", "Category"])
        filter_layout.addWidget(self.filter_type_combo)
        self.filter_input = QLineEdit(self)
        self.filter_input.setPlaceholderText("Enter filter text")
        filter_layout.addWidget(self.filter_input)
        filter_button = QPushButton("Filter", self)
        filter_button.clicked.connect(self.filter_books)
        filter_layout.addWidget(filter_button)
        book_tab_layout.addLayout(filter_layout)

        # List to display books
        self.books_list = QListWidget(self)
        book_tab_layout.addWidget(self.books_list)

        # Tab for managing customers
        customer_tab = QWidget(self)
        tab_widget.addTab(customer_tab, "Customers")
        customer_tab_layout = QVBoxLayout(customer_tab)

        # Title label for customer tab
        title_label = QLabel("Book Rental System - Customers", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        customer_tab_layout.addWidget(title_label)

        # Button for adding a new customer
        button_layout = QHBoxLayout()
        add_customer_button = QPushButton("Add Customer", self)
        add_customer_button.setToolTip("Add a new customer to the system")
        add_customer_button.clicked.connect(self.show_add_customer_dialog)
        self.set_button_style(add_customer_button)
        button_layout.addWidget(add_customer_button)
        customer_tab_layout.addLayout(button_layout)

        # Filter input for searching customers
        filter_layout = QHBoxLayout()
        filter_label = QLabel("Filter customers by:", self)
        filter_layout.addWidget(filter_label)
        self.filter_customer_type_combo = QComboBox(self)
        self.filter_customer_type_combo.addItems(["Name", "Number"])
        filter_layout.addWidget(self.filter_customer_type_combo)
        self.filter_customer_input = QLineEdit(self)
        self.filter_customer_input.setPlaceholderText("Enter filter text")
        filter_layout.addWidget(self.filter_customer_input)
        filter_button = QPushButton("Filter", self)
        filter_button.clicked.connect(self.filter_customers)
        filter_layout.addWidget(filter_button)
        customer_tab_layout.addLayout(filter_layout)

        # List to display customers
        self.customers_list = QListWidget(self)
        customer_tab_layout.addWidget(self.customers_list)

        # Buttons for viewing more info and action button
        books_button_layout = QHBoxLayout()
        book_tab_layout.addLayout(books_button_layout)
        more_info_button = QPushButton("More Info", self)
        more_info_button.setToolTip("View more information about the selected book")
        more_info_button.clicked.connect(self.show_book_info)
        self.set_button_style(more_info_button)
        books_button_layout.addWidget(more_info_button)

        action_button = QPushButton("Action", self)
        action_button.setToolTip("Perform an action on the selected book")
        action_button.clicked.connect(self.show_book_info_action)
        self.set_button_style(action_button)
        books_button_layout.addWidget(action_button)

    def show_action_dialog(self):
        # Assuming book_info is passed as a dictionary containing book information
        book_info = {}  # Populate book_info with relevant information
        dialog = ActionDialog(book_info)
        dialog.exec()

    # Method to set consistent style for buttons
    def set_button_style(self, button):
        button.setStyleSheet("font-size: 14pt; padding: 10px;")

    # Method to show the dialog for adding a new book
    def show_add_book_dialog(self):
        dialog = AddBookDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            book_info = dialog.get_book_info()
            self.add_book_to_db(book_info)
            self.load_books()

    # Method to show the dialog for adding a new customer
    def show_add_customer_dialog(self):
        dialog = AddCustomerDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            customer_info = dialog.get_customer_info()
            self.add_customer_to_db(customer_info)
            self.load_customers()

    # Method to filter books based on user input
    def filter_books(self):
        filter_type = self.filter_type_combo.currentText().lower()
        filter_text = self.filter_input.text()
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM books WHERE {filter_type} LIKE ?", (f"%{filter_text}%",))
                books = cursor.fetchall()
                self.books_list.clear()
                for book in books:
                    self.books_list.addItem(f"{book[1]}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error filtering books: {e}")

    # Method to filter customers based on user input
    def filter_customers(self):
        filter_type = self.filter_customer_type_combo.currentText().lower()
        filter_text = self.filter_customer_input.text()
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM customers WHERE {filter_type} LIKE ?", (f"%{filter_text}%",))
                customers = cursor.fetchall()
                self.customers_list.clear()
                for customer in customers:
                    self.customers_list.addItem(f"{customer[1]} ({customer[2]})")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error filtering customers: {e}")

    # Method to show detailed information about a selected book
    def show_book_info(self):
        selected_items = self.books_list.selectedItems()
        if selected_items:
            selected_book = selected_items[0].text()
            try:
                with sqlite3.connect("library.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM books WHERE title = ?", (selected_book.split(' by ')[0],))
                    book = cursor.fetchone()
                    book_info = {
                        "ISBN Code": book[0],
                        "Title": book[1],
                        "Author": book[2],
                        "Category": book[3],
                        "Status": book[4],
                        "Fee": book[5],
                        "Description": book[6],
                        "Cover Image": book[7]
                    }
                    cursor.execute("SELECT Name FROM customers")
                    customers = [row[0] for row in cursor.fetchall()]
                    dialog = BookInfoDialog(book_info, customers)
                    if dialog.exec() == QDialog.DialogCode.Accepted:
                        customer = dialog.rent_book()
                        if customer:
                            cursor.execute("UPDATE books SET rented_to = ? WHERE title = ?", (customer, book[2]))
                            conn.commit()
                            self.load_books()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Error fetching book details: {e}")

    def show_book_info_action(self):
        selected_items = self.books_list.selectedItems()
        if not selected_items:
            return
        selected_book = selected_items[0].text()
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM books WHERE title = ?", (selected_book.split(' by ')[0],))
                book = cursor.fetchone()
                book_info = {
                    "ISBN Code": book[0],
                    "Title": book[1],
                    "Author": book[2],
                    "Category": book[3],
                    "Status": book[4],
                    "Fee": book[5],
                    "Description": book[6],
                    "Cover Image": book[7]
                }
                cursor.execute("SELECT Name FROM customers")
                customers = [row[0] for row in cursor.fetchall()]
                dialog = ActionDialog(book_info, book[0])
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    customer = dialog.get_rental_fee(book[0])
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error fetching book details: {e}")


# Method to show detailed information about a selected customer
    def show_customer_info(self):
        selected_items = self.customers_list.selectedItems()
        if selected_items:
            selected_customer = selected_items[0].text()
            try:
                with sqlite3.connect("library.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM customers WHERE name = ?", (selected_customer.split(' (')[0],))
                    customer = cursor.fetchone()
                    customer_info = {
                        "Name": customer[1],
                        "Gender": customer[2],
                        "Number": customer[3],
                        "Phone Number": customer[4],
                        "Valid ID": customer[5]
                    }
                    dialog = CustomerInfoDialog(customer_info)
                    dialog.exec()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Error fetching customer details: {e}")

    # Method to load books from the database
    def load_books(self):
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM books")
                books = cursor.fetchall()
                self.books_list.clear()
                for book in books:
                    self.books_list.addItem(f"{book[1]}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error loading books: {e}")

    # Method to load customers from the database
    def load_customers(self):
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM customers")
                customers = cursor.fetchall()
                self.customers_list.clear()
                for customer in customers:
                    self.customers_list.addItem(f"{customer[1]} ({customer[3]})")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error loading customers: {e}")

    # Method to add a new book to the database
    def add_book_to_db(self, book_info):
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO books (BookId, Title, Author, Category, Status, RentalFee, Description, Cover_Image) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    book_info)
                conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error adding book: {e}")

    # Method to add a new customer to the database
    def add_customer_to_db(self, customer_info):
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO customers (CustomerId, Name, Gender, PhoneNumber, ValidIdPath) VALUES (?, ?, ?, ?, ?)",
                    customer_info)
                conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error adding customer: {e}")

    # Method to remove a selected book from the database
    def remove_book(self):
        selected_items = self.books_list.selectedItems()
        if selected_items:
            selected_book = selected_items[0].text()
            try:
                with sqlite3.connect("library.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM books WHERE title = ?", (selected_book.split(' by ')[0],))
                    conn.commit()
                    self.load_books()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Error removing book: {e}")

    # Method to remove a selected customer from the database
    def remove_customer(self):
        selected_items = self.customers_list.selectedItems()
        if selected_items:
            selected_customer = selected_items[0].text()
            try:
                with sqlite3.connect("library.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM customers WHERE name = ?", (selected_customer.split(' (')[0],))
                    conn.commit()
                    self.load_customers()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"Error removing customer: {e}")


# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec())
