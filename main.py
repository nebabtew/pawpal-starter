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
task1 = Task("Feed breakfast", "08:00", "daily")
task2 = Task("Walk", "10:00", "daily")
task3 = Task("Vet visit", "14:00", "once")

# Add tasks to pets
pet1.add_task(task1)
pet2.add_task(task2)
pet1.add_task(task3)

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

# Bonus: Mark a task complete
print("\nMarking 'Feed breakfast' as complete...")
task1.mark_complete()

# Show updated schedule
print("\nUpdated Today's Schedule:")
for task in scheduler.get_todays_tasks():
    status = "Completed" if task.completed else "Pending"
    print(f"- {task.time}: {task.description} ({task.frequency}) - {status}")

# Bonus: Add a conflicting task
task4 = Task("Groom", "08:00", "weekly")
pet2.add_task(task4)

# Detect conflicts
print("\nChecking for conflicts...")
conflicts = scheduler.detect_conflicts(scheduler.get_todays_tasks())
if conflicts:
    print("Conflicts detected:")
    for task in conflicts:
        print(f"- {task.time}: {task.description} ({task.frequency})")
else:
    print("No conflicts found.")

# Bonus: Filter by status
print("\nFiltering incomplete tasks:")
incomplete = scheduler.filter_tasks(scheduler.get_todays_tasks(), completed=False)
if incomplete:
    for task in incomplete:
        print(f"- {task.time}: {task.description} ({task.frequency})")
else:
    print("All tasks are complete.")
