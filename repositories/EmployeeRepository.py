import mysql
from DBManager import DBManager
from repositories import BooksRepository, MembersRepository, LoansRepository, PendingRequestsRepository

"""
these functions here can be done by both employee and manager type employee such as, adding, deleting, editing,
searching for books members, also they can register and return books, they can also get statistics for these
books (loaned books) whether it is get all current books and all returned books or loans between dates,
loans in a specific month etc...
"""


# ---------------------------------------------------------------------------------------------------------
def add_book(book):
    BooksRepository.add_book(book)


def delete_book(book_id):
    BooksRepository.delete_book(book_id)


def get_books():
    return BooksRepository.get_books()


def update_book(book):
    BooksRepository.update_book(book)


def search_books(search_type, search_term):
    return BooksRepository.search_books(search_type, search_term)


def add_member(member):
    MembersRepository.add_member(member)


def update_member(member):
    MembersRepository.update_member(member)


def delete_member(member_id):
    MembersRepository.delete_member(member_id)


def search_members(search_type, search_term):
    return MembersRepository.search_members(search_type, search_term)


def get_members():
    return MembersRepository.get_members()


def search_a_certain_member(member_id):
    return MembersRepository.search_a_certain_member(member_id)


def register_a_loan_book(loan):
    LoansRepository.register_a_loan_book(loan)


def return_a_lend_book(loan_id, book_id):
    return LoansRepository.return_a_lend_book(loan_id, book_id)


def get_current_loaned_books():
    return LoansRepository.get_current_loaned_books()


def all_loans_in_a_month(month):
    return LoansRepository.all_loans_in_a_month(month)


def loans_between_dates(date_1, date_2):
    return LoansRepository.loans_between_dates(date_1, date_2)


def get_returned_loaned_books():
    return LoansRepository.get_returned_loaned_books()


def get_top_loaned_books(month, num):
    return LoansRepository.get_top_loaned_books(month, num)


def get_current_loaned_books_for_specific_member(member_id):
    return LoansRepository.get_current_loaned_books_for_specific_member(member_id)


def get_returned_loaned_books_for_specific_member(member_id):
    return LoansRepository.get_returned_loaned_books_for_specific_member(member_id)


def get_current_loaned_books_for_specific_member_and_book(member_id, book_id):
    return LoansRepository.get_current_loaned_books_for_specific_member_and_book(member_id, book_id)


def get_first_member_in_waiting_list(book_id):
    return PendingRequestsRepository.get_first_member_in_waiting_list(book_id)


def get_waiting_list_for_a_book(book_id):
    return PendingRequestsRepository.get_waiting_list_for_a_book(book_id)


def add_to_waiting_list(book_id, member_id):
    PendingRequestsRepository.add_to_waiting_list(book_id, member_id)


def delete_from_waiting_list(member_id, book_id):
    PendingRequestsRepository.delete_from_waiting_list(member_id, book_id)


def member_in_waiting_list(member_id, book_id):
    return PendingRequestsRepository.member_in_waiting_list(member_id, book_id)


# --------------------------------------------------------------------------------------------------------------
# the add and delete functions are meant to be used only by the manager type employee
def add_employee(employee):
    # in case there was an incorrect input with the employee_type then change it to Employee
    if employee.employee_type != "Employee":
        employee.employee_type = "Employee"
    if search_employee(employee.employee_id) is None:
        try:
            connection = DBManager.get_connection()
            sql_query = "INSERT INTO employees (Name, Email, Phone, EmployeeType) " \
                        "VALUES (%s, %s, %s, %s)"
            values = (employee.name, employee.email, employee.phone, employee.employee_type)
            connection.cursor().execute(sql_query, values)
            connection.commit()
            connection.cursor().close()
            connection.close()
        except mysql.connector.Error as err:
            print("Error:", err)


def delete_employee(employee_id):
    if search_employee(employee_id) is not None:
        try:
            connection = DBManager.get_connection()
            connection.cursor().execute("DELETE FROM employees WHERE EmployeeID LIKE %s", (employee_id,))
            connection.commit()
            connection.cursor().close()
            connection.close()
        except mysql.connector.Error as err:
            print("Error:", err)


def search_employee(employee_id):
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()  # Obtain cursor
        sql_query = "SELECT * FROM employees WHERE EmployeeID LIKE %s"
        cursor.execute(sql_query, (employee_id,))
        row = cursor.fetchone()  # Fetch one row
        if row is None:
            print("No employee found with ID:", employee_id)
            return None
        else:
            # Process the fetched row
            cursor.close()
            connection.close()
            return row

    except mysql.connector.Error as error:
        print("Error:", error)
        return None


def get_employees():
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM employees WHERE EmployeeType = 'Employee'")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    except mysql.connector.Error as error:
        print("Error:", error)
        return None
