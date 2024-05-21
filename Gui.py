import tkinter as tk

from DBManager import DBManager
from libraryEntities.Loan import Loan
from repositories import EmployeeRepository
from libraryEntities.Book import Book
from libraryEntities.User import Member, Employee
from tkinter import *
from tkinter import ttk, messagebox
import re


class LoginGui:
    def __init__(self):
        self.root = Tk()
        self.root.title("Login")
        self.root.geometry("925x500")
        self.root.config(bg="#fff")
        self.root.resizable(False, False)
        self.root.iconbitmap("icons/loginIcon.ico")
        img = PhotoImage(file='images/login.png')
        Label(self.root, image=img, bg='white').place(x=50, y=50)
        self.frame = Frame(self.root, width=350, height=350, bg="white")
        self.frame.place(x=480, y=70)
        heading = Label(self.frame, text='Sign in', fg='#57a1f8', bg='white',
                        font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        self.user = Entry(self.frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        self.user.place(x=30, y=80)
        self.user.insert(0, 'Username')  # john0@gmail.com
        self.user.bind('<FocusIn>', self.user_on_enter)
        self.user.bind('<FocusOut>', self.user_on_leave)
        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=107)

        self.code = Entry(self.frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
        self.code.place(x=30, y=150)
        self.code.insert(0, 'Password/ID')  # 1
        self.code.bind('<FocusIn>', self.code_on_enter)
        self.code.bind('<FocusOut>', self.code_on_leave)
        Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=177)

        self.sign_in = Button(self.frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', cursor='hand2',
                              border=0, command=self.on_button_click)
        self.sign_in.place(x=35, y=240)
        self.label = Label(self.frame, text="Don't have an account?", border=0, bg='white', fg='black')
        self.label.place(x=75, y=290)
        self.sign_up = Button(self.frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8',
                              command=self.sign_up)
        self.sign_up.place(x=215, y=287)

        # Dropdown menu options
        options = ["Member", "Employee"]
        self.var = StringVar()
        self.var.set(options[0])  # Set default option
        self.dropdown = OptionMenu(self.frame, self.var, *options)
        self.dropdown.config(bg="white", fg="black", font=('Microsoft YaHei UI Light', 11), bd=1, relief="solid")
        self.dropdown.place(x=120, y=195)

        self.root.mainloop()

    def user_on_enter(self, e):
        self.user.delete(0, 'end')

    def user_on_leave(self, e):
        name = self.user.get()
        if name == '':
            self.user.insert(0, 'Username')

    def code_on_enter(self, e):
        self.code.delete(0, 'end')

    def code_on_leave(self, e):
        password = self.code.get()
        if password == '':
            self.code.insert(0, 'Password')

    def sign_up(self):
        # Destroy the current login GUI
        self.root.destroy()
        SignUpGUI()

    # when the sign in button is clicked this function will be called upon and get the username and password input
    def on_button_click(self):
        # the username is the email of the member/employee
        username = self.user.get()
        if not username or username == "UserName":
            messagebox.showerror("Error", "Please enter a valid username")
            return

        # the password is the id of the member/employee
        password = self.code.get()
        if not password or password == "Password":
            messagebox.showerror("Error", "Please enter a valid password")
            return

        selected_option = self.var.get()
        self.verify_user(username, password, selected_option)  # Call verify_user with the obtained values

    def verify_user(self, email, id, user_type):
        if user_type == "Member":
            # we'll search via the email first
            member = EmployeeRepository.search_a_certain_member(id)
            # Check if member is empty (not found)
            if member is None:
                messagebox.showerror("Error", "No such member in the system!")
                return
            # take the email value from the member
            retrieved_email = member[2]
            # check if the email in the input is incorrect
            if retrieved_email != email:
                messagebox.showerror("Error", "Provided email does not match the member's email!")
                return
            self.root.destroy()
            MenuForUser(member)
        else:
            employee = EmployeeRepository.search_employee(id)
            # check if employee is empty (not found)
            if employee is None:
                messagebox.showerror("Error", "No such employee in the system!")
                return
            # take the email value from the employee
            retrieved_email = employee[2]
            print(retrieved_email)
            # check if the email in the input is incorrect
            if retrieved_email != email:
                messagebox.showerror("Error", "Provided email does not match the employee's email!")
                return
            self.root.destroy()
            MenuForEmployee(employee)


class SignUpGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Sign Up")
        self.root.geometry("925x500")
        self.root.iconbitmap("icons/sign up.ico")
        img = PhotoImage(file='images/sign up.png')
        Label(self.root, image=img, bg='white').place(x=50, y=100)
        self.root.config(bg="#fff")
        self.root.resizable(False, False)
        self.frame = Frame(self.root, width=480, height=480, bg="white")
        self.frame.place(x=480, y=10)
        heading = Label(self.frame, text='Sign up', fg='#57a1f8', bg='white',
                        font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)
        self.entries = {}  # Dictionary to store entry widgets
        # a more dynamic way to setup the buttons
        self.create_entry(self.frame, "Name", 30, 80, "name")
        self.create_entry(self.frame, "Email", 30, 150, "email")
        self.create_entry(self.frame, "Phone", 30, 220, "phone")
        self.create_entry(self.frame, "Member Type (gold,silver)", 30, 290, "type")
        self.create_entry(self.frame, "Date (YYYY-MM-DD)", 30, 360, "start_date")

        self.sign_up = Button(self.frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white', cursor='hand2',
                              border=0, command=self.on_click)
        self.sign_up.place(x=30, y=420)
        self.root.mainloop()

    # providing placeholder text in the entry fields and removing it when the user interacts with the fields
    def create_entry(self, parent, placeholder, x, y, key):
        entry = Entry(parent, width=25, fg='black', border=0, bg='white',
                      font=('Microsoft YaHei UI Light', 11))
        entry.place(x=x, y=y)
        entry.insert(0, placeholder)
        """
        This lambda captures the event, widget, and text variables from the on_entry/on_leave functions 
        the widget is the entry in this case and the text is the text in each entry 
        then these values that are stored in the lambda function are bind by the <FocusIn>/<FocusOut> events
        """
        entry.bind("<FocusIn>", lambda event, widget=entry, text=placeholder: self.on_entry(event, widget, text))
        entry.bind("<FocusOut>", lambda event, widget=entry, text=placeholder: self.on_leave(event, widget, text))
        Frame(parent, width=295, height=2, bg='black').place(x=x - 5, y=y + 27)
        # storing the reference to entry widget
        self.entries[key] = entry

    def on_entry(self, event, widget, default_text):
        if widget.get() == default_text:
            widget.delete(0, 'end')

    def on_leave(self, event, widget, default_text):
        if widget.get() == '':
            widget.insert(0, default_text)

    def on_click(self):
        name = self.entries["name"].get().strip()
        email = self.entries["email"].get().strip()
        phone = self.entries["phone"].get().strip()
        type = self.entries["type"].get().strip()
        start_date = self.entries["start_date"].get().strip()
        # fields is created to check if the user did not insert anything in the entries or kept the placeholders
        fields = [(name, "Name"), (email, "Email"), (phone, "Phone"), (type, "Member Type (gold,silver)"),
                  (start_date, "Date (YYYY-MM-DD)")]

        for field, placeholder in fields:
            if not field:
                messagebox.showerror("Error", "All fields are required!")
                return
            elif field == placeholder:
                messagebox.showerror("Error", f"Please fill in the {placeholder} field.")
                return
            # checking the validity of the inserted email pattern by the member.
        pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(pattern, email) is None:
            messagebox.showerror("Error", "Invalid email address. Example: Roni@gmail.com")
            return
        # get a general phone number that start with 05 and 8 more numbers
        phone_pattern = re.compile(r'^05\d{8}$')
        if re.fullmatch(phone_pattern, phone) is None:
            messagebox.showerror("Error", "Invalid Phone number, example: 0502100781. 10 in length and starts with 05")
            return

        # check if the email exists in the db
        if EmployeeRepository.search_members("email", email):
            messagebox.showerror("Error", "you cant use this email, it already exists!")
            return
        member = Member(name, email, phone, type, start_date)
        EmployeeRepository.add_member(member)
        # search for the recently signed up member and show him his id
        member_id = EmployeeRepository.search_members("email", email)[0].member_id
        messagebox.showinfo("Success", f"you were added successfully this is your id: {member_id}")

        # destroy the current root and go back to the login frame after signing up.
        self.root.destroy()
        LoginGui()


class BookDialog(tk.Toplevel):
    def __init__(self, parent, title="Book Details", initial_values=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)

        if initial_values is None:
            initial_values = {"Title": "", "Author": "", "ISBN": "", "Genre": "", "ShelfLocation": ""}

        self.result = None

        tk.Label(self, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.title_entry.insert(0, initial_values["Title"])

        tk.Label(self, text="Author:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = tk.Entry(self)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)
        self.author_entry.insert(0, initial_values["Author"])

        tk.Label(self, text="ISBN:").grid(row=2, column=0, padx=5, pady=5)
        self.isbn_entry = tk.Entry(self)
        self.isbn_entry.grid(row=2, column=1, padx=5, pady=5)
        self.isbn_entry.insert(0, initial_values["ISBN"])

        tk.Label(self, text="Genre:").grid(row=3, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(self)
        self.genre_entry.grid(row=3, column=1, padx=5, pady=5)
        self.genre_entry.insert(0, initial_values["Genre"])

        tk.Label(self, text="Shelf Location:").grid(row=4, column=0, padx=5, pady=5)
        self.shelf_location_entry = tk.Entry(self)
        self.shelf_location_entry.grid(row=4, column=1, padx=5, pady=5)
        self.shelf_location_entry.insert(0, initial_values["ShelfLocation"])

        tk.Button(self, text="OK", command=self.on_add).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(self, text="Cancel", command=self.cancel).grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.grab_set()  # Make window modal
        self.wait_visibility()
        self.focus_set()

    def on_add(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        genre = self.genre_entry.get().strip()
        shelf_location = self.shelf_location_entry.get().strip()

        if not title or not author or not isbn or not genre or not shelf_location:
            messagebox.showerror("Error", "All fields are required.")
            return

        self.result = {"Title": title, "Author": author, "ISBN": isbn, "Genre": genre, "ShelfLocation": shelf_location}
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result

    def cancel(self):
        self.result = None
        self.destroy()  # Close the Toplevel window


class SearchBookDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent)
        self.title("Search Books")
        self.result = None
        options = ["Title", "Author", "Genre", "id"]
        self.var = tk.StringVar(self)
        self.var.set(options[0])  # Set default option

        tk.Label(self, text="Search by:").grid(row=0, column=0, padx=5, pady=5)
        self.dropdown = tk.OptionMenu(self, self.var, *options)
        self.dropdown.config(bg="white", fg="black", font=('Microsoft YaHei UI Light', 11), bd=1, relief="solid")
        self.dropdown.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Enter search term:").grid(row=1, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self, text="Search", command=self.on_search).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(self, text="Cancel", command=self.cancel).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def on_search(self):
        search_field = self.var.get()  # Get the selected search field
        search_term = self.search_entry.get()  # Get the entered search term
        self.result = {"SearchField": search_field, "SearchTerm": search_term}
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result

    def cancel(self):
        self.result = None
        self.destroy()


class PendingListDialog(tk.Toplevel):
    def __init__(self, parent, waiting_list):
        super().__init__(parent)
        self.waiting_list = waiting_list
        self.title("Pending List")
        self.geometry("1000x400")  # Adjust size as needed
        self.config(bg="#fff")
        self.iconbitmap("icons/waiting_list.ico")

        # Frame for Treeview
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # Treeview setup
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("MemberID", "BookID", "DateOfRequest", "NumberOfLoansInLastMonth"),
                                 show="headings")
        self.tree.heading("MemberID", text="MemberID")
        self.tree.heading("BookID", text="BookID")
        self.tree.heading("DateOfRequest", text="DateOfRequest")
        self.tree.heading("NumberOfLoansInLastMonth", text="NumberOfLoansInLastMonth")
        self.tree.grid(row=0, column=0, sticky="nsew")  # grid instead of pack

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        for entry in waiting_list:
            self.tree.insert('', 'end', values=(
                entry.member_id, entry.book_id, entry.request_date, entry.number_of_loans_last_month))

        self.grab_set()
        self.wait_visibility()
        self.focus_set()


class BookManagementGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Book Management System")
        self.window.geometry("1400x600")
        self.window.config(bg="#fff")
        self.window.resizable(False, False)
        self.window.iconbitmap("icons/bookIcon.ico")
        self.icons = {}
        # Frame for Treeview and Scrollbar for improved responsiveness
        tree_frame = ttk.Frame(window)
        tree_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        # Treeview setup
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("id", "title", "author", "ISBN", "genre", "ShelfLocation", "status"),
                                 show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("genre", text="Genre")
        self.tree.heading("ShelfLocation", text="ShelfLocation")
        self.tree.heading("status", text="Status")
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10)
        window.grid_columnconfigure(0, weight=1)

        icon_names = ['add', 'edit', 'delete', 'search', 'refresh', 'waiting_list']
        actions = [self.add_book, self.update_book, self.delete_book, self.search, self.refresh_book_list,
                   self.show_waiting_list_for_a_book]
        for i, (icon_name, action) in enumerate(zip(icon_names, actions)):
            icon_path = f'images/{icon_name}.png'
            self.icons[icon_name] = PhotoImage(file=icon_path)

            button = ttk.Button(btn_frame, text=f"{icon_name}", image=self.icons[icon_name], compound="left",
                                command=action)
            button.grid(row=0, column=i, padx=1, pady=1, sticky='ew')
            btn_frame.grid_columnconfigure(i, weight=1)
        self.refresh_book_list()
        # Make window modal
        self.window.grab_set()
        self.window.wait_visibility()
        self.window.focus_set()

    def refresh_book_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in EmployeeRepository.get_books():
            self.tree.insert('', 'end', values=(
                book.book_id, book.title, book.author, book.isbn, book.genre, book.shelf_location, book.status))

    def add_book(self):
        dialog = BookDialog(self.window)
        dialog.show()
        result = dialog.result
        if result:  # Check if result is not None
            book = Book(title=result["Title"], author=result["Author"], isbn=result["ISBN"], genre=result["Genre"],
                        shelf_location=result["ShelfLocation"])
            EmployeeRepository.add_book(book)
            self.refresh_book_list()

    def update_book(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0], 'values')
            initial_values = {"id": item[0], "Title": item[1], "Author": item[2], "ISBN": item[3], "Genre": item[4],
                              "ShelfLocation": item[5], "status": item[6]}
            dialog = BookDialog(self.window, "Update Book", initial_values)
            result = dialog.show()
            if result:  # Check if result is not None
                book = Book(result["Title"], result["Author"], result["ISBN"], result["Genre"], result["ShelfLocation"],
                            initial_values["status"], initial_values["id"])
                EmployeeRepository.update_book(book)
                self.refresh_book_list()
        else:
            messagebox.showwarning("Warning", "Please select a book to update.")

    def delete_book(self):
        selected = self.tree.selection()
        if selected:
            book_id = self.tree.item(selected[0], 'values')[0]
            EmployeeRepository.delete_book(book_id)
            self.refresh_book_list()
        else:
            messagebox.showwarning("Warning", "Please select a book to delete.")

    def search(self):
        dialog = SearchBookDialog(self.window)
        result = dialog.show()
        if result:
            search_field = result["SearchField"]
            search_term = result["SearchTerm"]

            if not search_term:
                messagebox.showwarning("Warning", "Please enter a search term.")
                return

            for item in self.tree.get_children():
                self.tree.delete(item)

            # Perform search using EmployeeRepository.search_books
            # Assuming EmployeeRepository.search_books returns a list of books matching the search criteria
            found_books = EmployeeRepository.search_books(search_field, search_term)

            # Insert found books into the treeview
            for book in found_books:
                self.tree.insert('', 'end', values=(
                    book.book_id, book.title, book.author, book.isbn, book.genre, book.shelf_location, book.status))

    def show_waiting_list_for_a_book(self):
        selected = self.tree.selection()
        if selected:
            book_id = self.tree.item(selected[0], 'values')[0]
            waiting_list = EmployeeRepository.get_waiting_list_for_a_book(book_id)
            PendingListDialog(self.window, waiting_list)

        else:
            messagebox.showwarning("Warning", "Please select a book to see its waiting list/pending list.")


class MemberDialog(tk.Toplevel):
    def __init__(self, parent, title="Member Details", initial_values=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)

        if initial_values is None:
            initial_values = {"Name": "", "Email": "", "Phone": "", "MembershipType": "", "MembershipStartDate": ""}

        self.result = None
        tk.Label(self, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.insert(0, initial_values["Name"])

        tk.Label(self, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        self.email_entry.insert(0, initial_values["Email"])

        tk.Label(self, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)
        self.phone_entry.insert(0, initial_values["Phone"])

        tk.Label(self, text="MembershipType:").grid(row=3, column=0, padx=5, pady=5)
        self.membership_type_entry = tk.Entry(self)
        self.membership_type_entry.grid(row=3, column=1, padx=5, pady=5)
        self.membership_type_entry.insert(0, initial_values["MembershipType"])

        tk.Label(self, text="MembershipStartDate:").grid(row=4, column=0, padx=5, pady=5)
        self.membership_start_date_entry = tk.Entry(self)
        self.membership_start_date_entry.grid(row=4, column=1, padx=5, pady=5)
        self.membership_start_date_entry.insert(0, initial_values["MembershipStartDate"])

        tk.Button(self, text="OK", command=self.on_add).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(self, text="Cancel", command=self.cancel).grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.grab_set()  # Make window modal
        self.wait_visibility()
        self.focus_set()

    def on_add(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        membership_type = self.membership_type_entry.get().strip()
        membership_start_date = self.membership_start_date_entry.get().strip()
        if not name or not email or not phone or not membership_type or not membership_start_date:
            messagebox.showerror("Error", "All fields are required.")
            return
        pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(pattern, email) is None:
            messagebox.showerror("Error", "Invalid email address. Example: Roni@gmail.com")
            return
        phone_pattern = re.compile(r'^05\d{8}$')
        if re.fullmatch(phone_pattern, phone) is None:
            messagebox.showerror("Error", "Invalid Phone number, example: 0502100781. 10 in length and starts with 05")
            return
        self.result = {"Name": name, "Email": email, "Phone": phone, "MembershipType": membership_type,
                       "MembershipStartDate": membership_start_date}
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result

    def cancel(self):
        self.result = None
        self.destroy()  # Close the Toplevel window


class SearchMemberDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent)
        self.title("Search Members")
        self.result = None

        options = ["name", "id", "email"]
        self.var = tk.StringVar(self)
        self.var.set(options[0])  # Set default option

        tk.Label(self, text="Search by:").grid(row=0, column=0, padx=5, pady=5)
        self.dropdown = tk.OptionMenu(self, self.var, *options)
        self.dropdown.config(bg="white", fg="black", font=('Microsoft YaHei UI Light', 11), bd=1, relief="solid")
        self.dropdown.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Enter search term:").grid(row=1, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self, text="Search", command=self.on_search).grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(self, text="Cancel", command=self.cancel).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    def on_search(self):
        search_field = self.var.get()  # Get the selected search field
        search_term = self.search_entry.get()  # Get the entered search term
        self.result = {"SearchField": search_field, "SearchTerm": search_term}
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result

    def cancel(self):
        self.result = None
        self.destroy()


class MemberManagementGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Member Management System")
        self.window.geometry("1300x600")
        self.window.config(bg="#fff")
        self.window.resizable(False, False)
        self.window.iconbitmap("icons/User.ico")
        self.icons = {}
        # Frame for Treeview and Scrollbar for improved responsiveness
        tree_frame = ttk.Frame(window)
        tree_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame,
                                 columns=("Id", "Name", "Email", "Phone", "MembershipType", "MembershipStartDate"),
                                 show="headings")
        self.tree.heading("Id", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("MembershipType", text="MembershipType")
        self.tree.heading("MembershipStartDate", text="MembershipStartDate")
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10)
        window.grid_columnconfigure(0, weight=1)

        icon_names = ['add_member', 'edit_member', 'delete_member', 'search', 'refresh']
        actions = [self.add_member, self.update_member, self.delete_member, self.search, self.refresh_member_list]
        for i, (icon_name, action) in enumerate(zip(icon_names, actions)):
            icon_path = f'images/{icon_name}.png'
            self.icons[icon_name] = PhotoImage(file=icon_path)

            button = ttk.Button(btn_frame, text=f"{icon_name}", image=self.icons[icon_name], compound="left",
                                command=action)
            button.grid(row=0, column=i, padx=1, pady=1, sticky='ew')
            btn_frame.grid_columnconfigure(i, weight=1)
        self.refresh_member_list()
        # Make window modal
        self.window.grab_set()
        self.window.wait_visibility()
        self.window.focus_set()

    def refresh_member_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for member_tuple in EmployeeRepository.get_members():
            # Assuming member_tuple contains (member_id, name, email, phone, membership_type, membership_start_date)
            self.tree.insert('', 'end', values=member_tuple)

    def add_member(self):
        dialog = MemberDialog(self.window)
        dialog.show()
        result = dialog.result
        if result:  # Check if result is not None
            member = Member(name=result["Name"], email=result["Email"], phone=result["Phone"],
                            membership_type=result["MembershipType"],
                            membership_start_date=result["MembershipStartDate"])
            EmployeeRepository.add_member(member)
            self.refresh_member_list()

    def update_member(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0], 'values')
            initial_values = {"id": item[0], "Name": item[1], "Email": item[2], "Phone": item[3],
                              "MembershipType": item[4],
                              "MembershipStartDate": item[5]}
            dialog = MemberDialog(self.window, "Update Member", initial_values)
            result = dialog.show()
            if result:  # Check if result is not None
                member = Member(result["Name"], result["Email"], result["Phone"], result["MembershipType"],
                                result["MembershipStartDate"],
                                initial_values["id"])
                EmployeeRepository.update_member(member)
                self.refresh_member_list()
        else:
            messagebox.showwarning("Warning", "Please select a book to update.")

    def delete_member(self):
        selected = self.tree.selection()
        if selected:
            member_id = self.tree.item(selected[0], 'values')[0]
            EmployeeRepository.delete_member(member_id)
            self.refresh_member_list()
        else:
            messagebox.showwarning("Warning", "Please select a user to delete.")

    def search(self):
        dialog = SearchMemberDialog(self.window)
        result = dialog.show()
        if result:
            search_field = result["SearchField"]
            search_term = result["SearchTerm"]

            if not search_term:
                messagebox.showwarning("Warning", "Please enter a search term.")
                return

            for item in self.tree.get_children():
                self.tree.delete(item)

            # Perform search using EmployeeRepository.search_books
            # Assuming EmployeeRepository.search_books returns a list of books matching the search criteria
            found_members = EmployeeRepository.search_members(search_field, search_term)

            # Insert found books into the treeview
            for member in found_members:
                self.tree.insert('', 'end', values=(
                    member.member_id, member.name, member.email, member.phone, member.membership_type,
                    member.membership_start_date))


# the dialog only the manager can use
class EmployeeDialog(tk.Toplevel):
    def __init__(self, parent, title="Employee Details", initial_values=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)

        if initial_values is None:
            initial_values = {"Name": "", "Email": "", "Phone": "", "EmployeeType": ""}

        self.result = None
        tk.Label(self, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.insert(0, initial_values["Name"])

        tk.Label(self, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        self.email_entry.insert(0, initial_values["Email"])

        tk.Label(self, text="Phone:").grid(row=2, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)
        self.phone_entry.insert(0, initial_values["Phone"])

        tk.Label(self, text="EmployeeType:").grid(row=3, column=0, padx=5, pady=5)
        self.employee_type_entry = tk.Entry(self)
        self.employee_type_entry.grid(row=3, column=1, padx=5, pady=5)
        self.employee_type_entry.insert(0, initial_values["EmployeeType"])

        tk.Button(self, text="OK", command=self.on_add).grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(self, text="Cancel", command=self.cancel).grid(row=6, column=0, columnspan=2, padx=5, pady=5)
        self.grab_set()  # Make window modal
        self.wait_visibility()
        self.focus_set()

    def on_add(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        employee_type = self.employee_type_entry.get().strip()
        if not name or not email or not phone or not employee_type:
            messagebox.showerror("Error", "All fields are required.")
            return
        pattern = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(pattern, email) is None:
            messagebox.showerror("Error", "Invalid email address. Example: Roni@gmail.com")
            return
        phone_pattern = re.compile(r'^05\d{8}$')
        if re.fullmatch(phone_pattern, phone) is None:
            messagebox.showerror("Error", "Invalid Phone number, example: 0502100781. 10 in length and starts with 05")
            return

        self.result = {"Name": name, "Email": email, "Phone": phone, "EmployeeType": employee_type,
                       }
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result

    def cancel(self):
        self.result = None
        self.destroy()  # Close the Toplevel window


# this is what the Manager has access to
class EmployeeManagementGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Employee Management System")
        self.window.geometry("1200x600")
        self.window.config(bg="#fff")
        self.window.resizable(False, False)
        self.window.iconbitmap("icons/employee.ico")
        self.icons = {}
        # Frame for Treeview and Scrollbar for improved responsiveness
        tree_frame = ttk.Frame(window)
        tree_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame,
                                 columns=("Id", "Name", "Email", "Phone", "EmployeeType"),
                                 show="headings")
        self.tree.heading("Id", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("EmployeeType", text="EmployeeType")
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10)
        window.grid_columnconfigure(0, weight=1)

        icon_names = ['add_employee', 'delete_employee']
        actions = [self.add_employee, self.delete_employee]
        for i, (icon_name, action) in enumerate(zip(icon_names, actions)):
            # it acts as an icon but its is png i just resized the image to be 25px*25px
            icon_path = f'images/{icon_name}.png'
            self.icons[icon_name] = PhotoImage(file=icon_path)

            button = ttk.Button(btn_frame, text=f"{icon_name}", image=self.icons[icon_name], compound="left",
                                command=action)
            button.grid(row=0, column=i, padx=1, pady=1, sticky='ew')
            btn_frame.grid_columnconfigure(i, weight=1)
        self.refresh_employee_list()
        # Make window modal
        self.window.grab_set()
        self.window.wait_visibility()
        self.window.focus_set()

    def refresh_employee_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for employee_tuple in EmployeeRepository.get_employees():
            self.tree.insert('', 'end', values=employee_tuple)

    def add_employee(self):
        dialog = EmployeeDialog(self.window)
        dialog.show()
        result = dialog.result
        if result:  # Check if result is not None
            employee = Employee(name=result["Name"], email=result["Email"], phone=result["Phone"],
                                employee_type=result["EmployeeType"],
                                )
            EmployeeRepository.add_employee(employee)
            self.refresh_employee_list()

    def delete_employee(self):
        selected = self.tree.selection()
        if selected:
            employee_id = self.tree.item(selected[0], 'values')[0]
            EmployeeRepository.delete_employee(employee_id)
            self.refresh_employee_list()
        else:
            messagebox.showwarning("Warning", "Please select a user to delete.")


# in here we'll do do the gui for the loans and the reports/statistics of the data in the db

# --------------------------------------------------------------------------------------------

# this class will display the returned books (the history of the loaned books)
class ReturnedLoansGui:
    def __init__(self):
        self.root = Tk()
        self.root.title("Returned Book")
        self.root.geometry("1250x600")
        self.root.config(bg="#fff")
        self.root.resizable(False, False)

        # Create tree frame
        label_title = ttk.Label(self.root, text="History / Returned Books", font=("Helvetica", 12, "bold"))
        label_title.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        tree_frame = ttk.Frame(self.root)
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("LoanID", "BookID", "MemberID", "LoanDate", "DueDate", "ReturnDate"),
                                 show="headings")
        self.tree.heading("LoanID", text="LoanID")
        self.tree.heading("BookID", text="BookID")
        self.tree.heading("MemberID", text="MemberID")
        self.tree.heading("LoanDate", text="LoanDate")
        self.tree.heading("DueDate", text="DueDate")
        self.tree.heading("ReturnDate", text="ReturnDate")
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Create button frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10)

        self.show_returned_books()
        # Start main event loop
        self.root.mainloop()

    def show_returned_books(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for loans_tuple in EmployeeRepository.get_returned_loaned_books():
            self.tree.insert('', 'end', values=loans_tuple)


"""
 shows the loaned books in a certain month the init function takes a month parameter that will be taken from the
 loans in a month button that is in the LoanedBooksReportsAndStatisticsManagementGui frame
"""


class LoansInMonthGUI:
    def __init__(self, month):
        self.root = Tk()
        self.month = month
        self.root.title("Returned Book")
        self.root.geometry("1250x600")
        self.root.config(bg="#fff")
        self.root.resizable(False, False)
        label_title = ttk.Label(self.root, text=f"loaned books in this month: {month}", font=("Helvetica", 12, "bold"))
        label_title.grid(row=0, column=0, columnspan=2, pady=(10, 5))
        # Create tree frame
        tree_frame = ttk.Frame(self.root)
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("LoanID", "BookID", "MemberID", "LoanDate", "DueDate", "ReturnDate"),
                                 show="headings")
        self.tree.heading("LoanID", text="LoanID")
        self.tree.heading("BookID", text="BookID")
        self.tree.heading("MemberID", text="MemberID")
        self.tree.heading("LoanDate", text="LoanDate")
        self.tree.heading("DueDate", text="DueDate")
        self.tree.heading("ReturnDate", text="ReturnDate")
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Create button frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10)
        self.all_loans_in_a_certain_month()
        # Start main event loop
        self.root.mainloop()

    def all_loans_in_a_certain_month(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for loans_tuple in EmployeeRepository.all_loans_in_a_month(self.month):
            self.tree.insert('', 'end', values=loans_tuple)


# this class will display the outcome/output of the loans between dates function
class LoansBetweenDates:
    def __init__(self, date_1, date_2):
        self.root = Tk()
        self.date_1 = date_1
        self.date_2 = date_2
        self.root.title("Returned Book")
        self.root.geometry("1250x600")
        self.root.config(bg="#fff")
        self.root.resizable(False, False)
        label_title = ttk.Label(self.root, text=f"loaned books between {date_1} and {date_2}",
                                font=("Helvetica", 12, "bold"))
        label_title.grid(row=0, column=0, columnspan=2, pady=(10, 5))
        # Create tree frame
        tree_frame = ttk.Frame(self.root)
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("LoanID", "BookID", "MemberID", "LoanDate", "DueDate", "ReturnDate"),
                                 show="headings")
        self.tree.heading("LoanID", text="LoanID")
        self.tree.heading("BookID", text="BookID")
        self.tree.heading("MemberID", text="MemberID")
        self.tree.heading("LoanDate", text="LoanDate")
        self.tree.heading("DueDate", text="DueDate")
        self.tree.heading("ReturnDate", text="ReturnDate")
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.loans_between_dates()
        # Create button frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10)
        # Start main event loop
        self.root.mainloop()

    def loans_between_dates(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for loans_tuple in EmployeeRepository.loans_between_dates(self.date_1, self.date_2):
            self.tree.insert('', 'end', values=loans_tuple)


# this function gets the top x (x-number) loaned books in a certain month
class MostLoanedBooks:
    def __init__(self, date, number):
        self.root = Tk()
        self.date = date
        self.number = number
        self.root.title("Most Loaned Books")
        self.root.geometry("450x300")
        self.root.config(bg="#fff")
        self.root.resizable(False, False)
        label_title = ttk.Label(self.root, text=f"top {number} most loaned book in this month : {date}",
                                font=("Helvetica", 12, "bold"))
        label_title.grid(row=0, column=0, columnspan=2, pady=(10, 5))
        # Create tree frame
        tree_frame = ttk.Frame(self.root)
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("Title", "titleCount"),
                                 show="headings")
        self.tree.heading("Title", text="Title")
        self.tree.heading("titleCount", text="TitleCount")

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.most_loaned_books()
        # Create button frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=1, column=0, sticky='ew', padx=10)
        # Start main event loop
        self.root.mainloop()

    def most_loaned_books(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for loans_tuple in EmployeeRepository.get_top_loaned_books(self.date, self.number):
            self.tree.insert('', 'end', values=loans_tuple)


class LoanedBooksReportsAndStatisticsManagementGui:
    def __init__(self, window):
        self.window = window
        self.window.title("Reports&Statistics for loaned books")
        self.window.geometry("1250x600")
        self.window.config(bg="#fff")
        self.window.resizable(False, False)
        self.window.iconbitmap("icons/reports.ico")
        self.icons = {}
        label_title = ttk.Label(window, text="Current Loaned Books", font=("Helvetica", 12, "bold"))
        label_title.grid(row=0, column=0, columnspan=2, pady=(10, 5))
        # Frame for Treeview and Scrollbar for improved responsiveness
        tree_frame = ttk.Frame(window)
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("LoanID", "BookID", "MemberID", "LoanDate", "DueDate", "ReturnDate"),
                                 show="headings")
        self.tree.heading("LoanID", text="LoanID")
        self.tree.heading("BookID", text="BookID")
        self.tree.heading("MemberID", text="MemberID")
        self.tree.heading("LoanDate", text="LoanDate")
        self.tree.heading("DueDate", text="DueDate")
        self.tree.heading("ReturnDate", text="ReturnDate")
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=2, column=0, sticky='ew', padx=10)
        # Configure each column with equal weight
        for i in range(4):
            btn_frame.grid_columnconfigure(i, weight=1)
        # to style the button using ttk customizations
        style = ttk.Style()
        style.configure('Custom.TButton', background='blue', font=('Helvetica', 9),
                        padding=3, borderwidth=0)

        # Button to show all loans
        all_loans_btn = ttk.Button(btn_frame, text="Returned Loans", style='Custom.TButton',
                                   cursor='hand2', command=ReturnedLoansGui
                                   )
        all_loans_btn.grid(row=0, column=0, padx=5, pady=(10, 20))

        # Frame for loans in a certain month
        loans_month_frame = ttk.Frame(btn_frame)
        loans_month_frame.grid(row=0, column=1, padx=5)
        ttk.Label(loans_month_frame, text="Loans in a Month").grid(row=0, column=0, pady=5)
        self.certain_month_entry = ttk.Entry(loans_month_frame)
        self.certain_month_entry.grid(row=1, column=0, padx=5, pady=10)
        ttk.Label(loans_month_frame, text="Enter month (e.g., 1-12)").grid(row=1, column=1, padx=5, pady=10)
        submit_month_btn = ttk.Button(loans_month_frame, text="Submit", style='Custom.TButton',
                                      cursor='hand2', command=self.show_loans_in_month)
        submit_month_btn.grid(row=2, column=0, padx=5, pady=(10, 20))

        # Frame for loans between two dates
        loans_dates_frame = ttk.Frame(btn_frame)
        loans_dates_frame.grid(row=0, column=2, padx=5)
        ttk.Label(loans_dates_frame, text="Loans Between Dates").grid(row=0, column=0, pady=5)
        self.start_date_entry = ttk.Entry(loans_dates_frame)
        self.start_date_entry.grid(row=1, column=0, padx=5, pady=10)
        ttk.Label(loans_dates_frame, text="Start Date (YYYY-MM-DD)").grid(row=1, column=1, padx=5, pady=10)
        self.end_date_entry = ttk.Entry(loans_dates_frame)
        self.end_date_entry.grid(row=2, column=0, padx=5, pady=10)
        ttk.Label(loans_dates_frame, text="End Date (YYYY-MM-DD)").grid(row=2, column=1, padx=5, pady=10)
        submit_dates_btn = ttk.Button(loans_dates_frame, text="Submit", style='Custom.TButton',
                                      cursor='hand2', command=self.show_loans_between_dates)
        submit_dates_btn.grid(row=3, column=0, padx=5, pady=(10, 20))

        # Frame for most loaned books in a certain month (sorted from the highest to lowest)
        most_loaned_books_frame = ttk.Frame(btn_frame)
        most_loaned_books_frame.grid(row=0, column=3, padx=5)
        ttk.Label(most_loaned_books_frame, text="Most Loaned Books").grid(row=0, column=0, pady=5)
        self.month_entry = ttk.Entry(most_loaned_books_frame)
        self.month_entry.grid(row=1, column=0, padx=5, pady=10)
        ttk.Label(most_loaned_books_frame, text="Enter month (e.g., 1-12)").grid(row=1, column=1, padx=5, pady=10)
        self.num_entry = ttk.Entry(most_loaned_books_frame)
        self.num_entry.grid(row=2, column=0, padx=5, pady=10)
        ttk.Label(most_loaned_books_frame, text="Enter number (for top loaned books)").grid(row=2, column=1, padx=5,
                                                                                            pady=10)
        submit_famous_btn = ttk.Button(most_loaned_books_frame, text="Submit", style='Custom.TButton',
                                       cursor='hand2', command=self.show_most_loaned_books)
        submit_famous_btn.grid(row=3, column=0, padx=5, pady=(10, 20))
        self.show_current_loans()
        self.window.grab_set()
        self.window.wait_visibility()
        self.window.focus_set()

    def show_current_loans(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for loans_tuple in EmployeeRepository.get_current_loaned_books():
            self.tree.insert('', 'end', values=loans_tuple)

    def show_loans_in_month(self):
        month = self.certain_month_entry.get()
        if month:
            if int(month) >= 1 and int(month) <= 12:
                LoansInMonthGUI(month)
            else:
                messagebox.showerror("Error", "Month must be in between 1-12!")
        else:
            messagebox.showerror("Error", "Month field are required!")

    def show_loans_between_dates(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        if start_date and end_date:
            LoansBetweenDates(start_date, end_date)
        else:
            messagebox.showerror("Error", "All fields are required!")

    def show_most_loaned_books(self):
        month = self.month_entry.get()
        number = self.num_entry.get()
        if month and number:
            if (int(month) >= 1 and int(month) <= 12) and int(number)>0:
                MostLoanedBooks(month, number)
            else:
                messagebox.showerror("Error", "month (1-12) input or number (positive) input is incorrect!")

        else:
            messagebox.showerror("Error", "All fields are required!")


# this is a menu for the employee/manager
class MenuForEmployee:
    def __init__(self, employee):
        self.root = Tk()
        self.root.title("Menu")
        self.root.geometry("925x500")
        self.root.config(bg="#fff")
        self.root.resizable(False, False)
        img = PhotoImage(file='images/menu.png')
        Label(self.root, image=img, bg='white').place(x=50, y=50)
        self.frame = Frame(self.root, width=350, height=350, bg="white")
        self.frame.place(x=480, y=80)
        heading = Label(self.frame, text='Menu', fg='#57a1f8', bg='white',
                        font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=130, y=5)

        self.Book_management = Button(self.frame, width=39, pady=7, text='Book management', bg='#57a1f8', fg='white',
                                      cursor='hand2',
                                      border=0, command=self.open_book_management)
        self.Book_management.place(x=45, y=80)
        self.Member_management = Button(self.frame, width=39, pady=7, text='Member management', bg='#57a1f8',
                                        fg='white',
                                        cursor='hand2',
                                        border=0, command=self.open_member_management)
        self.Member_management.place(x=45, y=140)
        self.Reports_Statistics = Button(self.frame, width=39, pady=7, text='Reports&Statistics', bg='#57a1f8',
                                         fg='white',
                                         cursor='hand2',
                                         border=0, command=self.open_reports_and_statistics_management)
        self.Reports_Statistics.place(x=45, y=200)
        # only if the employee who Logged in happens to be the manager then he can get access to the employee management
        if employee[4] == "Manager":
            self.Employee_management = Button(self.frame, width=39, pady=7, text='Employee management', bg='#57a1f8',
                                              fg='white',
                                              cursor='hand2',
                                              border=0, command=self.open_employee_management)
            self.Employee_management.place(x=45, y=260)
        self.root.grab_set()
        self.root.wait_visibility()
        self.root.focus_set()

        self.root.mainloop()

    def open_book_management(self):
        book_management_window = Toplevel(self.root)
        BookManagementGUI(book_management_window)

    def open_member_management(self):
        member_management_window = Toplevel(self.root)
        MemberManagementGUI(member_management_window)

    def open_employee_management(self):
        employee_management_window = Toplevel(self.root)
        EmployeeManagementGUI(employee_management_window)

    def open_reports_and_statistics_management(self):
        reports_and_statistics_management_window = Toplevel(self.root)
        LoanedBooksReportsAndStatisticsManagementGui(reports_and_statistics_management_window)


# ---------------------------------------------------------------------------------------------
# in this part of the code we will handle the gui for the member
class LibraryGUI:
    def __init__(self, window, member):
        self.window = window
        self.member = member
        self.window.title("Library")
        self.window.geometry("1400x600")
        self.window.config(bg="#fff")
        self.window.resizable(False, False)
        self.window.iconbitmap("icons/bookIcon.ico")
        self.icons = {}
        label_title = ttk.Label(window, text="Library", font=("Helvetica", 12, "bold"))
        label_title.grid(row=0, column=0, columnspan=2, pady=(10, 5))
        # Frame for Treeview and Scrollbar for improved responsiveness
        tree_frame = ttk.Frame(window)
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        # Treeview setup
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("id", "title", "author", "ISBN", "genre", "ShelfLocation", "status"),
                                 show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("genre", text="Genre")
        self.tree.heading("ShelfLocation", text="ShelfLocation")
        self.tree.heading("status", text="Status")
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=2, column=0, sticky='ew', padx=10)
        window.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('Custom.TButton', background='blue', font=('Helvetica', 9),
                        padding=3, borderwidth=0)

        icon_names = ['take_book', 'waiting_list', 'search', 'refresh']
        actions = [self.loan_a_book, self.join_waiting_list, self.search, self.refresh]
        for i, (icon_name, action) in enumerate(zip(icon_names, actions)):
            icon_path = f'images/{icon_name}.png'
            self.icons[icon_name] = PhotoImage(file=icon_path)

            button = ttk.Button(btn_frame, text=f"{icon_name}", image=self.icons[icon_name], compound="left",
                                command=action)
            button.grid(row=0, column=i, padx=1, pady=1, sticky='ew')
            btn_frame.grid_columnconfigure(i, weight=1)
        self.refresh_book_list()
        self.window.grab_set()
        self.window.wait_visibility()
        self.window.focus_set()

        self.window.mainloop()

    def refresh_book_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in EmployeeRepository.get_books():
            self.tree.insert('', 'end', values=(
                book.book_id, book.title, book.author, book.isbn, book.genre, book.shelf_location, book.status))

    def loan_a_book(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0], 'values')
            if item[6] == "Available":
                member_id = self.member[0]
                book_id = item[0]
                # check if this member is the one at the top of the waiting list or if there is no waiting list for the book
                if not EmployeeRepository.get_waiting_list_for_a_book(
                        book_id) or member_id == EmployeeRepository.get_first_member_in_waiting_list(
                    book_id):
                    # item[0] is the book id and member[0] is the member's id
                    loan = Loan(item[0], member_id)
                    EmployeeRepository.register_a_loan_book(loan)
                    # after the user gets the book we delete him from the waiting list (delete the top user in waiting list)
                    EmployeeRepository.delete_from_waiting_list(member_id, book_id)
                    self.refresh_book_list()
                else:
                    messagebox.showwarning("Warning",
                                           "there are members waiting for this book,you may join the waiting list. ")
            else:
                messagebox.showwarning("Warning", "This book is currently Unavailable, you may join the waiting list.")
        else:
            messagebox.showwarning("Warning", "Please select a book to loan.")

    def search(self):
        BookManagementGUI.search(self)

    def refresh(self):
        BookManagementGUI.refresh_book_list(self)

    def join_waiting_list(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0], 'values')
            book_id = item[0]
            member_id = self.member[0]
            # check if the member got the book currently loaned with him
            if EmployeeRepository.get_current_loaned_books_for_specific_member_and_book(member_id, book_id):
                messagebox.showwarning("Warning", "you currently have this book loaned!")
                return
            # check if the book is available and the waiting list for it is empty
            if item[6] == "Available" and not EmployeeRepository.get_waiting_list_for_a_book(
                    book_id):
                messagebox.showwarning("Warning",
                                       "there is no waiting list on this book, you are allowed to borrow it.")
                return
            # checks if the member is already listed in the waiting list
            if EmployeeRepository.member_in_waiting_list(member_id, book_id) is True:
                messagebox.showwarning("Warning", "Member already exists in this waiting list.")
                return
            EmployeeRepository.add_to_waiting_list(book_id, member_id)
        else:
            messagebox.showwarning("Warning", "Please select a book join the waiting list for.")
            return


class CurrentLoanedBooksGui:
    def __init__(self, window, member):
        self.window = window
        self.member = member
        self.window.title("Current Loaned Books")
        self.window.geometry("1450x600")
        self.window.config(bg="#fff")
        self.window.resizable(False, False)
        self.window.iconbitmap("icons/bookIcon.ico")
        self.icons = {}
        label_title = ttk.Label(window, text=f"Books borrowed by Member {member[1]} (ID: {member[0]})",
                                font=("Helvetica", 12, "bold"))
        label_title.grid(row=0, column=0, columnspan=2, pady=(10, 5))
        # Frame for Treeview and Scrollbar for improved responsiveness
        tree_frame = ttk.Frame(window)
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # Treeview setup
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("loanID", "bookID", "title", "author", "ISBN", "genre", "LoanDate"),
                                 show="headings")
        self.tree.heading("loanID", text="Loan ID")
        self.tree.heading("bookID", text="book ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("genre", text="Genre")
        self.tree.heading("LoanDate", text="LoanDate")
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Frame for buttons
        btn_frame = ttk.Frame(window)
        btn_frame.grid(row=2, column=0, sticky='ew', padx=10)
        window.grid_columnconfigure(0, weight=1)

        # Center the frame within the window
        btn_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=(10, 20))

        style = ttk.Style()
        style.configure('Custom.TButton', background='blue', font=('Helvetica', 9),
                        padding=3, borderwidth=0)

        # Load the image
        image_path = f'images/return_book.png'
        self.image = tk.PhotoImage(file=image_path)

        # Create the button
        return_a_book = ttk.Button(btn_frame, text="Return This Book", style='Custom.TButton', cursor='hand2',
                                   command=self.return_a_book, image=self.image, compound='left')
        return_a_book.grid(row=0, column=0, padx=5, pady=(10, 20), sticky='nsew')

        # Center the button within the frame
        btn_frame.grid_rowconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(0, weight=1)
        self.refresh_current_loaned_book_list()
        self.window.grab_set()
        self.window.wait_visibility()
        self.window.focus_set()

        self.window.mainloop()

    def refresh_current_loaned_book_list(self):
        member_id = self.member[0]
        for item in self.tree.get_children():
            self.tree.delete(item)
        for loaned_book in EmployeeRepository.get_current_loaned_books_for_specific_member(member_id):
            self.tree.insert('', 'end', values=(
                loaned_book[0], loaned_book[1], loaned_book[2], loaned_book[3], loaned_book[4],
                loaned_book[5], loaned_book[6]))

    def return_a_book(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0], 'values')
            EmployeeRepository.return_a_lend_book(item[0], item[1])
            self.refresh_current_loaned_book_list()
        else:
            messagebox.showwarning("Warning", "Please select a book to loan.")


class LoansHistoryGUI:
    def __init__(self, window, member):
        self.window = window
        self.member = member
        self.window.title("Book Loans History")
        self.window.geometry("1450x600")
        self.window.config(bg="#fff")
        self.window.resizable(False, False)
        self.window.iconbitmap("icons/bookIcon.ico")
        self.icons = {}
        label_title = ttk.Label(window,
                                text=f"Books that have been returned by Member {member[1]} (ID: {member[0]})",
                                font=("Helvetica", 12, "bold"))
        label_title.grid(row=0, column=0, columnspan=2, pady=(10, 5))
        # Frame for Treeview and Scrollbar for improved responsiveness
        tree_frame = ttk.Frame(window)
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # Treeview setup
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("loanID", "bookID", "title", "author", "ISBN", "genre", "LoanDate"),
                                 show="headings")
        self.tree.heading("loanID", text="Loan ID")
        self.tree.heading("bookID", text="book ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("genre", text="Genre")
        self.tree.heading("LoanDate", text="LoanDate")
        self.tree.grid(row=0, column=0, sticky='nsew')

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.refresh_returned_loaned_book_list()
        self.window.grab_set()
        self.window.wait_visibility()
        self.window.focus_set()

        self.window.mainloop()

    def refresh_returned_loaned_book_list(self):
        member_id = self.member[0]
        for item in self.tree.get_children():
            self.tree.delete(item)
        for loaned_book in EmployeeRepository.get_returned_loaned_books_for_specific_member(member_id):
            self.tree.insert('', 'end', values=(
                loaned_book[0], loaned_book[1], loaned_book[2], loaned_book[3], loaned_book[4],
                loaned_book[5], loaned_book[6]))


class MenuForUser:
    def __init__(self, member):
        self.root = Tk()
        self.member = member
        self.root.title("User's Menu")
        self.root.geometry("925x500")
        self.root.config(bg="#fff")
        self.root.resizable(False, False)
        img = PhotoImage(file='images/user_menu.png')
        Label(self.root, image=img, bg='white').place(x=10, y=10)
        self.root.iconbitmap("icons/User.ico")
        self.frame = Frame(self.root, width=350, height=350, bg="white")
        self.frame.place(x=480, y=80)
        heading = Label(self.frame, text='Menu', fg='#57a1f8', bg='white',
                        font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=130, y=5)
        self.Library = Button(self.frame, width=39, pady=7, text='Library', bg='#57a1f8', fg='white',
                              cursor='hand2',
                              border=0, command=self.open_library)
        self.Library.place(x=45, y=80)
        self.Loaned_Books = Button(self.frame, width=39, pady=7, text='Current Loaned Books', bg='#57a1f8',
                                   fg='white',
                                   cursor='hand2',
                                   border=0, command=self.open_current_loaned_books)
        self.Loaned_Books.place(x=45, y=140)
        self.Loans_History = Button(self.frame, width=39, pady=7, text='Loans History', bg='#57a1f8',
                                    fg='white',
                                    cursor='hand2',
                                    border=0, command=self.open_loan_history)
        self.Loans_History.place(x=45, y=200)
        self.root.grab_set()
        self.root.wait_visibility()
        self.root.focus_set()

        self.root.mainloop()

    def open_library(self):
        library_window = Toplevel(self.root)
        LibraryGUI(library_window, self.member)

    def open_current_loaned_books(self):
        current_loaned_books_window = Toplevel(self.root)
        CurrentLoanedBooksGui(current_loaned_books_window, self.member)

    def open_loan_history(self):
        loan_history_window = Toplevel(self.root)
        LoansHistoryGUI(loan_history_window, self.member)


if __name__ == '__main__':
    # remember to use DBmanager once and then put it in '#'
    #DBManager.init_connection()
    login = LoginGui()
    login.root.mainloop()
