import sqlite3


class OperationDb:

    def __init__(self, username, points, table_name):
        self.username = username
        self.points = points
        self.table_name = table_name

    def insert_kring_points(self):
        try:
            sqliteConnection = sqlite3.connect('stats.db')
            cursor = sqliteConnection.cursor()

            cursor.execute("SELECT username FROM " + self.table_name + " WHERE username = ?", (self.username,))
            data = cursor.fetchall()
            if len(data) == 0:
                cursor.execute("INSERT INTO " + self.table_name + "(username, points) VALUES (?, ?)", (self.username, self.points))
            else:
                cursor.execute("UPDATE " + self.table_name + " SET points = points - " + str(self.points) + " WHERE username = ?",
                               (self.username,))

            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

    def insert_krasava_points(self):
        try:
            sqliteConnection = sqlite3.connect('stats.db')
            cursor = sqliteConnection.cursor()

            cursor.execute("SELECT username FROM " + self.table_name + " WHERE username = ?", (self.username,))
            data = cursor.fetchall()
            if len(data) == 0:
                cursor.execute("INSERT INTO " + self.table_name + "(username, points) VALUES (?, ?)", (self.username, self.points))
            else:
                cursor.execute("UPDATE " + self.table_name + " SET points = points + " + str(self.points) + " WHERE username = ?",
                               (self.username,))

            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

class InsertDB:

    def __init__(self, username, request_text, date, table_name):
        self.username = username
        self.request_text = request_text
        self.date = date
        self.table_name = table_name

    def insert_request_users(self):
        try:
            sqliteConnection = sqlite3.connect('stats.db')
            cursor = sqliteConnection.cursor()

            cursor.execute("INSERT INTO " + self.table_name + "(username, request_text, date) VALUES (?, ?, ?)", (self.username, self.request_text, self.date))

            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()                
