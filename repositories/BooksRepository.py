import mysql
from DBManager import DBManager

# Create an instance of the DBManager class
from libraryEntities.Book import Book


@staticmethod
def add_book(book):
    try:
        connection = DBManager.get_connection()
        sql_query = "INSERT INTO books (Title, Author, ISBN, Genre, shelfLocation, Status) " \
                    "VALUES (%s, %s, %s, %s, %s, %s)"
        values = (book.title, book.author, book.isbn, book.genre, book.shelf_location, book.status)
        connection.cursor().execute(sql_query, values)
        connection.commit()
        connection.cursor().close()
        connection.close()
    except mysql.connector.Error as err:
        print("Error:", err)


@staticmethod
def update_book(book):
    existing_book = search_books("id", book.book_id)
    if not existing_book:
        print("Error: Book with ID {} not found.".format(book.book_id))
        return

    try:
        connection = DBManager.get_connection()
        sql_query = "UPDATE books SET Title = %s, Author = %s, ISBN = %s, Genre = %s, shelfLocation = %s," \
                    " Status = %s WHERE BookID = %s"
        values = (
            book.title, book.author, book.isbn, book.genre, book.shelf_location, book.status,
            book.book_id)
        connection.cursor().execute(sql_query, values)
        connection.commit()
        connection.cursor().close()
        connection.close()
    except mysql.connector.Error as err:
        print("Error:", err)


def delete_book(book_id):
    if search_books("id", book_id) is None:
        print("no such book")
        return None
    try:
        connection = DBManager.get_connection()
        connection.cursor().execute("DELETE FROM books WHERE BookID = %s", (book_id,))
        connection.commit()
        connection.cursor().close()
        connection.close()
    except mysql.connector.Error as err:
        print("Error:", err)


@staticmethod
# it takes 2 parameters (search_type and search_term) we look for the type of what we'll search for (title,id etc..)
# and then we search for the search_term which could the number of id or the name of the title etc...
def search_books(search_type, search_term):
    try:
        connection = DBManager.get_connection()
        if search_type == "Title":
            sql_query = "SELECT * FROM books WHERE Title LIKE %s"
        elif search_type == "Author":
            sql_query = "SELECT * FROM books WHERE Author LIKE %s"
        elif search_type == "Genre":
            sql_query = "SELECT * FROM books WHERE Genre LIKE %s"
        elif search_type == "id":
            sql_query = "SELECT * FROM books WHERE BookID = %s"

        else:
            print("Invalid search type")
            return None

        cursor = connection.cursor()
        cursor.execute(sql_query, (search_term,))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        if not rows:
            print("no such book exists!")
            return None

        return [
            Book(book_id=book_id, title=title, author=author, isbn=isbn, genre=genre, shelf_location=shelf_location,
                 status=status)
            for
            book_id, title, author, isbn, genre, shelf_location, status in
            rows]

    except mysql.connector.Error as error:
        print("Error:", error)
        return None


# helping function to check the book status in the db
def check_book_status(book_id):
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()

        # Fetch the current status of the book
        cursor.execute("SELECT Status FROM books WHERE BookID = %s", (book_id,))
        # takes the select option from the query and stores it in the current_status variable
        current_status = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return current_status
    except mysql.connector.Error as err:
        print("Error:", err)


# helping function to change the status of the book dynamically after it got loaned or returned via the book id
def update_book_status(book_id):
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()

        # Fetch the current status of the book
        cursor.execute("SELECT Status FROM books WHERE BookID = %s", (book_id,))
        # takes the select option from the query and stores it in the current_status variable
        current_status = cursor.fetchone()[0]

        # Update the status based on the current status
        new_status = "Unavailable" if current_status.lower() == "available" else "Available"

        # Update the status in the database
        cursor.execute("UPDATE books SET Status = %s WHERE BookID = %s", (new_status, book_id))
        connection.commit()

        cursor.close()
        connection.close()

        print("Book status updated successfully.")
    except mysql.connector.Error as err:
        print("Error:", err)


@staticmethod
def get_books():
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        return [
            Book(book_id=book_id, title=title, author=author, isbn=isbn, genre=genre, shelf_location=shelf_location,
                 status=status)
            for
            book_id, title, author, isbn, genre, shelf_location, status in
            books]
    except mysql.connector.Error as err:
        print("Error:", err)

