-- Create the customers table
CREATE TABLE IF NOT EXISTS customers (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Gender TEXT,
    PhoneNumber TEXT,
    ValidIdPath TEXT
);



-- Create the books table
CREATE TABLE IF NOT EXISTS books (
    BookID INTEGER PRIMARY KEY AUTOINCREMENT,
    ISBN TEXT,
    Title TEXT,
    Author TEXT,
    Category TEXT,
    Status TEXT,
    RentalFee INTEGER,
    Description TEXT,
    Cover_Image TEXT
);



-- Create the rentals table
CREATE TABLE IF NOT EXISTS rentals (
    RentalID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER,
    BookID INTEGER,
    RentalDate TEXT,
    RentalDueDate TEXT,
    RentalFee INTEGER,
    FinalRentFee INTEGER,
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
    FOREIGN KEY (BookID) REFERENCES books(BookID)
);



-- Create the returns table
CREATE TABLE IF NOT EXISTS returns (
    ReturnID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER,
    BookID INTEGER,
    ReturnDate TEXT,
    RentalDueDate TEXT,
    OverdueFee INTEGER,
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
    FOREIGN KEY (BookID) REFERENCES books(BookID),
    FOREIGN KEY (RentalDueDate) REFERENCES rentals(RentalDueDate)
);



-- Create the reserve table
CREATE TABLE IF NOT EXISTS reserve (
    ReserveID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER,
    BookID INTEGER,
    ReservationDate TEXT,
    ReservationFee REAL,
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
    FOREIGN KEY (BookID) REFERENCES books(BookID)
);



-- Insert 4 books
INSERT INTO books (ISBN, Title, Author, Category, Status, RentalFee, Description, Cover_Image) VALUES
('978-3-16-148410-0', 'Book One', 'Author A', 'Fiction', 'Available', 5, 'Description of Book One', 'cover_image1.jpg'),
('978-1-23-456789-7', 'Book Two', 'Author B', 'Non-Fiction', 'Available', 7, 'Description of Book Two', 'cover_image2.jpg'),
('978-0-12-345678-9', 'Book Three', 'Author C', 'Science', 'Available', 6, 'Description of Book Three', 'cover_image3.jpg'),
('978-4-56-789012-3', 'Book Four', 'Author D', 'Fantasy', 'Available', 8, 'Description of Book Four', 'cover_image4.jpg');



-- Insert 2 customers
INSERT INTO customers (Name, Gender, PhoneNumber, ValidIdPath) VALUES
('Customer One', 'Male', '1234567890', 'id_path1.jpg'),
('Customer Two', 'Female', '0987654321', 'id_path2.jpg');



-- Calculate the final rent fee for each rental and insert into rentals
-- Customer 1 rents Book 1 and Book 2
INSERT INTO rentals (CustomerID, BookID, RentalDate, RentalDueDate, RentalFee, FinalRentFee) VALUES
(1, 1, '2024-05-01', '2024-05-15', 5, (julianday('2024-05-15') - julianday('2024-05-01')) * 5),
(1, 2, '2024-05-01', '2024-05-15', 7, (julianday('2024-05-15') - julianday('2024-05-01')) * 7);



-- Update status of Book 1 and Book 2 to 'Rented'
UPDATE books SET Status = 'Rented' WHERE BookID IN (1, 2);



-- Customer 2 rents Book 3, Book 4, and Book 1
INSERT INTO rentals (CustomerID, BookID, RentalDate, RentalDueDate, RentalFee, FinalRentFee) VALUES
(2, 3, '2024-05-02', '2024-05-16', 6, (julianday('2024-05-16') - julianday('2024-05-02')) * 6),
(2, 4, '2024-05-02', '2024-05-16', 8, (julianday('2024-05-16') - julianday('2024-05-02')) * 8),
(2, 1, '2024-05-02', '2024-05-16', 5, (julianday('2024-05-16') - julianday('2024-05-02')) * 5);



-- Update status of Book 3, Book 4, and Book 1 to 'Rented'
UPDATE books SET Status = 'Rented' WHERE BookID IN (3, 4, 1);

-- Customer 2 returns Book 3
-- Calculate the overdue fee and insert into returns
-- Assuming an overdue fee of 2 units per day
INSERT INTO returns (CustomerID, BookID, ReturnDate, RentalDueDate, OverdueFee) VALUES
  
CASE 
    WHEN julianday('2024-05-10') > julianday('2024-05-16') THEN 
        (julianday('2024-05-10') - julianday('2024-05-16')) * 2 
    ELSE 
        0 
END);



-- Update the status of the returned book to 'Available'
UPDATE books SET Status = 'Available' WHERE BookID = 3;



-- Customer 2 reserves Book 2
INSERT INTO reserve (CustomerID, BookID, ReservationDate, ReservationFee) VALUES
(2, 2, '2024-05-11', 2.5);



-- Update the status of the reserved book to 'Reserved'
UPDATE books SET Status = 'Reserved' WHERE BookID = 2;



-- Filter the books that are rented
SELECT * FROM books WHERE Status = 'Rented';



-- Filter the books that are returned
SELECT * FROM books WHERE BookID IN (SELECT BookID FROM returns);



-- Filter the books that are available
SELECT * FROM books WHERE Status = 'Available';



-- Calculate the final rent fee based on rent date and due date
-- Assuming the rental fee is a daily rate
SELECT 
    r.RentalID,
    r.CustomerID,
    r.BookID,
    r.RentalDate,
    r.RentalDueDate,
    b.RentalFee,
    (julianday(r.RentalDueDate) - julianday(r.RentalDate)) * b.RentalFee AS FinalRentFee
FROM 
    rentals r
JOIN 
    books b ON r.BookID = b.BookID;



-- Calculate the overdue fee based on the return date and the due date
-- Assuming an overdue fee of 2 units per day
SELECT 
    r.ReturnID,
    r.CustomerID,
    r.BookID,
    r.ReturnDate,
    r.RentalDueDate,
    b.RentalFee,
    CASE 
        WHEN julianday(r.ReturnDate) > julianday(r.RentalDueDate) THEN 
            (julianday(r.ReturnDate) - julianday(r.RentalDueDate)) * 2 
        ELSE 
            0 
    END AS OverdueFee
FROM 
    returns r
JOIN 
    books b ON r.BookID = b.BookID;

--How many books customer rented
SELECT
    CustomerID,
    COUNT(BookID) AS RentedBooksCount
FROM
    rentals
WHERE   
    CustomerID = 1
GROUP BY
    CustomerID;