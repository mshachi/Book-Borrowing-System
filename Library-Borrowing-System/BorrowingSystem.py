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
    QTextEdit
)
from PyQt6.QtCore import Qt
import sqlite3

# Dialog for adding a new book
class AddBookDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Book")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Input fields for author, title, and category
        self.author_input = QLineEdit(self)
        self.author_input.setPlaceholderText("Enter author")
        layout.addWidget(self.author_input)

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText("Enter title")
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Category:"))

        # Combo box for selecting category
        category_layout = QVBoxLayout()
        layout.addLayout(category_layout)

        categories = [
            "Action and Adventure",
            "Anthology",
            # More categories...
        ]

        self.category_combo = QComboBox(self)
        self.category_combo.addItems(categories)
        category_layout.addWidget(self.category_combo)

        # Input field for description
        self.description_input = QTextEdit(self)
        self.description_input.setPlaceholderText("Enter description")
        layout.addWidget(self.description_input)

        # Button for adding the book
        add_button = QPushButton("Add", self)
        add_button.clicked.connect(self.accept)
        layout.addWidget(add_button)

    # Method to get the entered book information
    def get_book_info(self):
        author = self.author_input.text()
        title = self.title_input.text()
        category = self.category_combo.currentText()
        description = self.description_input.toPlainText()
        return author, title, category, description

# Dialog for displaying detailed book information
class BookInfoDialog(QDialog):
    def __init__(self, book_info):
        super().__init__()
        self.setWindowTitle("Book Details")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Display book information
        for key, value in book_info.items():
            label = QLabel(f"{key}: {value}", self)
            layout.addWidget(label)

# Main application window
class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Book Borrowing System")
        self.setGeometry(100, 100, 500, 400)

        self.init_ui()

        # Load books from the database
        self.load_books()

    def init_ui(self):
        # Create central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Title label
        title_label = QLabel("Book Borrowing System", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(title_label)

        # Button layout for add, borrow, return, and delete buttons
        button_layout = QHBoxLayout()
        buttons = [
            ("Add Book", "Add a new book to the library", self.show_add_book_dialog),
            ("Borrow Book", "Borrow the selected book", self.borrow_book),
            ("Return Book", "Return the selected book", self.return_book),
            ("Delete Book", "Delete the selected book", self.delete_book)
        ]

        for button_data in buttons:
            button = QPushButton(button_data[0], self)
            button.setToolTip(button_data[1])
            button.clicked.connect(button_data[2])
            self.set_button_style(button)
            button_layout.addWidget(button)

        layout.addLayout(button_layout)

        # Filter layout
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

        layout.addLayout(filter_layout)

        # List widget to display books
        self.books_list = QListWidget(self)
        layout.addWidget(self.books_list)

        # Button for displaying detailed book information
        more_info_button = QPushButton("More Info", self)
        more_info_button.setToolTip("View detailed information about the selected book")
        more_info_button.clicked.connect(self.show_book_info)
        self.set_button_style(more_info_button)
        layout.addWidget(more_info_button)

        # Initialize database
        self.init_database()

    # Method to initialize the database
    def init_database(self):
        self.connection = sqlite3.connect("library.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, author TEXT, title TEXT, category TEXT, description TEXT, available BOOLEAN)"
        )
        self.connection.commit()

    # Method to display the dialog for adding a new book
    def show_add_book_dialog(self):
        dialog = AddBookDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            author, title, category, description = dialog.get_book_info()
            if author and title and category:
                self.cursor.execute("INSERT INTO books (author, title, category, description, available) VALUES (?, ?, ?, ?, ?)", (author, title, category, description, True))
                self.connection.commit()
                self.load_books()
            else:
                QMessageBox.warning(self, "Warning", "Please fill in all fields.")

    # Method to borrow a book
    def borrow_book(self):
        selected_book = self.books_list.currentItem()
        if selected_book:
            book_id = int(selected_book.text().split(":")[0])
            self.cursor.execute("UPDATE books SET available = ? WHERE id = ?", (False, book_id))
            self.connection.commit()
            self.load_books()
        else:
            QMessageBox.warning(self, "Warning", "Please select a book to borrow.")

    # Method to return a borrowed book
    def return_book(self):
        selected_book = self.books_list.currentItem()
        if selected_book:
            book_id = int(selected_book.text().split(":")[0])
            self.cursor.execute("UPDATE books SET available = ? WHERE id = ?", (True, book_id))
            self.connection.commit()
            self.load_books()
        else:
            QMessageBox.warning(self, "Warning", "Please select a book to return.")

    # Method to delete a book
    def delete_book(self):
        selected_book = self.books_list.currentItem()
        if selected_book:
            book_id = int(selected_book.text().split(":")[0])
            self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            self.connection.commit()
            self.load_books()
        else:
            QMessageBox.warning(self, "Warning", "Please select a book to delete.")

    # Method to load books from the database
    def load_books(self):
        self.books_list.clear()
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        for book in books:
            status = "Available" if book[5] else "Borrowed"
            self.books_list.addItem(f"{book[0]}: {book[2]} by {book[1]} ({book[3]}) - {status}")

    # Method to set button style
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
                    "Status": "Available" if book_info[5] else "Borrowed"
                }
                dialog = BookInfoDialog(book_details)
                dialog.exec()
        else:
            QMessageBox.warning(self, "Warning", "Please select a book to view details.")

# Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
