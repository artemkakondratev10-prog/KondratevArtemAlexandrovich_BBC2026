import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TaskWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.tasks = []

        self.setWindowTitle("Учебный список задач — PyQt6")
        self.resize(720, 650)
        # Окно можно растягивать. Задаём только нижнюю границу размера.
        self.setMinimumSize(640, 580)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("Мой список задач"))

        # Форма ввода.
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

        # Список получает свободное место при растяжении окна.
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

        self.summary_label = QLabel("Всего: 0 | Выполнено: 0 | Общее время: 0 мин")
        self.result_label = QLabel("Добавьте первую задачу.")
        self.result_label.setTextFormat(Qt.TextFormat.PlainText)
        self.result_label.setWordWrap(True)
        main_layout.addWidget(self.summary_label)
        main_layout.addWidget(self.result_label)

        # Управление главным окном.
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

        # Связываем сигналы виджетов с методами.
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

        self.update_buttons()
        self.title_entry.setFocus()

    def selected_row(self):
        items = self.task_list.selectedItems()
        if not items:
            return -1
        return self.task_list.row(items[0])

    def update_buttons(self):
        row = self.selected_row()
        self.delete_button.setEnabled(row >= 0)
        self.complete_button.setEnabled(row >= 0 and not self.tasks[row]["done"])

    def refresh_list(self, selected_row=-1):
        self.task_list.clear()
        done_count = 0
        total_minutes = 0

        for task in self.tasks:
            mark = "[ ]"
            if task["done"]:
                mark = "[x]"
                done_count += 1
            line = f"{mark} {task['title']} | {task['minutes']} мин | {task['priority']}"
            if task["important"]:
                line += " | Важная"
            self.task_list.addItem(line)
            total_minutes += task["minutes"]

        self.summary_label.setText(
            f"Всего: {len(self.tasks)} | Выполнено: {done_count} | "
            f"Общее время: {total_minutes} мин"
        )
        if selected_row >= 0:
            self.task_list.setCurrentRow(selected_row)
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

        task = {
            "title": title,
            "minutes": minutes,
            "priority": self.priority_box.currentText(),
            "important": self.important_check.isChecked(),
            "done": False,
        }
        self.tasks.append(task)
        self.refresh_list(len(self.tasks) - 1)
        self.result_label.setText(f"Добавлена задача: {title}")
        self.title_entry.clear()
        self.title_entry.setFocus()

    def complete_task(self):
        row = self.selected_row()
        if row < 0:
            return

        self.tasks[row]["done"] = True
        self.refresh_list(row)
        self.result_label.setText(f"Выполнена задача: {self.tasks[row]['title']}")

    def delete_task(self):
        row = self.selected_row()
        if row < 0:
            return

        yes = QMessageBox.StandardButton.Yes
        no = QMessageBox.StandardButton.No
        answer = QMessageBox.question(self, "Удаление", "Удалить выбранную задачу?", yes | no, no)
        if answer == yes:
            task = self.tasks.pop(row)
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
        answer = QMessageBox.question(
            self, "Выход", "Закрыть программу? Задачи не сохранятся.", yes | no, no
        )
        if answer == yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskWindow()
    window.show()
    sys.exit(app.exec())
