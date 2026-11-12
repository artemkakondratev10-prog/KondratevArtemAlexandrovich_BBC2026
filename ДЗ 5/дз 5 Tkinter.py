import tkinter as tk
from tkinter import ttk, messagebox


# Здесь хранятся данные. Пока программа работает, задачи остаются в списке.
tasks = []
help_window = None


def update_buttons(event=None):
    """Включаем кнопки только тогда, когда выбрана подходящая задача."""
    selection = task_list.curselection()

    if not selection:
        complete_button.config(state="disabled")
        delete_button.config(state="disabled")
        return

    index = selection[0]
    delete_button.config(state="normal")

    if tasks[index]["done"]:
        complete_button.config(state="disabled")
    else:
        complete_button.config(state="normal")


def refresh_list(selected_index=None):
    """Выводим текущие данные в список и пересчитываем результат."""
    task_list.delete(0, tk.END)
    done_count = 0
    total_minutes = 0

    for task in tasks:
        mark = "[ ]"
        if task["done"]:
            mark = "[x]"
            done_count += 1

        line = (
            f"{mark} {task['title']} | {task['minutes']} мин | "
            f"{task['priority']}"
        )
        if task["important"]:
            line += " | Важная"

        task_list.insert(tk.END, line)
        total_minutes += task["minutes"]

    summary_var.set(
        f"Всего: {len(tasks)} | Выполнено: {done_count} | "
        f"Общее время: {total_minutes} мин"
    )

    if selected_index is not None:
        task_list.selection_set(selected_index)
        task_list.see(selected_index)

    update_buttons()


def add_task(event=None):
    """Проверяем ввод и только после этого добавляем задачу."""
    title = title_entry.get().strip()
    minutes_text = minutes_entry.get().strip()

    if not title:
        messagebox.showerror("Ошибка", "Введите название задачи.", parent=root)
        title_entry.focus_set()
        return

    if len(title) > 60:
        messagebox.showerror("Ошибка", "Название: не больше 60 символов.", parent=root)
        return

    try:
        minutes = int(minutes_text)
    except ValueError:
        messagebox.showerror("Ошибка", "Время должно быть целым числом.", parent=root)
        minutes_entry.focus_set()
        return

    if minutes < 1 or minutes > 1440:
        messagebox.showerror("Ошибка", "Укажите время от 1 до 1440 минут.", parent=root)
        return

    task = {
        "title": title,
        "minutes": minutes,
        "priority": priority_var.get(),
        "important": important_var.get(),
        "done": False,
    }
    tasks.append(task)
    refresh_list(len(tasks) - 1)
    result_var.set(f"Добавлена задача: {title}")

    title_entry.delete(0, tk.END)
    title_entry.focus_set()


def complete_task():
    selection = task_list.curselection()
    if not selection:
        return

    index = selection[0]
    tasks[index]["done"] = True
    refresh_list(index)
    result_var.set(f"Выполнена задача: {tasks[index]['title']}")


def delete_task():
    selection = task_list.curselection()
    if not selection:
        return

    index = selection[0]
    title = tasks[index]["title"]
    answer = messagebox.askyesno(
        "Удаление", f"Удалить задачу «{title}»?", parent=root
    )

    if answer:
        tasks.pop(index)
        refresh_list()
        result_var.set(f"Удалена задача: {title}")


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


def open_help():
    global help_window

    if help_window is None or not help_window.winfo_exists():
        help_window = tk.Toplevel(root)
        help_window.title("Дополнительное окно")
        help_window.geometry("420x180")
        help_window.resizable(False, False)
        ttk.Label(
            help_window,
            text="Это отдельное окно Toplevel.\n"
                 "Его можно скрыть или закрыть.\n"
                 "Кнопка в главном окне откроет его снова.",
        ).grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky="w")
        ttk.Button(
            help_window, text="Скрыть", command=help_window.withdraw
        ).grid(row=1, column=0, padx=15, pady=10)
        ttk.Button(
            help_window, text="Закрыть", command=help_window.destroy
        ).grid(row=1, column=1, padx=15, pady=10)
    else:
        help_window.deiconify()
        help_window.lift()


def close_app():
    if messagebox.askyesno(
        "Выход", "Закрыть программу? Задачи не сохранятся.", parent=root
    ):
        root.destroy()


# Создаём главное окно и задаём его свойства.
root = tk.Tk()
root.title("Учебный список задач")
root.geometry("720x650")
root.minsize(640, 580)
root.resizable(True, True)
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

# Переменные Tkinter связаны с элементами на экране.
priority_var = tk.StringVar(value="Обычный")
important_var = tk.BooleanVar(value=False)
summary_var = tk.StringVar(value="Всего: 0 | Выполнено: 0 | Общее время: 0 мин")
result_var = tk.StringVar(value="Добавьте первую задачу.")

ttk.Label(root, text="Мой список задач").grid(
    row=0, column=0, padx=10, pady=10, sticky="w"
)

# Форма ввода.
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

# Список с вертикальной и горизонтальной прокруткой.
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

# Кнопки для демонстрации управления окнами.
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
ttk.Button(windows_frame, text="Открыть доп. окно", command=open_help).grid(
    row=1, column=0, padx=5, pady=5
)
ttk.Button(windows_frame, text="Закрыть программу", command=close_app).grid(
    row=1, column=1, padx=5, pady=5
)

# События: выбор строки, клавиатура и закрытие крестиком.
task_list.bind("<<ListboxSelect>>", update_buttons)
title_entry.bind("<Return>", add_task)
minutes_entry.bind("<Return>", add_task)
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", leave_fullscreen)
root.protocol("WM_DELETE_WINDOW", close_app)
title_entry.focus_set()

if __name__ == "__main__":
    root.mainloop()
