class User:
    def __init__(self, name, email, phone, user_id=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone


class Member(User):
    def __init__(self, name, email, phone, membership_type, membership_start_date, member_id=None):
        super().__init__(name, email, phone, member_id)
        self.membership_type = membership_type
        self.membership_start_date = membership_start_date
        self.member_id = member_id


class Employee(User):
    def __init__(self, name, email, phone, employee_type, employee_id=None):
        super().__init__(name, email, phone, employee_id)
        self.employee_type = employee_type
        self.employee_id = employee_id
