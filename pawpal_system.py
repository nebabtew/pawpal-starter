from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import List, Dict


@dataclass
class Task:
    """Represents a pet care task with scheduling details."""
    description: str
    time: str  # HH:MM format
    frequency: str  # daily/weekly/once
    duration: int = 30  # duration in minutes
    completed: bool = False
    date: str = field(default_factory=lambda: date.today().isoformat())  # YYYY-MM-DD format

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Pet:
    """Represents a pet with its care tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet."""
        if not isinstance(task, Task):
            raise TypeError("Expected Task instance")
        if task in self.tasks:
            return
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Get all tasks for the pet."""
        return list(self.tasks)


class Owner:
    """Manages pets and aggregates their tasks."""
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        if not isinstance(pet, Pet):
            raise TypeError("Expected Pet instance")
        if pet in self.pets:
            return
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks across all pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks


class Scheduler:
    """Manages task scheduling for an owner."""
    def __init__(self, owner: Owner):
        if not isinstance(owner, Owner):
            raise TypeError("Expected Owner instance")
        self.owner = owner

    def get_todays_tasks(self) -> List[Task]:
        """Get today's tasks (by date and frequency rules)."""
        today = date.today().isoformat()
        valid = []
        for task in self.owner.get_all_tasks():
            if task.date != today:
                continue
            if task.completed:
                continue
            freq = task.frequency.lower()
            if freq in ["daily", "weekly", "once"]:
                valid.append(task)
        return self.sort_by_time(valid)

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by time in HH:MM format."""
        def parse_time(task: Task):
            try:
                return datetime.strptime(task.time, "%H:%M").time()
            except ValueError:
                return datetime.min.time()

        return sorted(tasks, key=parse_time)

    def filter_tasks(self, tasks: List[Task], completed: bool = False, frequency: str = None) -> List[Task]:
        """Filter tasks by completion status and optionally frequency."""
        filtered = []
        for task in tasks:
            if task.completed != completed:
                continue
            if frequency and task.frequency.lower() != frequency.lower():
                continue
            filtered.append(task)
        return filtered

    def detect_conflicts(self, tasks: List[Task]) -> List[Task]:
        """Detect tasks with overlapping time ranges based on start time and duration."""
        conflicts: List[Task] = []
        for i, task1 in enumerate(tasks):
            start1 = datetime.strptime(task1.time, "%H:%M").time()
            end1 = (datetime.combine(date.today(), start1) + timedelta(minutes=task1.duration)).time()
            for j, task2 in enumerate(tasks):
                if i >= j:
                    continue
                start2 = datetime.strptime(task2.time, "%H:%M").time()
                end2 = (datetime.combine(date.today(), start2) + timedelta(minutes=task2.duration)).time()
                # Check for overlap: task1 starts before task2 ends and task2 starts before task1 ends
                if start1 < end2 and start2 < end1:
                    if task1 not in conflicts:
                        conflicts.append(task1)
                    if task2 not in conflicts:
                        conflicts.append(task2)
        return conflicts

    def get_tomorrows_tasks(self) -> List[Task]:
        """Get tomorrow's tasks (by date and frequency rules)."""
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        valid = []
        for task in self.owner.get_all_tasks():
            if task.date != tomorrow:
                continue
            if task.completed:
                continue
            freq = task.frequency.lower()
            if freq in ["daily", "weekly", "once"]:
                valid.append(task)
        return self.sort_by_time(valid)

    def mark_task_complete(self, task: Task, pet: Pet) -> None:
        """Mark a task complete and create next occurrence if recurring."""
        task.mark_complete()
        if task.frequency in ["daily", "weekly"]:
            current_date = date.fromisoformat(task.date)
            if task.frequency == "daily":
                next_date = current_date + timedelta(days=1)
            else:
                next_date = current_date + timedelta(days=7)
            new_task = Task(
                description=task.description,
                time=task.time,
                frequency=task.frequency,
                date=next_date.isoformat()
            )
            pet.add_task(new_task)
