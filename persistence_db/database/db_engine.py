import sqlite3


class DatabaseEngine:

    def __init__(self):

        self.conn = sqlite3.connect(
            "nuvibank.db"
        )

        self.cursor = self.conn.cursor()

    def initialize(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS runtime_state (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            system TEXT,

            status TEXT,

            latency INTEGER
        )

        """)

        self.conn.commit()

    def insert_state(
        self,
        system,
        status,
        latency
    ):

        self.cursor.execute("""

        INSERT INTO runtime_state (
            system,
            status,
            latency
        )

        VALUES (?, ?, ?)

        """, (

            system,
            status,
            latency
        ))

        self.conn.commit()

    def fetch_all(self):

        self.cursor.execute("""

        SELECT * FROM runtime_state

        """)

        return self.cursor.fetchall()
