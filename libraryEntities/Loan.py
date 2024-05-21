class Loan:
    def __init__(self, book_id, member_id, loan_date=None, due_date=None, return_date=None, loan_id=None):
        self.loan_id = loan_id
        self.book_id = book_id
        self.member_id = member_id
        self.return_date = return_date
        self.due_date = due_date
        self.loan_date = loan_date

    def __str__(self):
        return f"Loan ID: {self.loan_id}\n" \
               f"Book ID: {self.book_id}\n" \
               f"Member ID: {self.member_id}\n" \
               f"Loan Date: {self.loan_date}\n" \
               f"Due Date: {self.due_date}\n" \
               f"Return Date: {self.return_date}\n"
