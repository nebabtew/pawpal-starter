from pawpal_system import Task, Pet


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
