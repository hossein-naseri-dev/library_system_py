"""
DATABASE Relation's in project
"""
import sqlite3
from utils.config import DATABASE_PATH, get_current_user

# Create Required Table's if not exists
with sqlite3.connect(DATABASE_PATH) as conn:
    """Create Required Table's if not exists"""

    cursor = conn.cursor()

    # Create users table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        "username"	TEXT NOT NULL UNIQUE,
                        "password"	TEXT NOT NULL,
                        PRIMARY KEY("username")
                    );
                   ''')


    # Create books table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        "book_id" INTEGER NOT NULL UNIQUE,
                        "title"	TEXT NOT NULL UNIQUE,
                        "author" TEXT NOT NULL,
                        "year" INTEGER NOT NULL,
                        "translator" TEXT,
                        "publisher" TEXT,
                        "owner"	TEXT NOT NULL,
                        PRIMARY KEY("book_id" AUTOINCREMENT)
                        FOREIGN KEY ("owner") REFERENCES users("username")
                    );
                   ''')


    conn.commit()


def login_query(username, password):
    """Check if username and password are correct"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            statement = (f"SELECT username, password FROM users WHERE username='"
                         f"{username}' AND password='{password}';")
            cursor.execute(statement)
            if not cursor.fetchone():
                return None
            else:
                return username
    except Exception as e:
        print(e)


def create_user_query(username, password):
    """Create a new user in database -> users"""
    try:
        if login_query(username, password):
            return 0
        else:
            with sqlite3.connect(DATABASE_PATH) as conn:
                cursor = conn.cursor()
                statement = (
                    f"INSERT INTO users VALUES ('{username}', '{password}');"
                )
                cursor.execute(statement)
                conn.commit()
                return 1
    except sqlite3.Error:
        return -1


def add_book_query(title, author, year, owner, translator=None, publisher=None):
    """Add a book to the database"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            statement = """INSERT INTO books
                         (title, author, year, translator, publisher, owner)
                SELECT ?, ?, ?, ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM books
                    WHERE title = ? AND author = ?
                );
            """
            data_tuple = (
                title, author, year, translator, publisher, owner, title, author
            )
            cursor.execute(statement, data_tuple)
            conn.commit()
    except sqlite3.Error as e:
        print(f"ERROR ADDING BOOK: {e}")


def update_book_query(title, author, new_title=None, new_author=None, new_year=None,
                      new_translator=None, new_publisher=None, new_owner=None):
    """Update a book in the database"""

    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            fields = []
            params = []

            if new_title is not None:
                fields.append("title = ?")
                params.append(new_title)
            if new_author is not None:
                fields.append("author = ?")
                params.append(new_author)
            if new_year is not None:
                fields.append("year = ?")
                params.append(new_year)
            if new_translator is not None:
                fields.append("translator = ?")
                params.append(new_translator)
            if new_publisher is not None:
                fields.append("publisher = ?")
                params.append(new_publisher)
            if new_owner is not None:
                fields.append("owner = ?")
                params.append(new_owner)

            if not fields:
                return False

            params.append(title)
            params.append(author)

            statement = (f"UPDATE books SET {', '.join(fields)} "
                         f"WHERE title=? AND author=?")

            cursor.execute(statement, params)
            conn.commit()
    except sqlite3.Error as e:
        print(f"ERROR RENAME BOOK: {e}")


def delete_book_query(title, author):
    """Delete a book in the database"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            statement = (f"DELETE FROM books WHERE title=? AND author=?")
            cursor.execute(statement, (title, author))
            conn.commit()
    except sqlite3.Error as e:
        print(f"ERROR DELETE BOOK: {e}")


def read_books_table_query(owner):
    """Return all books in the database"""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            statement = (f"SELECT * FROM books WHERE owner=?")
            cursor.execute(statement, (owner,))
            books = cursor.fetchall()
            return books
    except sqlite3.Error as e:
        print(f"ERROR READ BOOKS: {e}")
