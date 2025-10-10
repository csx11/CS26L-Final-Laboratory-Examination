import sqlite3

DB_NAME = "user.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                language TEXT NOT NULL,
                level TEXT DEFAULT 'Beginner',
                words_learned INTEGER DEFAULT 0,
                speaking INTEGER DEFAULT 0,
                writing INTEGER DEFAULT 0,
                reading INTEGER DEFAULT 0,
                listening INTEGER DEFAULT 0
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                definition TEXT,
                language_category TEXT
            )
        """)
        
        conn.commit()

def add_user(username, language):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, language) 
            VALUES (?, ?)
        """, (username, language))
        conn.commit()
        return cur.lastrowid

def get_all_users():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        return cur.fetchall()

def update_user(user_id, language, level, words_learned, speaking, writing, reading, listening):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE users 
            SET language=?, level=?, words_learned=?, speaking=?, writing=?, reading=?, listening=?
            WHERE id=?
        """, (language, level, words_learned, speaking, writing, reading, listening, user_id))
        conn.commit()

def delete_user(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()

def get_user_languages():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT language FROM users WHERE language != ''")
        return [row[0] for row in cur.fetchall()]

def get_username():
    """Get the first username from the database"""
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT username FROM users LIMIT 1")
        result = cur.fetchone()
        return result[0] if result else ""

# Vocabulary functions
def add_vocabulary(word, definition, language_category=""):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO vocabulary (word, definition, language_category)
            VALUES (?, ?, ?)
        """, (word, definition, language_category))
        conn.commit()
        return cur.lastrowid

def get_all_vocabulary():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vocabulary")
        return cur.fetchall()

def update_vocabulary(vocab_id, word, definition, language_category):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE vocabulary 
            SET word=?, definition=?, language_category=?
            WHERE id=?
        """, (word, definition, language_category, vocab_id))
        conn.commit()

def delete_vocabulary(vocab_id):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM vocabulary WHERE id=?", (vocab_id,))
        conn.commit()

def get_vocabulary_count_by_language(language):
    """Get vocabulary count for a specific language"""
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM vocabulary WHERE language_category=?", (language,))
        return cur.fetchone()[0]