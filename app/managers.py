import sqlite3
from app.models import Actor


class ActorManager:
    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name
        self.connection = sqlite3.connect(db_name)
        self._create_table()

    def _create_table(self):
        """Вспомогательный метод для создания таблицы"""
        cursor = self.connection.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def create(self, first_name: str, last_name: str) -> Actor:
        """Создает новую запись в таблице"""
        cursor = self.connection.cursor()
        cursor.execute(
            f"INSERT INTO {self.table_name} (first_name, last_name) VALUES (?, ?)",
            (first_name, last_name)
        )
        self.connection.commit()
        return Actor(id=cursor.lastrowid, first_name=first_name, last_name=last_name)

    def all(self) -> list:
        """Возвращает список всех актеров из БД"""
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT id, first_name, last_name FROM {self.table_name}")
        rows = cursor.fetchall()
        return [Actor(id=row[0], first_name=row[1], last_name=row[2]) for row in rows]

    def update(self, pk: int, new_first_name: str, new_last_name: str) -> None:
        """Обновляет данные актера по id"""
        cursor = self.connection.cursor()
        cursor.execute(
            f"UPDATE {self.table_name} SET first_name = ?, last_name = ? WHERE id = ?",
            (new_first_name, new_last_name, pk)
        )
        self.connection.commit()

    def delete(self, pk: int) -> None:
        """Удаляет актера по id"""
        cursor = self.connection.cursor()
        cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (pk,))
        self.connection.commit()