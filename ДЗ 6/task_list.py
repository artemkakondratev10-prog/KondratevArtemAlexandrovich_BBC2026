import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from database import DB_PATH, open_database, read_tasks


root = None
connection = None
tasks = []
sync_after_id = None


def selected_row():
    selection = task_list.curselection()
    if not selection:
        return -1
    return selection[0]


def update_buttons(event=None):
    row = selected_row()
    if row < 0:
        complete_button.config(state="disabled")
        delete_button.config(state="disabled")
        return

    delete_button.config(state="normal")
    if tasks[row]["done"]:
        complete_button.config(state="disabled")
    else:
        complete_button.config(state="normal")


def refresh_list(selected_id=None):
    task_list.delete(0, tk.END)
    done_count = 0
    total_minutes = 0
    selected_index = -1

    for index, task in enumerate(tasks):
        mark = "[ ]"
        if task["done"]:
            mark = "[x]"
            done_count += 1

        line = f"{mark} {task['title']} | {task['minutes']} мин | {task['priority']}"
        if task["important"]:
            line += " | Важная"
        task_list.insert(tk.END, line)
        total_minutes += task["minutes"]
        if task["id"] == selected_id:
            selected_index = index

    summary_var.set(
        f"Всего: {len(tasks)} | Выполнено: {done_count} | "
        f"Общее время: {total_minutes} мин"
    )
    if selected_index >= 0:
        task_list.selection_set(selected_index)
        task_list.see(selected_index)
    update_buttons()


def add_task(event=None):
    global tasks
    title = title_entry.get().strip()
    minutes_text = minutes_entry.get().strip()

    if not title:
        messagebox.showerror("Ошибка", "Введите название задачи.", parent=root)
        title_entry.focus_set()
        return
    if len(title) > 60:
        messagebox.showerror("Ошибка", "Название: не больше 60 символов.", parent=root)
        title_entry.focus_set()
        return
    try:
        minutes = int(minutes_text)
    except ValueError:
        messagebox.showerror("Ошибка", "Время должно быть целым числом.", parent=root)
        minutes_entry.focus_set()
        return
    if minutes < 1 or minutes > 1440:
        messagebox.showerror("Ошибка", "Укажите время от 1 до 1440 минут.", parent=root)
        minutes_entry.focus_set()
        return

    try:
        with connection:
            cursor = connection.execute("""
                INSERT INTO tasks (title, minutes, priority_id, important, done)
                VALUES (?, ?, (SELECT id FROM priorities WHERE name = ?), ?, 0)
            """, (title, minutes, priority_var.get(), int(important_var.get())))
            saved_tasks = read_tasks(connection)
    except sqlite3.Error as error:
        messagebox.showerror("Ошибка сохранения", f"Задача не добавлена.\n{error}", parent=root)
        return

    tasks = saved_tasks
    refresh_list(cursor.lastrowid)
    result_var.set(f"Сохранена задача: {title}")
    title_entry.delete(0, tk.END)
    title_entry.focus_set()


def complete_task():
    global tasks
    row = selected_row()
    if row < 0:
        return
    task = tasks[row]

    try:
        with connection:
            connection.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task["id"],))
            saved_tasks = read_tasks(connection)
    except sqlite3.Error as error:
        messagebox.showerror("Ошибка сохранения", f"Статус не изменён.\n{error}", parent=root)
        return

    tasks = saved_tasks
    refresh_list(task["id"])
    result_var.set(f"Выполнена и сохранена задача: {task['title']}")


def delete_task():
    global tasks
    row = selected_row()
    if row < 0:
        return
    task = tasks[row]
    answer = messagebox.askyesno("Удаление", "Удалить выбранную задачу?", parent=root)
    if not answer:
        return

    try:
        with connection:
            connection.execute("DELETE FROM tasks WHERE id = ?", (task["id"],))
            saved_tasks = read_tasks(connection)
    except sqlite3.Error as error:
        messagebox.showerror("Ошибка сохранения", f"Задача не удалена.\n{error}", parent=root)
        return

    tasks = saved_tasks
    refresh_list()
    result_var.set(f"Удалена задача: {task['title']}")


def sync_tasks():
    global tasks, sync_after_id
    try:
        saved_tasks = read_tasks(connection)
        if saved_tasks != tasks:
            row = selected_row()
            selected_id = None
            if row >= 0:
                selected_id = tasks[row]["id"]
            tasks = saved_tasks
            refresh_list(selected_id)
    except sqlite3.Error:
        pass
    sync_after_id = root.after(1000, sync_tasks)


def toggle_fullscreen(event=None):
    enabled = not root.attributes("-fullscreen")
    root.attributes("-fullscreen", enabled)
    if enabled:
        fullscreen_button.config(text="Обычный режим (F11)")
    else:
        fullscreen_button.config(text="На весь экран (F11)")
    return "break"


def leave_fullscreen(event=None):
    root.attributes("-fullscreen", False)
    fullscreen_button.config(text="На весь экран (F11)")


def hide_window():
    root.withdraw()
    root.after(2000, root.deiconify)


def close_app():
    if messagebox.askyesno("Выход", "Закрыть программу?", parent=root):
        if sync_after_id is not None:
            root.after_cancel(sync_after_id)
        connection.close()
        root.destroy()


def create_window(db_path=DB_PATH):
    global root, connection, tasks, sync_after_id
    global title_entry, minutes_entry, priority_var, important_var
    global task_list, summary_var, result_var, complete_button, delete_button
    global add_button, fullscreen_button, form, list_frame, actions, windows_frame

    root = tk.Tk()
    root.withdraw()
    connection = None
    try:
        connection = open_database(db_path)
        tasks = read_tasks(connection)
    except (sqlite3.Error, OSError) as error:
        if connection is not None:
            connection.close()
        messagebox.showerror("Ошибка базы данных", f"Не удалось открыть базу.\n{db_path}\n{error}", parent=root)
        root.destroy()
        return None

    root.title("Учебный список задач")
    root.geometry("720x650")
    root.minsize(640, 580)
    root.resizable(True, True)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)

    priority_var = tk.StringVar(value="Обычный")
    important_var = tk.BooleanVar(value=False)
    summary_var = tk.StringVar()
    result_var = tk.StringVar(value="Задачи загружены. Изменения сохраняются автоматически.")

    ttk.Label(root, text="Мой список задач").grid(
        row=0, column=0, padx=10, pady=10, sticky="w"
    )

    form = ttk.LabelFrame(root, text="Новая задача", padding=10)
    form.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    form.columnconfigure(1, weight=1)
    ttk.Label(form, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    title_entry = ttk.Entry(form)
    title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    ttk.Label(form, text="Время в минутах:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    minutes_entry = ttk.Entry(form, width=10)
    minutes_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    minutes_entry.insert(0, "30")
    ttk.Label(form, text="Приоритет:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    priority_box = ttk.Combobox(
        form, textvariable=priority_var,
        values=["Низкий", "Обычный", "Высокий"], state="readonly", width=15
    )
    priority_box.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    ttk.Checkbutton(form, text="Важная задача", variable=important_var).grid(
        row=3, column=1, padx=5, pady=5, sticky="w"
    )
    add_button = ttk.Button(form, text="Добавить задачу", command=add_task)
    add_button.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    list_frame = ttk.LabelFrame(root, text="Задачи", padding=5)
    list_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
    list_frame.columnconfigure(0, weight=1)
    list_frame.rowconfigure(0, weight=1)
    task_list = tk.Listbox(list_frame, height=6, exportselection=False)
    task_list.grid(row=0, column=0, sticky="nsew")
    vertical_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=task_list.yview)
    vertical_scroll.grid(row=0, column=1, sticky="ns")
    horizontal_scroll = ttk.Scrollbar(list_frame, orient="horizontal", command=task_list.xview)
    horizontal_scroll.grid(row=1, column=0, sticky="ew")
    task_list.config(yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set)

    actions = ttk.Frame(root)
    actions.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    complete_button = ttk.Button(
        actions, text="Выполнить выбранную", command=complete_task, state="disabled"
    )
    complete_button.grid(row=0, column=0, padx=5)
    delete_button = ttk.Button(
        actions, text="Удалить выбранную", command=delete_task, state="disabled"
    )
    delete_button.grid(row=0, column=1, padx=5)
    ttk.Label(root, textvariable=summary_var).grid(
        row=4, column=0, padx=10, pady=5, sticky="w"
    )
    ttk.Label(root, textvariable=result_var, wraplength=600).grid(
        row=5, column=0, padx=10, pady=5, sticky="w"
    )

    windows_frame = ttk.LabelFrame(root, text="Управление окнами", padding=5)
    windows_frame.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
    fullscreen_button = ttk.Button(
        windows_frame, text="На весь экран (F11)", command=toggle_fullscreen
    )
    fullscreen_button.grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(windows_frame, text="Свернуть", command=root.iconify).grid(
        row=0, column=1, padx=5, pady=5
    )
    ttk.Button(windows_frame, text="Скрыть на 2 секунды", command=hide_window).grid(
        row=0, column=2, padx=5, pady=5
    )
    ttk.Button(windows_frame, text="Закрыть программу", command=close_app).grid(
        row=1, column=0, padx=5, pady=5
    )

    task_list.bind("<<ListboxSelect>>", update_buttons)
    title_entry.bind("<Return>", add_task)
    minutes_entry.bind("<Return>", add_task)
    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", leave_fullscreen)
    root.protocol("WM_DELETE_WINDOW", close_app)
    refresh_list()
    sync_after_id = root.after(1000, sync_tasks)
    root.deiconify()
    title_entry.focus_set()
    return root


if __name__ == "__main__":
    root = create_window()
    if root is not None:
        root.mainloop()
