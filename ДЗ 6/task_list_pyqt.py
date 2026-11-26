import sqlite3
import sys

from database import DB_PATH, open_database, read_tasks

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget, QMessageBox,
    QPushButton, QVBoxLayout, QWidget,
)


class TaskWindow(QWidget):
    def __init__(self, db_path=DB_PATH):
        super().__init__()
        self.connection = open_database(db_path)

        try:
            self.tasks = self.read_tasks()
        except sqlite3.Error:
            self.connection.close()
            raise

        self.setWindowTitle("Учебный список задач — PyQt6 и SQLite")
        self.resize(720, 650)
        self.setMinimumSize(640, 580)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("Мой список задач"))

        form = QGroupBox("Новая задача")
        form_layout = QGridLayout(form)
        form_layout.setColumnStretch(1, 1)
        self.title_entry = QLineEdit()
        self.minutes_entry = QLineEdit("30")
        self.minutes_entry.setMaximumWidth(100)
        self.priority_box = QComboBox()
        self.priority_box.addItems(["Низкий", "Обычный", "Высокий"])
        self.priority_box.setCurrentText("Обычный")
        self.important_check = QCheckBox("Важная задача")
        self.add_button = QPushButton("Добавить задачу")

        form_layout.addWidget(QLabel("Название:"), 0, 0)
        form_layout.addWidget(self.title_entry, 0, 1)
        form_layout.addWidget(QLabel("Время в минутах:"), 1, 0)
        form_layout.addWidget(self.minutes_entry, 1, 1)
        form_layout.addWidget(QLabel("Приоритет:"), 2, 0)
        form_layout.addWidget(self.priority_box, 2, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(self.important_check, 3, 1)
        form_layout.addWidget(self.add_button, 4, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(form)

        tasks_group = QGroupBox("Задачи")
        tasks_layout = QVBoxLayout(tasks_group)
        self.task_list = QListWidget()
        tasks_layout.addWidget(self.task_list)
        main_layout.addWidget(tasks_group, 1)

        actions_layout = QHBoxLayout()
        self.complete_button = QPushButton("Выполнить выбранную")
        self.delete_button = QPushButton("Удалить выбранную")
        actions_layout.addWidget(self.complete_button)
        actions_layout.addWidget(self.delete_button)
        actions_layout.addStretch()
        main_layout.addLayout(actions_layout)

        self.summary_label = QLabel()
        self.result_label = QLabel("Задачи загружены. Изменения сохраняются автоматически.")
        self.result_label.setTextFormat(Qt.TextFormat.PlainText)
        self.result_label.setWordWrap(True)
        main_layout.addWidget(self.summary_label)
        main_layout.addWidget(self.result_label)

        window_group = QGroupBox("Управление окном")
        window_layout = QHBoxLayout(window_group)
        self.fullscreen_button = QPushButton("На весь экран (F11)")
        minimize_button = QPushButton("Свернуть")
        hide_button = QPushButton("Скрыть на 2 секунды")
        close_button = QPushButton("Закрыть программу")
        window_layout.addWidget(self.fullscreen_button)
        window_layout.addWidget(minimize_button)
        window_layout.addWidget(hide_button)
        window_layout.addWidget(close_button)
        main_layout.addWidget(window_group)

        self.add_button.clicked.connect(self.add_task)
        self.title_entry.returnPressed.connect(self.add_task)
        self.minutes_entry.returnPressed.connect(self.add_task)
        self.task_list.itemSelectionChanged.connect(self.update_buttons)
        self.complete_button.clicked.connect(self.complete_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        minimize_button.clicked.connect(self.showMinimized)
        hide_button.clicked.connect(self.hide_window)
        close_button.clicked.connect(self.close)

        self.fullscreen_shortcut = QShortcut(QKeySequence("F11"), self)
        self.fullscreen_shortcut.activated.connect(self.toggle_fullscreen)
        self.escape_shortcut = QShortcut(QKeySequence("Escape"), self)
        self.escape_shortcut.activated.connect(self.leave_fullscreen)

        self.refresh_list()
        self.title_entry.setFocus()
        self.sync_timer = QTimer(self)
        self.sync_timer.timeout.connect(self.sync_tasks)
        self.sync_timer.start(1000)

    def read_tasks(self):
        return read_tasks(self.connection)

    def sync_tasks(self):
        try:
            tasks = self.read_tasks()
        except sqlite3.Error:
            return
        if tasks == self.tasks:
            return

        selected_id = None
        row = self.selected_row()
        if row >= 0:
            selected_id = self.tasks[row]["id"]
        self.tasks = tasks
        self.refresh_list(selected_id)

    def selected_row(self):
        items = self.task_list.selectedItems()
        if not items:
            return -1
        return self.task_list.row(items[0])

    def update_buttons(self):
        row = self.selected_row()
        self.delete_button.setEnabled(row >= 0)
        self.complete_button.setEnabled(row >= 0 and not self.tasks[row]["done"])

    def refresh_list(self, selected_id=None):
        self.task_list.blockSignals(True)
        self.task_list.clear()
        done_count = 0
        total_minutes = 0
        selected_row = -1

        for row, task in enumerate(self.tasks):
            mark = "[ ]"
            if task["done"]:
                mark = "[x]"
                done_count += 1
            line = f"{mark} {task['title']} | {task['minutes']} мин | {task['priority']}"
            if task["important"]:
                line += " | Важная"
            self.task_list.addItem(line)
            total_minutes += task["minutes"]
            if task["id"] == selected_id:
                selected_row = row

        self.summary_label.setText(
            f"Всего: {len(self.tasks)} | Выполнено: {done_count} | "
            f"Общее время: {total_minutes} мин"
        )
        if selected_row >= 0:
            self.task_list.setCurrentRow(selected_row)
        self.task_list.blockSignals(False)
        self.update_buttons()

    def add_task(self):
        title = self.title_entry.text().strip()
        minutes_text = self.minutes_entry.text().strip()

        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название задачи.")
            self.title_entry.setFocus()
            return
        if len(title) > 60:
            QMessageBox.warning(self, "Ошибка", "Название: не больше 60 символов.")
            self.title_entry.setFocus()
            return
        try:
            minutes = int(minutes_text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Время должно быть целым числом.")
            self.minutes_entry.setFocus()
            return
        if minutes < 1 or minutes > 1440:
            QMessageBox.warning(self, "Ошибка", "Укажите время от 1 до 1440 минут.")
            self.minutes_entry.setFocus()
            return

        try:
            with self.connection:
                cursor = self.connection.execute("""
                    INSERT INTO tasks (title, minutes, priority_id, important, done)
                    VALUES (?, ?, (SELECT id FROM priorities WHERE name = ?), ?, 0)
                """, (title, minutes, self.priority_box.currentText(),
                      int(self.important_check.isChecked())))
                tasks = self.read_tasks()
        except sqlite3.Error as error:
            QMessageBox.critical(self, "Ошибка сохранения", f"Задача не добавлена.\n{error}")
            return

        self.tasks = tasks
        self.refresh_list(cursor.lastrowid)
        self.result_label.setText(f"Сохранена задача: {title}")
        self.title_entry.clear()
        self.title_entry.setFocus()

    def complete_task(self):
        row = self.selected_row()
        if row < 0:
            return
        task = self.tasks[row]

        try:
            with self.connection:
                self.connection.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task["id"],))
                tasks = self.read_tasks()
        except sqlite3.Error as error:
            QMessageBox.critical(self, "Ошибка сохранения", f"Статус не изменён.\n{error}")
            return

        self.tasks = tasks
        self.refresh_list(task["id"])
        self.result_label.setText(f"Выполнена и сохранена задача: {task['title']}")

    def delete_task(self):
        row = self.selected_row()
        if row < 0:
            return
        task = self.tasks[row]
        yes = QMessageBox.StandardButton.Yes
        no = QMessageBox.StandardButton.No
        answer = QMessageBox.question(self, "Удаление", "Удалить выбранную задачу?", yes | no, no)
        if answer != yes:
            return

        try:
            with self.connection:
                self.connection.execute("DELETE FROM tasks WHERE id = ?", (task["id"],))
                tasks = self.read_tasks()
        except sqlite3.Error as error:
            QMessageBox.critical(self, "Ошибка сохранения", f"Задача не удалена.\n{error}")
            return

        self.tasks = tasks
        self.refresh_list()
        self.result_label.setText(f"Удалена задача: {task['title']}")

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.leave_fullscreen()
        else:
            self.showFullScreen()
            self.fullscreen_button.setText("Обычный режим (F11)")

    def leave_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.fullscreen_button.setText("На весь экран (F11)")

    def hide_window(self):
        self.hide()
        QTimer.singleShot(2000, self.show)

    def closeEvent(self, event):
        yes = QMessageBox.StandardButton.Yes
        no = QMessageBox.StandardButton.No
        answer = QMessageBox.question(self, "Выход", "Закрыть программу?", yes | no, no)
        if answer == yes:
            self.sync_timer.stop()
            self.connection.close()
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        window = TaskWindow()
    except (sqlite3.Error, OSError) as error:
        QMessageBox.critical(None, "Ошибка базы данных", f"Не удалось открыть базу.\n{DB_PATH}\n{error}")
        sys.exit(1)
    window.show()
    sys.exit(app.exec())
