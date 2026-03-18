"""
TaskStore - タスクデータの永続化
"""
import json
import os
import uuid
import calendar
from datetime import date


class TaskStore:
    def __init__(self, path: str):
        self.path  = path
        self.tasks = []
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except Exception:
                self.tasks = []

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def add(self, title, detail, start_date, due_date, note,
            label_color="#4F7EFF", due_time="12:00") -> dict:
        task = {
            "id":          str(uuid.uuid4()),
            "title":       title,
            "detail":      detail,
            "start_date":  start_date,
            "due_date":    due_date,
            "due_time":    due_time,
            "note":        note,
            "done":        False,
            "color":       self._next_color(),
            "label_color": label_color,
        }
        self.tasks.append(task)
        self.save()
        return task

    def update(self, task_id, **kwargs):
        for t in self.tasks:
            if t["id"] == task_id:
                t.update(kwargs)
                break
        self.save()

    def delete(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.save()

    def get_all(self) -> list:
        return list(self.tasks)

    def get_in_range(self, start_date, end_date) -> list:
        result = []
        for t in self.tasks:
            try:
                s = date.fromisoformat(t["start_date"])
                e = date.fromisoformat(t["due_date"])
                if s <= end_date and e >= start_date:
                    result.append(t)
            except Exception:
                pass
        return result

    def get_for_month(self, year: int, month: int) -> list:
        first = date(year, month, 1)
        last  = date(year, month, calendar.monthrange(year, month)[1])
        return self.get_in_range(first, last)

    _COLORS = [
        "#4F7EFF", "#FF6B6B", "#43D9A2", "#FFB347",
        "#A78BFA", "#38BDF8", "#F472B6", "#FBBF24",
    ]
    _color_idx = 0

    def _next_color(self):
        c = self._COLORS[TaskStore._color_idx % len(self._COLORS)]
        TaskStore._color_idx += 1
        return c
