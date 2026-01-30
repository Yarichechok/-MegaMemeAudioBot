import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_id TEXT,
                name TEXT,
                user_id INTEGER,
                is_public INTEGER DEFAULT 0,
                file_type TEXT DEFAULT 'voice'
            )
        """)
        self.connection.commit()

    def add_sound(self, file_id, name, user_id, is_public, file_type):
        self.cursor.execute("INSERT INTO sounds (file_id, name, user_id, is_public, file_type) VALUES (?, ?, ?, ?, ?)",
                            (file_id, name, user_id, is_public, file_type))
        self.connection.commit()

    def search_sounds(self, text, viewer_id):
        self.cursor.execute("""
            SELECT id, name, file_id, file_type FROM sounds
            WHERE name LIKE ? AND (is_public = 1 OR user_id = ?)
            ORDER BY id DESC LIMIT 50
        """, (f"%{text}%", viewer_id))
        return self.cursor.fetchall()

    def get_all_sounds(self, viewer_id):
        self.cursor.execute("""
            SELECT id, name, file_id, file_type FROM sounds
            WHERE is_public = 1 OR user_id = ?
            ORDER BY id DESC LIMIT 50
        """, (viewer_id,))
        return self.cursor.fetchall()

    def get_random_sound(self):
        self.cursor.execute("""
            SELECT file_id, name, file_type FROM sounds
            WHERE is_public = 1
            ORDER BY RANDOM() LIMIT 1
        """)
        return self.cursor.fetchone()

    def get_user_sounds(self, user_id):
        self.cursor.execute("SELECT id, name, file_id, file_type FROM sounds WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def delete_sound(self, sound_id):
        self.cursor.execute("DELETE FROM sounds WHERE id = ?", (sound_id,))
        self.connection.commit()

    def get_sound_owner(self, sound_id):
        self.cursor.execute("SELECT user_id FROM sounds WHERE id = ?", (sound_id,))
        res = self.cursor.fetchone()
        return res[0] if res else None