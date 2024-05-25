--addbook.py
CREATE TABLE IF NOT EXISTS Books (
    ISBN TEXT PRIMARY KEY,
    Title TEXT NOT NULL,
    Author TEXT NOT NULL,
    Category TEXT NOT NULL,
    Status TEXT NOT NULL,
    BaseRentFee REAL NOT NULL,
    Description TEXT NOT NULL,
    CoverImage TEXT NOT NULL
);

INSERT INTO Books (ISBN, Title, Author, Category, Status, BaseRentFee, Description, CoverImage)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);

--main.py
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

Inserting Data
These queries are used to insert new records into the respective tables.

#Insert a new book:
python
Copy code
c.execute('''INSERT INTO books (ISBN, Title, Author, Category, Status, RentalFee, Description, Cover_Image)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', book_info)
Insert a new customer:

python
Copy code
cursor.execute(
    "INSERT INTO customers (Name, Gender, PhoneNumber, ValidIdPath) VALUES (?, ?, ?, ?)",
    customer_info)
Updating Data
These queries are used to update existing records in the database.

#Update a book:
python
Copy code
c.execute('''
    UPDATE books
    SET ISBN = ?, Title = ?, Author = ?, Category = ?, RentalFee = ?, Description = ?, Cover_Image = ?
    WHERE BookID = ?
''', (book_info['ISBN'], book_info['Title'], book_info['Author'], book_info['Category'], float(book_info['RentalFee']), book_info['Description'], book_info['Cover_Image'], book_info['BookID']))
Update a customer:

python
Copy code
c.execute('''
    UPDATE customers
    SET Name = ?, Gender = ?, PhoneNumber = ?, ValidIdPath = ?
    WHERE CustomerID = ?
''', (customer_info['Name'], customer_info['Gender'], customer_info['PhoneNumber'], customer_info['ValidIdPath'], customer_info['CustomerID']))
Deleting Data
These queries are used to delete records from the database.

#Delete a book:
python
Copy code
cursor.execute("DELETE FROM books WHERE BookID = ?", (book_id,))
Delete a customer:

python
Copy code
cursor.execute("DELETE FROM customers WHERE CustomerID = ?", (customer_id,))
Fetching Data
These queries are used to retrieve data from the database for display in the application.

#Fetch all books:
python
Copy code
c.execute('SELECT * FROM books')
books = c.fetchall()
Fetch all customers:

python
Copy code
c.execute('SELECT * FROM customers')
customers = c.fetchall()
Fetch book data by ID:

python
Copy code
c.execute('SELECT ISBN, Title, Author, Category, RentalFee, Description, Cover_Image FROM books WHERE BookID = ?', (book_id,))
book = c.fetchone()
Fetch customer data by ID:

python
Copy code
c.execute('SELECT Name, Gender, PhoneNumber, ValidIdPath FROM customers WHERE CustomerID = ?', (customer_id,))
customer = c.fetchone()
Filter books based on search text:

python
Copy code
query = f"SELECT * FROM books WHERE Title LIKE '%{text}%' OR RentalFee LIKE '%{text}%' OR Author LIKE '%{text}%' OR Category LIKE '%{text}%' OR Status LIKE '%{text}%'"
c.execute(query)
books = c.fetchall()
Filter customers based on search text:

python
Copy code
query = f"SELECT * FROM customers WHERE Name LIKE '%{text}%' OR Gender LIKE '%{text}%' OR CustomerID LIKE '%{text}%'"
c.execute(query)
customers = c.fetchall()
Fetch transactions data:

# Fetch data from rentals table
c.execute('SELECT RentalDate, "Rented", Title, Name FROM rentals INNER JOIN books ON rentals.BookID = books.BookID INNER JOIN customers ON rentals.CustomerID = customers.CustomerID')
rentals_data = c.fetchall()

# Fetch data from returns table
c.execute('SELECT ReturnDate, "Returned", Title, Name FROM returns INNER JOIN books ON returns.BookID = books.BookID INNER JOIN customers ON returns.CustomerID = customers.CustomerID')
returns_data = c.fetchall()

# Fetch data from reserve table
c.execute('SELECT ReservationDate, "Reserved", Title, Name FROM reserve INNER JOIN books ON reserve.BookID = books.BookID INNER JOIN customers ON reserve.CustomerID = customers.CustomerID')
reserve_data = c.fetchall()

--rentbook.py
#Fetching the CustomerID based on the selected customer's name:
SELECT CustomerID FROM customers WHERE Name = ?

#Fetching the BookID, RentalFee, and Status based on the selected book's title:
SELECT BookID, RentalFee, Status FROM books WHERE Title = ?

#Checking if the book is available for rent:
SELECT CustomerID FROM reserve WHERE BookID = ? AND ReservationDate = ?

#Inserting the rental record into the rentals table:
INSERT INTO rentals (CustomerID, BookID, RentalDate, RentalDueDate, RentalFee) VALUES (?, ?, ?, ?, ?)

#Updating the status of the book to 'Rented':
UPDATE books SET Status = 'Rented' WHERE BookID = ?

--Reservebook.py
#Fetching the BookID based on the selected book's title:
SELECT BookID FROM books WHERE Title = ?

#Fetching the CustomerID based on the selected customer's name:
SELECT CustomerID FROM customers WHERE Name = ?

#Inserting the reservation record into the reserve table:
INSERT INTO reserve (CustomerId, BookId, ReservationDate, ReservationFee) VALUES (?, ?, ?, ?)

#Fetching the status of the book:
SELECT Status FROM books WHERE BookID = ?

#Updating the status of the book to 'Reserved':
UPDATE books SET Status = 'Reserved' WHERE BookID = ?

--returnbook.py
#Fetching the BookID based on the selected book's title:
SELECT BookID FROM books WHERE Title = ?

#Fetching the CustomerID based on the selected customer's name:
SELECT CustomerID FROM customers WHERE Name = ?

#Fetching the Rental Due Date based on the selected book's title:
SELECT RentalDueDate FROM rentals WHERE BookID = (SELECT BookID FROM books WHERE Title = ?)

#Fetching the Rental Fee based on the selected book's title:
SELECT RentalFee FROM books WHERE Title = ?

#Inserting the return record into the returns table:
INSERT INTO returns (CustomerId, BookId, ReturnDate, RentalDueDate, OverdueFee) VALUES (?, ?, ?, ?, ?)

#Updating the status of the book to 'Available':
UPDATE books SET Status = 'Available' WHERE BookID = ?