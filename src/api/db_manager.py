import sqlite3
import os
from datetime import datetime

class DBManager:
    def __init__(self, db_path="data/desm.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 상담 목록 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                chat_id TEXT PRIMARY KEY,
                user_id TEXT,
                last_message TEXT,
                category TEXT DEFAULT '대기',
                updated_at DATETIME
            )
        ''')
        
        # 메시지 내역 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT,
                sender TEXT,
                content TEXT,
                msg_type TEXT DEFAULT 'text',
                media_url TEXT,
                file_name TEXT,
                timestamp DATETIME,
                FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
            )
        ''')
        
        # 컬럼 추가 (기존 테이블이 있을 경우를 대비)
        try:
            cursor.execute("ALTER TABLE messages ADD COLUMN msg_type TEXT DEFAULT 'text'")
            cursor.execute("ALTER TABLE messages ADD COLUMN media_url TEXT")
            cursor.execute("ALTER TABLE messages ADD COLUMN file_name TEXT")
        except sqlite3.OperationalError:
            # 이미 컬럼이 존재하는 경우 무시
            pass
        
        conn.commit()
        conn.close()

    def upsert_chat(self, chat_id, user_id, last_message, category='대기'):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO chats (chat_id, user_id, last_message, category, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(chat_id) DO UPDATE SET
                last_message=excluded.last_message,
                category=excluded.category,
                updated_at=excluded.updated_at
        ''', (chat_id, user_id, last_message, category, now))
        conn.commit()
        conn.close()

    def add_message(self, chat_id, sender, content, msg_type='text', media_url=None, file_name=None, timestamp=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        if not timestamp:
            timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO messages (chat_id, sender, content, msg_type, media_url, file_name, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (chat_id, sender, content, msg_type, media_url, file_name, timestamp))
        conn.commit()
        conn.close()

    def get_chats(self, category='전체'):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if category == '전체':
            cursor.execute('SELECT * FROM chats ORDER BY updated_at DESC')
        else:
            cursor.execute('SELECT * FROM chats WHERE category=? ORDER BY updated_at DESC', (category,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_messages(self, chat_id):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages WHERE chat_id=? ORDER BY timestamp ASC', (chat_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
