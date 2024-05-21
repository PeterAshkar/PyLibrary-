import mysql.connector


class DBManager:

    @staticmethod
    def init_connection():
        try:
            connection = mysql.connector.connect(host="localhost", user="root", password="Ash971Pet271")
            print("Connection established")
            DBManager.create_database(connection.cursor())
            connection = mysql.connector.connect(host="localhost", user="root", password="Ash971Pet271",
                                                 database="library")
            DBManager.create_tables(connection.cursor())
            DBManager.insert_manager_to_employees(connection)

        except mysql.connector.Error as err:
            print("Error:", err)

    @staticmethod
    def create_database(cursor):
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS library")
            print("Database created successfully!")
        except mysql.connector.Error as err:
            print("Error:", err)

    @staticmethod
    def create_tables(cursor):
        DBManager.create_books_table(cursor)
        DBManager.create_members_table(cursor)
        DBManager.loaned_books_table(cursor)
        DBManager.create_employees_table(cursor)
        DBManager.create_pending_request_table(cursor)

    @staticmethod
    def insert_manager_to_employees(connection):
        try:
            cursor = connection.cursor()
            sql = "INSERT INTO employees (Name, Email, Phone, EmployeeType ) VALUES (%s, %s, %s, %s)"
            values = ("John Doe", "john0@gmail.com", "0508730519", "Manager")
            cursor.execute(sql, values)
            # Commit the transaction
            connection.commit()
            print("Manager inserted successfully.")
        except mysql.connector.Error as err:
            print("Error:", err)

    @staticmethod
    def create_employees_table(curses):
        curses.execute(
            """
            CREATE TABLE employees (
            EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255),
            Email Varchar(255),
            Phone VARCHAR(255),
            EmployeeType VARCHAR(255) );
            """
        )

    @staticmethod
    def loaned_books_table(curses):
        curses.execute(
            """
            CREATE TABLE loanedBooks (
            LoanID INT AUTO_INCREMENT PRIMARY KEY,
            BookID INT,
            MemberID INT,
            FOREIGN KEY (BookID) REFERENCES books(BookID) ON DELETE CASCADE,
            FOREIGN KEY (MemberID) REFERENCES members(MemberID) ON DELETE CASCADE,
            LoanDate Date,
            DueDate Date,
            ReturnDate Date);
            """
        )

    @staticmethod
    def create_members_table(curses):
        curses.execute(
            """
            CREATE TABLE members (
            MemberID INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255),
            Email VARCHAR(255),
            Phone VARCHAR(255),
            MembershipType VARCHAR(255),
            MembershipStartDate Date );
            """
        )

    @staticmethod
    def create_books_table(curses):
        curses.execute(
            """
            CREATE TABLE books (
            BookID INT AUTO_INCREMENT PRIMARY KEY,
            Title VARCHAR(255),
            Author VARCHAR(255), 
            ISBN VARCHAR(255),
            Genre VARCHAR(255),
            ShelfLocation VARCHAR(255),
            Status VARCHAR(255));
            """
        )

    @staticmethod
    def create_pending_request_table(curses):
        curses.execute(
            """
            CREATE TABLE pendingrequest (
            MemberID INT,
            BookID INT,
            DateOfRequest DATETIME(6),
            NumberOfLoansInLastMonth INT,
            PRIMARY KEY (MemberID, BookID),
            FOREIGN KEY (MemberID) REFERENCES members(MemberID) ON DELETE CASCADE,
            FOREIGN KEY (BookID) REFERENCES books(BookID) ON DELETE CASCADE );
            """
        )

    @staticmethod
    def get_cursor():
        connection = DBManager.init_connection()
        if connection:
            return connection.cursor()

    @staticmethod
    def get_connection():
        try:
            return mysql.connector.connect(host="localhost", user="root", password="Ash971Pet271", database="library")
        except mysql.connector.Error as err:
            print("Error:", err)
