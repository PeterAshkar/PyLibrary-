import mysql
from DBManager import DBManager
from libraryEntities.User import Member


@staticmethod
def add_member(member):
    try:
        connection = DBManager.get_connection()
        sql_query = "INSERT INTO members (Name, Email, Phone, MembershipType, MembershipStartDate) " \
                    "VALUES (%s, %s, %s, %s, %s)"
        values = (member.name, member.email, member.phone, member.membership_type, member.membership_start_date)
        connection.cursor().execute(sql_query, values)
        connection.commit()
        connection.cursor().close()
        connection.close()
    except mysql.connector.Error as err:
        print("Error:", err)


@staticmethod
def update_member(member):
    try:
        connection = DBManager.get_connection()
        sql_query = "UPDATE members SET Name = %s, Email = %s, Phone = %s, MembershipType = %s," \
                    " MembershipStartDate = %s WHERE MemberID = %s"
        values = (
            member.name, member.email, member.phone, member.membership_type, member.membership_start_date,
            member.member_id)
        connection.cursor().execute(sql_query, values)
        connection.commit()
        connection.cursor().close()
        connection.close()
    except mysql.connector.Error as err:
        print("Error:", err)


def delete_member(member_id):
    try:
        connection = DBManager.get_connection()
        connection.cursor().execute("DELETE FROM members WHERE MemberID = %s", (member_id,))
        connection.commit()
        connection.cursor().close()
        connection.close()
    except mysql.connector.Error as err:
        print("Error:", err)


@staticmethod
# it takes 2 parameters (search_type and search_term) we look for the type of what we'll search for (title,id etc..)
# and then we search for the search_term which could the number of id or the name of the title etc...
def search_members(search_type, search_term):
    try:
        connection = DBManager.get_connection()
        if search_type == "name":
            sql_query = "SELECT * FROM members WHERE Name LIKE %s"
        elif search_type == "id":
            sql_query = "SELECT * FROM members WHERE MemberID LIKE %s"
        elif search_type == "email":
            sql_query = "SELECT * FROM members WHERE Email LIKE %s"
        else:
            print("Invalid search type")
            return None

        cursor = connection.cursor()
        cursor.execute(sql_query, ("%" + search_term + "%",))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        # if rows are empty
        if not rows:
            print("no such member!")
            return None
        return [Member(member_id=member_id, name=name, email=email, phone=phone, membership_type=membership_type,
                       membership_start_date=membership_start_date,
                       )
                for
                member_id, name, email, phone, membership_type, membership_start_date in
                rows]

    except mysql.connector.Error as error:
        print("Error:", error)
        return None


# this is a more optimal search for individual search and it's more convenient for the login checking
def search_a_certain_member(member_id):
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()  # Obtain cursor
        sql_query = "SELECT * FROM members WHERE MemberID LIKE %s"
        cursor.execute(sql_query, (member_id,))
        row = cursor.fetchone()  # Fetch one row
        if row is None:
            print("No employee found with ID:", member_id)
            return None
        else:
            # Process the fetched row
            cursor.close()
            connection.close()
            return row

    except mysql.connector.Error as error:
        print("Error:", error)
        return None


# this function helps me to get all the members that are in the system
def get_members():
    try:
        connection = DBManager.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM members")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except mysql.connector.Error as error:
        print("Error:", error)
        return None
