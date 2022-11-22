import sys
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from datetime import datetime

class Contacts:
    def __init__(self, db_path):
        self.db_path = db_path
        if not db_path.exists():
            print("Migrating db")
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute(
                """
                CREATE TABLE contacts(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
                );
                """)
            connection.commit()
            cursor.execute("CREATE UNIQUE INDEX index_contacts_email ON contacts(email);")
            connection.commit()
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row

    def insert_contacts(self, contacts):
        print("Inserting contacts ...")
        cursor = self.connection.cursor()
        cursor.executemany(""" 
            INSERT INTO contacts(name,email)
            VALUES(?,?)
        """,(contacts))

    def get_name_for_email(self, email):
        print("Looking for email", email)
        cursor = self.connection.cursor()
        start = datetime.now()
        cursor.execute(
            """
            SELECT * FROM contacts
            WHERE email = ?
            """,
            (email,),
        )
        row = cursor.fetchone()
        end = datetime.now()

        elapsed = end - start
        print("query took", elapsed.microseconds / 1000, "ms")
        if row:
            name = row["name"]
            print(f"Found name: '{name}'")
            return name
        else:
            print("Not found")


def yield_contacts(num_contacts):
    # TODO: Generate a lot of contacts
    # instead of just 3
    for i in range(num_contacts - 3) :
        yield("Alice" + str(i), "Alice" + str(i) + "@domain.tld")
    yield ("Alice", "alice@domain.tld")
    yield ("Bob", "bob@foo.com")
    yield ("Charlie", "charlie@acme.corp")

def drawGraph() :
    num_contacts = [10, 100, 1000, 10000, 50000, 10000, 1000000]
    times= []
    db_path = Path("contacts.sqlite3")
    for num in num_contacts:
        num_contacts = int(num)
        contacts = Contacts(db_path)
        contacts.insert_contacts(yield_contacts(num_contacts))
        start = datetime.now()
        charlie = contacts.get_name_for_email("charlie@acme.corp")
        end = datetime.now()
        elapsed = end - start
        times.append(elapsed)
    plt.plot(num_contacts, times)
    plt.show()
        

def main():
    num_contacts = int(sys.argv[1])
    db_path = Path("contacts.sqlite3")
    contacts = Contacts(db_path)
    contacts.insert_contacts(yield_contacts(num_contacts))
    charlie = contacts.get_name_for_email("charlie@acme.corp")

    #drawGraph()


if __name__ == "__main__":
    main()
