class Book:
    # the status of the book is always available upon first entering it to the db
    def __init__(self, title, author, isbn, genre, shelf_location, status="Available", book_id=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.shelf_location = shelf_location
        self.status = status
