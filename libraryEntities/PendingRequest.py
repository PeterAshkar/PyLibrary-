class PendingRequest:
    def __init__(self, member_id, book_id, request_date, number_of_loans_last_month):
        self.member_id = member_id
        self.book_id = book_id
        self.request_date = request_date
        self.number_of_loans_last_month = number_of_loans_last_month
