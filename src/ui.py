import calendar
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkcalendar import Calendar as _Calendar
from models import Task

class Calendar(_Calendar):
    def __init__(self, *args, **kwargs):
        kwargs.pop('style', None)
        super().__init__(*args, **kwargs)

    def configure(self, cnf=None, **kwargs):
        kwargs.pop('style', None)
        return super().configure(cnf or {}, **kwargs)

class DetailsPopup(tb.Toplevel):
    def __init__(self, parent, task: Task, save_callback, delete_callback):
        super().__init__(parent)
        self.title("Детали задачи")
        container = tb.Frame(self, padding=10)
        container.pack(fill="both", expand=True)

        self.task = task
        self.save_callback = save_callback
        self.delete_callback = delete_callback

        tb.Label(container, text="Предмет:", font=('Helvetica', 10, 'bold')).grid(
            row=0, column=0, sticky="w", padx=5, pady=5)
        self.subject_entry = tb.Entry(container, bootstyle="light")
        self.subject_entry.insert(0, task.subject)
        self.subject_entry.grid(row=0, column=1, padx=5, pady=5)

        tb.Label(container, text="Задача:", font=('Helvetica', 10, 'bold')).grid(
            row=1, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = tb.Entry(container, bootstyle="light")
        self.title_entry.insert(0, task.title)
        self.title_entry.grid(row=1, column=1, padx=5, pady=5)

        tb.Label(container, text="Приоритет:", font=('Helvetica', 10, 'bold')).grid(
            row=2, column=0, sticky="w", padx=5, pady=5)
        self.priority_combo = tb.Combobox(
            container, values=["Высокий", "Средний", "Низкий"], state="readonly", bootstyle="info")
        self.priority_combo.set(task.priority)
        self.priority_combo.grid(row=2, column=1, padx=5, pady=5)

        tb.Label(container, text="Дата:", font=('Helvetica', 10, 'bold')).grid(
            row=3, column=0, sticky="w", padx=5, pady=5)
        tb.Label(container, text=task.date.strftime("%Y-%m-%d"), bootstyle="light").grid(
            row=3, column=1, sticky="w", padx=5, pady=5)

        tb.Label(container, text="Время:", font=('Helvetica', 10, 'bold')).grid(
            row=4, column=0, sticky="w", padx=5, pady=5)
        time_frame = tb.Frame(container)
        time_frame.grid(row=4, column=1, padx=5, pady=5)
        hour_val, minute_val = task.time.split(":") if ":" in task.time else ("00", "00")
        self.hour_spin = tb.Spinbox(
            time_frame, from_=0, to=23, width=3, format="%02.0f", bootstyle="light")
        self.hour_spin.set(hour_val)
        self.hour_spin.pack(side="left")
        tb.Label(time_frame, text=":", font=('Helvetica', 10, 'bold')).pack(side="left")
        self.minute_spin = tb.Spinbox(
            time_frame, from_=0, to=59, width=3, format="%02.0f", bootstyle="light")
        self.minute_spin.set(minute_val)
        self.minute_spin.pack(side="left")

        btn_frame = tb.Frame(container)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        tb.Button(btn_frame, text="Сохранить", bootstyle="success", command=self.on_save).pack(side="left", padx=5)
        tb.Button(btn_frame, text="Удалить", bootstyle="danger", command=self.on_delete).pack(side="left", padx=5)

    def on_save(self):
        new_subject = self.subject_entry.get().strip()
        new_title = self.title_entry.get().strip()
        new_priority = self.priority_combo.get()
        new_time = f"{self.hour_spin.get()}:{self.minute_spin.get()}"
        if not new_subject or not new_title:
            messagebox.showerror("Ошибка", "Предмет и задача не могут быть пустыми.")
            return
        self.task.subject = new_subject
        self.task.title = new_title
        self.task.priority = new_priority
        self.task.time = new_time
        self.save_callback(self.task)
        self.destroy()

    def on_delete(self):
        if messagebox.askyesno("Подтвердить", "Удалить эту задачу?"):
            self.delete_callback(self.task)
            self.destroy()

class MainView(tb.Window):
    def __init__(self, tasks):
        super().__init__(themename="flatly")
        self.title("Student Task Organizer")
        self.geometry("900x550")
        self.tasks = tasks
        self.create_widgets()
        self.refresh_calendar_events()

    def create_widgets(self):
        header = tb.Frame(self, bootstyle="light", padding=(10, 5))
        header.pack(fill="x")

        tb.Button(header, text="‹", bootstyle="outline-secondary", width=3,
                  command=lambda: self.navigate(-1)).pack(side="left")
        self.month_label = tb.Label(header, text="", font=('Helvetica', 16, 'bold'))
        self.month_label.pack(side="left", padx=10)
        tb.Button(header, text="›", bootstyle="outline-secondary", width=3,
                  command=lambda: self.navigate(1)).pack(side="left")

        btns = tb.Frame(header)
        btns.pack(side="right")
        tb.Button(btns, text="+ Add", bootstyle="primary").pack(side="left", padx=5)
        tb.Button(btns, text="Reminders", bootstyle="info").pack(side="left", padx=5)
        tb.Button(btns, text="Event", bootstyle="secondary").pack(side="left", padx=5)
        tb.Button(btns, text="+", bootstyle="outline-secondary", width=3).pack(side="left")

        body = tb.Frame(self)
        body.pack(fill="both", expand=True, padx=10, pady=10)

        left = tb.Frame(body)
        left.pack(side="left", fill="both", expand=True, padx=(0,10))
        self.calendar = Calendar(
            left,
            selectmode='day',
            background='white',
            foreground='#212529',
            selectbackground='#4e73df',
            headersbackground='#f8f9fa',
            normalbackground='white',
            weekendbackground='white',
            othermonthbackground='#e9ecef',
            bordercolor='#dee2e6',
            font=('Helvetica', 10),
            disabledforeground='#adb5bd'
        )
        self.calendar.pack(fill="both", expand=True)
        self.calendar.bind("<<CalendarSelected>>", self.on_date_select)
        self.update_month_label()

        right = tb.LabelFrame(body, text="New Event", bootstyle="info", padding=10)
        right.pack(side="right", fill="y")

        tb.Label(right, text="Предмет:").pack(anchor="w")
        self.subject_entry = tb.Entry(right)
        self.subject_entry.pack(fill="x", pady=5)

        tb.Label(right, text="Задача:").pack(anchor="w")
        self.title_entry = tb.Entry(right)
        self.title_entry.pack(fill="x", pady=5)

        tb.Label(right, text="Приоритет:").pack(anchor="w")
        self.priority_combo = tb.Combobox(right,
                                          values=["Высокий", "Средний", "Низкий"],
                                          state="readonly")
        self.priority_combo.set("Средний")
        self.priority_combo.pack(fill="x", pady=5)

        tb.Label(right, text="Дата:").pack(anchor="w")
        self.small_cal = Calendar(right, selectmode='day',
                                  background='white', foreground='#212529',
                                  headersbackground='#f8f9fa', normalbackground='white',
                                  othermonthbackground='#e9ecef', bordercolor='#dee2e6',
                                  font=('Helvetica', 10))
        self.small_cal.pack(fill="x", pady=5)

        tb.Label(right, text="Время:").pack(anchor="w")
        tf = tb.Frame(right)
        tf.pack(pady=5)
        self.hour_spin = tb.Spinbox(tf, from_=0, to=23, width=3, format="%02.0f")
        self.hour_spin.set("12")
        self.hour_spin.pack(side="left")
        tb.Label(tf, text=":").pack(side="left")
        self.minute_spin = tb.Spinbox(tf, from_=0, to=59, width=3, format="%02.0f")
        self.minute_spin.set("00")
        self.minute_spin.pack(side="left")

        tb.Button(right, text="Добавить", bootstyle="success", command=self.add_task).pack(fill="x", pady=10)

    def update_month_label(self):
        disp = self.calendar._date
        month_name = calendar.month_name[disp.month]
        self.month_label.configure(text=f"{month_name} {disp.year}")

    def navigate(self, delta):
        if delta < 0:
            self.calendar._prev_month()
        else:
            self.calendar._next_month()
        self.update_month_label()
        self.refresh_calendar_events()

    def refresh_calendar_events(self):
        self.calendar.calevent_remove('all')
        for task in self.tasks:
            desc = f"[{task.priority}] {task.title}"
            self.calendar.calevent_create(task.date, desc, 'task')
        self.calendar.tag_config('task', background='#4e73df', foreground='white')

    def add_task(self):
        subj = self.subject_entry.get().strip()
        title = self.title_entry.get().strip()
        prio = self.priority_combo.get()
        date = self.small_cal.selection_get()
        time = f"{self.hour_spin.get()}:{self.minute_spin.get()}"
        if not subj or not title:
            messagebox.showerror("Ошибка", "Предмет и задача не могут быть пустыми.")
            return
        new = Task(subj, title, prio, date, time)
        self.tasks.append(new)
        self.refresh_calendar_events()
        self.subject_entry.delete(0, 'end')
        self.title_entry.delete(0, 'end')
        self.priority_combo.set("Средний")
        self.hour_spin.set("12")
        self.minute_spin.set("00")

    def on_date_select(self, event):
        sel = self.calendar.selection_get()
        lst = [t for t in self.tasks if t.date == sel]
        if not lst:
            return
        DetailsPopup(self, lst[0], save_callback=self.on_task_updated, delete_callback=self.on_task_deleted)

    def on_task_updated(self, task):
        self.refresh_calendar_events()

    def on_task_deleted(self, task):
        self.tasks.remove(task)
        self.refresh_calendar_events()