from pawpal_system import Owner, Pet, Task, Scheduler

# Create an owner
owner = Owner("Alice")

# Create pets with different species
pet1 = Pet("Fluffy", "Cat")
pet2 = Pet("Buddy", "Dog")

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create tasks with different times and frequencies
task1 = Task("Feed breakfast", "08:00", "daily", duration=30)
task2 = Task("Walk", "10:00", "daily", duration=60)
task3 = Task("Vet visit", "14:00", "once", duration=120)

# Add tasks to pets
pet1.add_task(task1)
pet2.add_task(task2)
pet1.add_task(task3)

# Demo conflict detection: Add a conflicting task that overlaps
task4 = Task("Groom", "08:15", "weekly", duration=30)
pet2.add_task(task4)

# Create scheduler
scheduler = Scheduler(owner)

# Print today's schedule
print("Today's Schedule:")
todays_tasks = scheduler.get_todays_tasks()
if todays_tasks:
    for task in todays_tasks:
        status = "Completed" if task.completed else "Pending"
        print(f"- {task.time}: {task.description} ({task.frequency}) - {status}")
else:
    print("No tasks for today.")

# Demo conflict detection with two tasks at the same time
print("\nChecking for conflicts...")
conflicts = scheduler.detect_conflicts(todays_tasks)
if conflicts:
    print("Conflicts detected:")
    for task in conflicts:
        print(f"- {task.time}: {task.description} ({task.frequency})")
else:
    print("No conflicts found.")

# Demo recurring task feature: Mark a daily task complete and show tomorrow's tasks
print("\nMarking 'Feed breakfast' as complete...")
scheduler.mark_task_complete(task1, pet1)

print("\nTomorrow's Schedule (showing new recurring task):")
tomorrows_tasks = scheduler.get_tomorrows_tasks()
if tomorrows_tasks:
    for task in tomorrows_tasks:
        status = "Completed" if task.completed else "Pending"
        print(f"- {task.time}: {task.description} ({task.frequency}) - {status}")
else:
    print("No tasks for tomorrow.")
