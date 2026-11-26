import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().with_name("tasks.db")


def open_database(db_path=DB_PATH):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        with connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("""
                CREATE TABLE IF NOT EXISTS priorities (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE
                        CHECK (name IN ('Низкий', 'Обычный', 'Высокий'))
                )
            """)
            connection.executemany(
                "INSERT OR IGNORE INTO priorities (name) VALUES (?)",
                [("Низкий",), ("Обычный",), ("Высокий",)]
            )

            columns = connection.execute("PRAGMA table_info(tasks)").fetchall()
            table_name = "tasks"
            if "priority" in [column["name"] for column in columns]:
                table_name = "tasks_new"

            if not columns or table_name == "tasks_new":
                connection.execute(f"""
                    CREATE TABLE {table_name} (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL
                            CHECK (length(trim(title)) BETWEEN 1 AND 60),
                        minutes INTEGER NOT NULL CHECK (minutes BETWEEN 1 AND 1440),
                        priority_id INTEGER NOT NULL,
                        important INTEGER NOT NULL DEFAULT 0 CHECK (important IN (0, 1)),
                        done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1)),
                        FOREIGN KEY (priority_id) REFERENCES priorities(id)
                    )
                """)

            if table_name == "tasks_new":
                connection.execute("""
                    INSERT INTO tasks_new (id, title, minutes, priority_id, important, done)
                    SELECT id, title, minutes,
                           (SELECT id FROM priorities WHERE name = tasks.priority),
                           important, done
                    FROM tasks
                """)
                connection.execute("DROP TABLE tasks")
                connection.execute("ALTER TABLE tasks_new RENAME TO tasks")

            if connection.execute("PRAGMA foreign_key_check").fetchone():
                raise sqlite3.IntegrityError("Нарушена связь задачи с приоритетом.")
    except sqlite3.Error:
        connection.close()
        raise

    return connection


def read_tasks(connection):
    return connection.execute("""
        SELECT tasks.id, tasks.title, tasks.minutes,
               priorities.name AS priority, tasks.important, tasks.done
        FROM tasks
        JOIN priorities ON tasks.priority_id = priorities.id
        ORDER BY tasks.id
    """).fetchall()
