import sqlite3


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users_events (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                event1 INTEGER DEFAULT 0,
                                event2 INTEGER DEFAULT 0,
                                event3 INTEGER DEFAULT 0,
                                event4 INTEGER DEFAULT 0,
                                event5 INTEGER DEFAULT 0,
                                event6 INTEGER DEFAULT 0,
                                event7 INTEGER DEFAULT 0,
                                event8 INTEGER DEFAULT 0)""")
            self.connection.commit()
        except sqlite3.Error as error:
            print("DB ERROR", error)

    def get_user_by_chat_id(self, user_id):
        """Получает и возвращает айди пользователя."""
        try:
            self.cursor.execute('SELECT * FROM users_events WHERE user_id = ?', (user_id,))
            user = self.cursor.fetchone()
            return user
        except sqlite3.Error as error:
            print("DB ERROR", error)
        return None

    def add_user(self, user_id):
        """Добавляет пользователя в базу данных."""
        try:
            if not self.get_user_by_chat_id(user_id):
                self.cursor.execute('INSERT INTO users_events (user_id) VALUES (?)', (user_id, ))
                self.connection.commit()
        except sqlite3.Error as error:
            print("DB ERROR", error)

    def update_subscribe(self, user_id, event):
        """Обновляет подпски пользователя."""
        try:
            self.cursor.execute(f'SELECT event{event} FROM users_events WHERE user_id = ?', (user_id, ))
            ev = self.cursor.fetchone()
            if ev[0]:
                self.cursor.execute(f'UPDATE users_events SET event{event} = ? WHERE user_id = ?',
                                    (0, user_id))
                self.connection.commit()
                return False
            else:
                self.cursor.execute(f'UPDATE users_events SET event{event} = ? WHERE user_id = ?',
                                    (1, user_id))
                self.connection.commit()
                return True
        except sqlite3.Error as error:
            print("DB ERROR", error)
        return None

    def update_subscribe_all(self, user_id, state):
        """Обновляет все подписки пользователя."""
        try:
            self.cursor.execute('UPDATE users_events SET event1 = ?, event2 = ?, event3 = ?, event4 = ?,'
                                ' event5 = ?, event6 = ?, event7 = ?, event8 = ? WHERE user_id = ?',
                                (state, state, state, state, state, state, state, state, user_id))
            self.connection.commit()
        except sqlite3.Error as error:
            print("DB ERROR", error)

    def get_events(self, user_id):
        """Получает и возвращает подписки пользователя."""
        try:
            self.cursor.execute('SELECT * FROM users_events WHERE user_id = ?', (user_id, ))
            events = self.cursor.fetchone()
            return events[2:]
        except sqlite3.Error as error:
            print("DB ERROR", error)
        return None

    def get_subscribed_users(self, event):
        """Получает и возвращает список кортежей подписанных пользователей"""
        try:
            self.cursor.execute(f'SELECT user_id FROM users_events WHERE event{event} = ?', (True,))
            info_users = self.cursor.fetchall()
            return info_users
        except sqlite3.Error as error:
            print("DB ERROR", error)
        return None

