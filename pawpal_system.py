from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict


@dataclass
class Task:
    """Represents a pet care task with scheduling details."""
    description: str
    time: str  # HH:MM format
    frequency: str  # daily/weekly/once
    completed: bool = False

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
        """Get today's tasks (by simple frequency rules)."""
        now = datetime.now()
        weekday = now.strftime("%A").lower()
        valid = []
        for task in self.owner.get_all_tasks():
            if task.completed:
                continue
            freq = task.frequency.lower()
            if freq == "daily":
                valid.append(task)
            elif freq == "weekly":
                valid.append(task)
            elif freq == "once":
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
        """Detect tasks with duplicate times (simple conflict detection)."""
        seen: Dict[str, Task] = {}
        conflicts: List[Task] = []
        for task in tasks:
            if task.time in seen:
                if seen[task.time] not in conflicts:
                    conflicts.append(seen[task.time])
                conflicts.append(task)
            else:
                seen[task.time] = task
        return conflicts</content>
<parameter name="filePath">c:\Users\neba_\Documents\codepath\section 2\project 2\pawpal-starter\pawpal_system.py
