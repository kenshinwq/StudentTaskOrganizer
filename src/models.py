from datetime import datetime, date

class Task:
    def __init__(self, subject: str, title: str, priority: str, date: date, time: str):
        self.subject = subject
        self.title = title
        self.priority = priority
        self.date = date
        self.time = time

    def to_dict(self) -> dict:
        return {
            "subject": self.subject,
            "title": self.title,
            "priority": self.priority,
            "date": self.date.strftime("%Y-%m-%d"),
            "time": self.time,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        dt = datetime.strptime(data.get("date", "1970-01-01"), "%Y-%m-%d").date()
        return Task(
            subject=data.get("subject", ""),
            title=data.get("title", ""),
            priority=data.get("priority", "Средний"),
            date=dt,
            time=data.get("time", "00:00"),
        )
