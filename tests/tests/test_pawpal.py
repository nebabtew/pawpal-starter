import os
import sys

# Ensure repository root is on sys.path for module imports during pytest runs.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_completion():
    """Test that marking a task complete sets completed to True."""
    task = Task("Test task", "10:00", "daily")
    assert not task.completed
    task.mark_complete()
    assert task.completed


def test_task_addition():
    """Test adding a task to a pet increases task count."""
    pet = Pet("TestPet", "Dog")
    assert len(pet.get_tasks()) == 0
    task = Task("Feed", "08:00", "daily")
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1


def test_scheduler_sort_by_time():
    """Test sort_by_time returns tasks in chronological order."""
    owner = Owner("Owner")
    pet = Pet("TestPet", "Cat")
    owner.add_pet(pet)

    task_late = Task("Play", "14:00", "once")
    task_early = Task("Feed", "08:00", "once")
    task_mid = Task("Walk", "10:00", "once")

    pet.add_task(task_late)
    pet.add_task(task_early)
    pet.add_task(task_mid)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(pet.get_tasks())

    assert [t.time for t in sorted_tasks] == ["08:00", "10:00", "14:00"]


def test_daily_recurrence_mark_task_complete_adds_next_day():
    """Test marking a daily task complete adds next-day task."""
    from datetime import date, timedelta

    owner = Owner("Owner")
    pet = Pet("TestPet", "Dog")
    owner.add_pet(pet)

    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    task = Task("Walk", "09:00", "daily", date=today)
    pet.add_task(task)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(task, pet)

    all_task_dates = [t.date for t in pet.get_tasks()]
    assert task.completed
    assert tomorrow in all_task_dates
    assert len([t for t in pet.get_tasks() if t.date == tomorrow and t.description == "Walk"]) == 1


def test_detect_conflicts_same_time_returns_both():
    """Test conflict detection for two tasks at same time."""
    owner = Owner("Owner")
    pet = Pet("TestPet", "Bird")
    owner.add_pet(pet)

    task1 = Task("Feed", "09:00", "once", duration=30)
    task2 = Task("Vet", "09:00", "once", duration=30)

    pet.add_task(task1)
    pet.add_task(task2)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(pet.get_tasks())

    assert task1 in conflicts
    assert task2 in conflicts
    assert len(conflicts) == 2
