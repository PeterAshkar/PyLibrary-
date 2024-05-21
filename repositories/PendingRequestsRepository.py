import mysql
from DBManager import DBManager
from datetime import datetime
from libraryEntities.PendingRequest import PendingRequest
from repositories import LoansRepository

"""
this function inserts all the values to the pendingRequest table, it enters a 
date that is with fraction of seconds in order to be more accurate with the sorting later on.
"""


@staticmethod
def insert_to_waiting_list(member_id, book_id, num_of_loans_last_month):
    try:
        connection = DBManager.get_connection()
        # get the date of fractions of seconds precision
        request_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        sql_query = "INSERT INTO PendingRequest (MemberID, BookID, DateOfRequest, NumberOfLoansInLastMonth)" \
                    "VALUES (%s, %s, %s , %s)"
        values = (member_id, book_id, request_date, num_of_loans_last_month)
        connection.cursor().execute(sql_query, values)
        connection.commit()
        connection.cursor().close()
        connection.close()

    except mysql.connector.Error as err:
        print("Error:", err)


"""
this function will delete a row in the waiting list after the member manages to get the book
it needs both the member_id and the book_id to delete a row since a member can be in
different waiting lists for different books
"""


@staticmethod
def delete_from_waiting_list(member_id, book_id):
    try:
        connection = DBManager.get_connection()
        connection.cursor().execute("DELETE FROM PendingRequest WHERE MemberID = %s AND BookID=%s",
                                    (member_id, book_id))
        connection.commit()
        connection.cursor().close()
        connection.close()
    except mysql.connector.Error as err:
        print("Error:", err)


""""
get the waiting list for a specific book sorted first by if the number of the loan the user made in the last month
were more than 2, if not then sort the row via the date of request,
the output of this function/query is that it will returned a prioritized list first by the number of loans then the 
date of the request of the book.
"""


@staticmethod
def get_waiting_list_for_a_book(book_id):
    try:
        # fetch the waiting list entries for the specified book
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM PendingRequest "
            "WHERE BookID = %s "
            "ORDER BY "
            "       CASE "
            "           WHEN NumberOfLoansInLastMonth >=2 THEN -NumberOfLoansInLastMonth "
            "           ELSE DateOfRequest "
            "END ASC;",
            (book_id,))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return [
            PendingRequest(member_id=member_id,
                           book_id=book_id,
                           request_date=request_date,
                           number_of_loans_last_month=number_of_loans_last_month)
            for
            member_id, book_id, request_date, number_of_loans_last_month in rows
        ]

    except mysql.connector.Error as error:
        print("Error:", error)
        return None


"""
this function returns the first user in a specific waiting list based on the id of the book 
and with the help of get_waiting_list_for_a_book function.
"""


@staticmethod
def get_first_member_in_waiting_list(book_id):
    waiting_list = get_waiting_list_for_a_book(book_id)
    if waiting_list:
        return waiting_list[0].member_id
    else:
        print("Waiting List is empty for book:", book_id)


# this function checks if the member is in a waiting list based on his id and the id of the book
@staticmethod
def member_in_waiting_list(member_id, book_id):
    pending_list_for_book = get_waiting_list_for_a_book(book_id)
    # filter the result by the memberId , if the size 0 return false otherwise true
    size = len([obj for obj in pending_list_for_book if obj.member_id == member_id])
    return size > 0


"""
this function takes in the book id and members id then checks if they are in the waiting list
if they are then it wont add them but if they are not then it calls upon the get_loans_in_last_month
function to get the amount of a specific book that the member took in the last month
then it calls upon the insert_to_waiting_list to enter all 3 values (member_id, book_id, num_of_loans_last_month)
"""


@staticmethod
def add_to_waiting_list(book_id, member_id):
    member_exists = member_in_waiting_list(member_id, book_id)
    # if the member id and book id exist do nothing otherwise get number of loans las month
    if not member_exists:
        num_of_loans_last_month = LoansRepository.get_loans_in_last_month(member_id, book_id);
        insert_to_waiting_list(member_id, book_id, num_of_loans_last_month)
        print("Member have been put into the waiting list")
    else:
        print("Member already exists in this waiting list")
        return False
