import sqlite3

class Database:
    def __init__(self, db_name="finance.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                type TEXT,
                category TEXT,
                amount REAL,
                date TEXT,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions_categories (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                transaction_type TEXT,
                category TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )

        """)
        self.conn.commit()

    def add_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user(self, username, password):
        self.cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone()

    def add_transaction(self, user_id, type, category, amount, date, description):
        self.cursor.execute("""
            INSERT INTO transactions (user_id, type, category, amount, date, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, type, category, amount, date, description))
        self.conn.commit()

    def get_transactions(self, user_id, category=None, date=None, type=None):
        query = "SELECT * FROM transactions WHERE user_id = ?"
        params = [user_id]
        if category:
            query += " AND category = ?"
            params.append(category)
        if date:
            query += " AND date = ?"
            params.append(date)
        if type:
            query += " AND type = ?"
            params.append(type)
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_transaction_to_export(self, user_id):
        self.cursor.execute("SELECT type, category, amount, date, description FROM transactions WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()
    
    def add_transaction_categories(self, user_id, transaction_type, category):
        self.cursor.execute("""
            INSERT INTO transactions_categories (user_id, transaction_type, category)
            VALUES (?, ?, ?)
        """, (user_id, transaction_type, category))
        self.conn.commit()

        

    def get_transactions_categories(self, user_id, transaction_type):
        self.cursor.execute("SELECT category FROM transactions_categories WHERE user_id = ? AND transaction_type = ?", (user_id, transaction_type))
        return self.cursor.fetchall()
    
    def delete_transaction(self, user_id, transaction_id):
        self.cursor.execute(
                "DELETE FROM transactions WHERE user_id = ? AND id = ?",
                (user_id, transaction_id),
            )
        self.conn.commit()

    def update_transaction(self, user_id, transaction_id, new_type, new_category, new_amount, new_date, new_description):
        self.cursor.execute(
                """
                UPDATE transactions
                SET type = ?, category = ?, amount = ?, date = ?, description = ?
                WHERE user_id = ? AND transaction_id = ?
                """,
                (
                    new_type,
                    new_category,
                    new_amount,
                    new_date,
                    new_description,
                    user_id,
                    transaction_id,
                ),
            )
        self.conn.commit()

    def close(self):
        self.conn.close()