import datetime
import mysql
from DBManager import DBManager
from . import BooksRepository, MembersRepository


# this is a helping function to count how many loans did a specific member take of a specific book in the last month
@staticmethod
def get_loans_in_last_month(member_id, book_id):
    try:
        connection = DBManager.get_connection()

        # Get the current date
        current_date = datetime.date.today()

        # Subtract 1 month from the current date
        last_month_date = current_date.replace(month=current_date.month - 1)

        # Get the first day of the last month
        first_day_of_last_month = last_month_date.replace(day=1)

        # Get the last day of the last month
        last_day_of_last_month = first_day_of_last_month.replace(
            day=first_day_of_last_month.day,
            month=first_day_of_last_month.month + 1) - datetime.timedelta(days=1)

        sql_query = "SELECT count(*) as count " \
                    "FROM library.loanedbooks " \
                    "WHERE " \
                    "BookID=%s and " \
                    "MemberID=%s and " \
                    "LoanDate>=%s and LoanDate<=%s"

        values = (book_id, member_id, first_day_of_last_month, last_day_of_last_month)
        cursor = connection.cursor()
        cursor.execute(sql_query, values)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0]

    except mysql.connector.Error as err:
        print("Error:", err)


@staticmethod
def register_a_loan_book(loan):
    # checking if the book and the member exist in the db , checking via the id of each one
    if BooksRepository.search_books("id", loan.book_id) is None and MembersRepository.search_members("id",
                                                                                                     loan.member_id) is None:
        print("theres no such book or member")
        return None
    if BooksRepository.check_book_status(loan.book_id) == "Unavailable":
        print("the book is currently Unavailable!, you can join a waiting List")
        return None
    try:
        connection = DBManager.get_connection()
        # Automatically set the loan date to the current date
        loan_date = datetime.date.today()
        # Automatically set the due date to one month after the loan date
        due_date = loan_date + datetime.timedelta(days=30)
        # did not put the return date here since this function when the member first takes the book
        sql_query = "INSERT INTO loanedBooks (BookID, MemberID, LoanDate, DueDate)" \
                    "VALUES (%s, %s, %s, %s)"
        values = (loan.book_id, loan.member_id, loan_date, due_date)
        connection.cursor().execute(sql_query, values)
        connection.commit()
        connection.cursor().close()
        connection.close()
    except mysql.connector.Error as err:
        print("Error:", err)
    # change the status of the book to Unavailable after lending it
    BooksRepository.update_book_status(loan.book_id)


@staticmethod
# this function takes 2 parameters cause i need to set the return from the outside for more flexible approach
def return_a_lend_book(loan_id, book_id):
    if search_lend_book(loan_id) is None:
        print("no such loan in the loanedBooks db")
        return None
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        return_date = datetime.date.today()
        # Update the return date in the database
        cursor.execute("UPDATE loanedBooks SET ReturnDate = %s WHERE LoanID = %s", (return_date, loan_id))
        connection.commit()

        cursor.close()
        connection.close()

        print("Book returned successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)
    BooksRepository.update_book_status(book_id)


# helping function to check if the book actually exists in the loanedBooks db
def search_lend_book(loan_id):
    loan_id = int(loan_id)
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM loanedBooks WHERE LoanID = %s", (loan_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    except mysql.connector.Error as err:
        print("Error:", err)


# loaned books that have not been returned yet
def get_current_loaned_books():
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM loanedBooks WHERE ReturnDate IS NULL")
        loaned_books = cursor.fetchall()
        cursor.close()
        connection.close()
        return loaned_books

    except mysql.connector.Error as err:
        print("Error:", err)


def all_loans_in_a_month(month):
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM library.loanedBooks WHERE month(LoanDate) = %s", (month,))
        loans = cursor.fetchall()
        return loans
    except mysql.connector.Error as err:
        print("Error:", err)


def loans_between_dates(date_1, date_2):
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM library.loanedBooks WHERE LoanDate BETWEEN %s AND %s", (date_1, date_2))
        loans = cursor.fetchall()
        return loans
    except mysql.connector.Error as err:
        print("Error:", err)


# get all the loaned books that have been returned by the member
def get_returned_loaned_books():
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM library.loanedBooks WHERE ReturnDate IS NOT null")
        loans = cursor.fetchall()
        return loans
    except mysql.connector.Error as err:
        print("Error:", err)


# this function returns the most famous books by how many times the title of the book appeared in a certain month
def get_top_loaned_books(month, num):
    num = int(num)
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        # this query joins between the books and loanedBooks table by the BookID then it selects the title
        # it orders the result by titleCount in descending order and selects only the top num rows
        cursor.execute("SELECT books.Title, COUNT(*) AS titleCount "
                       "FROM library.books "
                       "JOIN library.loanedBooks ON books.BookID = loanedBooks.BookID "
                       "WHERE MONTH(LoanDate) = %s "
                       "GROUP BY books.Title "
                       "ORDER BY titleCount DESC "
                       "LIMIT %s;", (month, num))
        book_title_count = cursor.fetchall()
        return book_title_count
    except mysql.connector.Error as err:
        print("Error:", err)


# extra function for demonstration
def get_current_loaned_books_for_specific_member(member_id):
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT loanedBooks.LoanID, books.BookID, books.Title, books.Author, books.ISBN, books.Genre,LoanedBooks.LoanDate "
            "FROM library.books "
            "JOIN library.loanedBooks ON books.BookID = loanedBooks.BookID "
            "WHERE MemberID = %s and ReturnDate IS NULL", (member_id,))
        current_loaned_books = cursor.fetchall()
        return current_loaned_books
    except mysql.connector.Error as err:
        print("Error:", err)


# extra function
def get_current_loaned_books_for_specific_member_and_book(member_id, book_id):
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT loanedBooks.LoanID, books.BookID, books.Title, books.Author, books.ISBN, books.Genre,LoanedBooks.LoanDate "
            "FROM library.books "
            "JOIN library.loanedBooks ON books.BookID = loanedBooks.BookID "
            "WHERE MemberID = %s AND books.BookID = %s AND ReturnDate IS NULL", (member_id, book_id))
        current_loaned_books = cursor.fetchall()
        return current_loaned_books
    except mysql.connector.Error as err:
        print("Error:", err)


def get_returned_loaned_books_for_specific_member(member_id):
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT loanedBooks.LoanID, books.BookID, books.Title, books.Author, books.ISBN, books.Genre,loanedBooks.LoanDate "
            "FROM library.books "
            "JOIN library.loanedBooks ON books.BookID = loanedBooks.BookID "
            "WHERE MemberID = %s and ReturnDate IS NOT NULL", (member_id,))
        current_loaned_books = cursor.fetchall()
        return current_loaned_books
    except mysql.connector.Error as err:
        print("Error:", err)
