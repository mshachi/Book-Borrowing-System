import sys
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
    QFormLayout
)
from PyQt6.QtCore import Qt
import sqlite3

# Dialog for adding a new book
class AddBookDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Book")
        layout = QVBoxLayout(self)
        
        # Input fields for author, title, category, description, and fee
        self.author_input = QLineEdit(self)
        self.author_input.setPlaceholderText("Enter author")
        layout.addWidget(self.author_input)

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Enter title")
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Category:"))
        category_layout = QVBoxLayout()
        layout.addLayout(category_layout)

        categories = [
            "Action and Adventure",
            "Anthology",
            # Add more categories here...
        ]

        self.category_combo = QComboBox(self)
        self.category_combo.addItems(categories)
        category_layout.addWidget(self.category_combo)

        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("Enter description")
        layout.addWidget(self.description_input)
        
        self.fee_input = QLineEdit(self)
        self.fee_input.setPlaceholderText("Enter fee")
        layout.addWidget(self.fee_input)

        # Buttons for adding and canceling
        buttons = QDialogButtonBox()
        buttons.addButton("Add", QDialogButtonBox.ButtonRole.AcceptRole)
        buttons.addButton(QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    # Method to get the entered book information
    def get_book_info(self):
        author = self.author_input.text()
        title = self.title_input.text()
        category = self.category_combo.currentText()
        description = self.description_input.toPlainText()
        fee = float(self.fee_input.text())
        return author, title, category, description, fee

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

        self.number_input = QLineEdit(self)
        self.number_input.setPlaceholderText("Enter number")
        layout.addWidget(self.number_input)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Enter phone number")
        layout.addWidget(self.phone_input)

        self.valid_id_input = QLineEdit(self)
        self.valid_id_input.setPlaceholderText("Enter valid ID")
        layout.addWidget(self.valid_id_input)

        # Buttons for adding and canceling
        buttons = QDialogButtonBox()
        buttons.addButton("Add", QDialogButtonBox.ButtonRole.AcceptRole)
        buttons.addButton(QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

    # Method to get the entered customer information
    def get_customer_info(self):
        name = self.name_input.text()
        gender = self.gender_combo.currentText()
        number = self.number_input.text()
        phone_num = self.phone_input.text()
        valid_id = self.valid_id_input.text()
        return name, gender, number, phone_num, valid_id

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
            label = QLabel(key)
            form_layout.addRow(label, QLabel(str(value)))

        # Combo box for selecting a customer
        self.customer_combo = QComboBox(self)
        self.customer_combo.addItems(customers)
        form_layout.addRow("Select Customer:", self.customer_combo)

        layout.addLayout(form_layout)

        # Buttons for renting, returning, reserving, and canceling
        buttons = QDialogButtonBox()
        buttons.addButton("Rent", QDialogButtonBox.ButtonRole.AcceptRole)
        buttons.addButton("Return", QDialogButtonBox.ButtonRole.AcceptRole)
        buttons.addButton("Reserve", QDialogButtonBox.ButtonRole.AcceptRole)
        buttons.addButton(QDialogButtonBox.StandardButton.Cancel)
        layout.addWidget(buttons)

        buttons.accepted.connect(self.rent_book)
        buttons.rejected.connect(self.reject)

    # Method to handle renting a book
    def rent_book(self):
        selected_customer = self.customer_combo.currentText()
        if selected_customer:
            QMessageBox.information(self, "Rent", f"Renting book {self.book_info['Title']} to {selected_customer}.")
        else:
            QMessageBox.warning(self, "Warning", "Please select a customer.")

# Main application window
class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Book Borrowing System")
        self.setGeometry(100, 100, 500, 400)

        self.init_ui()

        self.load_books()
        self.load_customers()

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
        title_label = QLabel("Book Borrowing System - Books", self)
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
        filter_label = QLabel("Filter:", self)
        filter_layout.addWidget(filter_label)
        self.filter_input = QLineEdit(self)
        self.filter_input.setPlaceholderText("Enter keyword")
        self.filter_input.textChanged.connect(self.filter_books)
        filter_layout.addWidget(self.filter_input)

        self.filter_type_combo = QComboBox(self)
        self.filter_type_combo.addItems(["Title", "Author", "Category"])
        filter_layout.addWidget(self.filter_type_combo)

        book_tab_layout.addLayout(filter_layout)

        # List widget to display books
        self.books_list = QListWidget(self)
        book_tab_layout.addWidget(self.books_list)

        # Button for viewing more information about a book
        more_info_button = QPushButton("More Info", self)
        more_info_button.setToolTip("View detailed information about the selected book")
        more_info_button.clicked.connect(self.show_book_info)
        self.set_button_style(more_info_button)
        book_tab_layout.addWidget(more_info_button)

        # Tab for managing customers
        customer_tab = QWidget(self)
        tab_widget.addTab(customer_tab, "Customers")
        customer_tab_layout = QVBoxLayout(customer_tab)
        
        # Title label for customer tab
        title_label_customers = QLabel("Book Borrowing System - Customers", self)
        title_label_customers.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label_customers.setStyleSheet("font-size: 18pt; font-weight: bold;")
        customer_tab_layout.addWidget(title_label_customers)

        # Button for adding a new customer
        button_layout_customers = QHBoxLayout()
        add_customer_button = QPushButton("Add Customer", self)
        add_customer_button.setToolTip("Add a new customer to the library")
        add_customer_button.clicked.connect(self.show_add_customer_dialog)
        self.set_button_style(add_customer_button)
        button_layout_customers.addWidget(add_customer_button)
        customer_tab_layout.addLayout(button_layout_customers)

        # List widget to display customers
        self.customers_list = QListWidget(self)
        customer_tab_layout.addWidget(self.customers_list)

        self.init_database()

    # Method to initialize the database
    def init_database(self):
        self.connection = sqlite3.connect("library.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, author TEXT, title TEXT, category TEXT, description TEXT, fee REAL, available BOOLEAN)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, gender TEXT, number TEXT, phone_num TEXT, valid_id TEXT)"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS rentals (id INTEGER PRIMARY KEY, customer_id INTEGER, book_id INTEGER, FOREIGN KEY(customer_id) REFERENCES customers(id), FOREIGN KEY(book_id) REFERENCES books(id))"
        )  
        self.connection.commit()

    # Method to display the add book dialog
    def show_add_book_dialog(self):
        dialog = AddBookDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            author, title, category, description, fee = dialog.get_book_info()
            if author and title and category:
                self.cursor.execute("INSERT INTO books (author, title, category, description, fee, available) VALUES (?, ?, ?, ?, ?, ?)", (author, title, category, description, fee, True))
                self.connection.commit()
                self.load_books()
            else:
                QMessageBox.warning(self, "Warning", "Please fill in all fields.")

    # Method to display the add customer dialog
    def show_add_customer_dialog(self):
        dialog = AddCustomerDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, gender, number, phone_num, valid_id = dialog.get_customer_info()
            if name and gender and number and phone_num and valid_id:
                self.cursor.execute("INSERT INTO customers (name, gender, number, phone_num, valid_id) VALUES (?, ?, ?, ?, ?)", (name, gender, number, phone_num, valid_id))
                self.connection.commit()
                self.load_customers()
            else:
                QMessageBox.warning(self, "Warning", "Please fill in all fields for the customer.")

    # Method to load customers into the customers list
    def load_customers(self):
        self.customers_list.clear()
        self.cursor.execute("SELECT * FROM customers")
        customers = self.cursor.fetchall()
        for customer in customers:
            self.customers_list.addItem(f"{customer[0]}: {customer[1]}")

    # Method to load books into the books list
    def load_books(self):
        self.books_list.clear()
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        for book in books:
            status = "Available" if book[6] else "Borrowed"
            self.books_list.addItem(f"{book[0]}: {book[2]} by {book[1]} ({book[3]}) - Fee: {book[5]} - {status}")

    # Method to set the style for buttons
    def set_button_style(self, button):
        button.setStyleSheet("QPushButton { background-color: maroon; color: white; border: 2px solid gold; border-radius: 10px; padding: 5px; } QPushButton:hover { background-color: #800000; }")

    # Method to filter books based on user input
    def filter_books(self):
        text = self.filter_input.text()
        filter_type = self.filter_type_combo.currentText()
        if text:
            for i in range(self.books_list.count()):
                item = self.books_list.item(i)
                book_info = item.text()
                if filter_type == "Title":
                    if text.lower() not in book_info.split(":")[1].split("by")[0].strip().lower():
                        item.setHidden(True)
                    else:
                        item.setHidden(False)
                elif filter_type == "Author":
                    if text.lower() not in book_info.split("by")[1].split("(")[0].strip().lower():
                        item.setHidden(True)
                    else:
                        item.setHidden(False)
                elif filter_type == "Category":
                    if text.lower() not in book_info.split("(")[1].split(")")[0].strip().lower():
                        item.setHidden(True)
                    else:
                        item.setHidden(False)

    # Method to display detailed information about a book
    def show_book_info(self):
        selected_book = self.books_list.currentItem()
        if selected_book:
            book_id = int(selected_book.text().split(":")[0])
            self.cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            book_info = self.cursor.fetchone()
            if book_info:
                book_details = {
                    "ID": book_info[0],
                    "Title": book_info[2],
                    "Author": book_info[1],
                    "Category": book_info[3],
                    "Description": book_info[4],
                    "Fee": book_info[5],
                    "Status": "Available" if book_info[6] else "Borrowed"
                }
                self.show_rent_dialog(book_details)
        else:
            QMessageBox.warning(self, "Warning", "Please select a book to view details.")

    # Method to display the book info dialog
    def show_rent_dialog(self, book_details):
        self.rent_dialog = BookInfoDialog(book_details, self.get_customer_names())
        self.rent_dialog.accepted.connect(self.rent_book)
        self.rent_dialog.show()

    # Method to get the names of all customers
    def get_customer_names(self):
        customers = []
        self.cursor.execute("SELECT name FROM customers")
        for customer in self.cursor.fetchall():
            customers.append(customer[0])
        return customers

    # Method to handle renting a book
    def rent_book(self):
        selected_book = self.books_list.currentItem()
        if selected_book:
            book_id = int(selected_book.text().split(":")[0])
            selected_customer = self.rent_dialog.customer_combo.currentText()
            if selected_customer:
                self.cursor.execute("UPDATE books SET available = ? WHERE id = ?", (False, book_id))
                self.connection.commit()
                QMessageBox.information(self, "Rent", f"Book rented to {selected_customer}.")
                self.load_books()
            else:
                QMessageBox.warning(self, "Warning", "Please select a customer.")
        else:
            QMessageBox.warning(self, "Warning", "Please select a book to rent.")

def main():
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
