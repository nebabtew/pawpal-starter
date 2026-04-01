from datetime import date
import re

from pawpal_system import Owner, Pet, Task, Scheduler

import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.markdown(
    """
Welcome to PawPal+, your pet care planning assistant!
"""
)

st.divider()

# Add Pet section
st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", key="pet_name")
pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species")
if st.button("Add Pet"):
    if not pet_name.strip():
        st.error("Please enter a pet name")
    else:
        new_pet = Pet(pet_name.strip(), pet_species)
        owner.add_pet(new_pet)
        st.success(f"Added pet: {pet_name.strip()} ({pet_species})")
        st.rerun()

# Display pets
if owner.pets:
    st.write("Current Pets:")
    pet_data = [{"Name": pet.name, "Species": pet.species, "Tasks": len(pet.get_tasks())} for pet in owner.pets]
    st.table(pet_data)
else:
    st.info("No pets added yet.")

st.divider()

# Add Task section
st.subheader("Add a Task")
if owner.pets:
    pet_options = [pet.name for pet in owner.pets]
    selected_pet = st.selectbox("Select Pet", pet_options)
    task_desc = st.text_input("Task description", key="task_desc")
    task_time = st.text_input("Time (HH:MM)", value="08:00", key="task_time")
    task_freq = st.selectbox("Frequency", ["daily", "weekly", "once"], key="task_freq")

    if st.button("Add Task"):
        if not task_desc.strip():
            st.error("Please enter a task description")
        elif not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", task_time.strip()):
            st.error("Please enter time in HH:MM format")
        else:
            task = Task(task_desc.strip(), task_time.strip(), task_freq)
            pet = next(p for p in owner.pets if p.name == selected_pet)
            pet.add_task(task)
            st.success(f"Added task '{task_desc.strip()}' to {selected_pet}")
            st.rerun()
else:
    st.warning("Add a pet first to add tasks.")

st.divider()

# Today's Schedule
st.subheader("Today's Schedule")
filter_choice = st.selectbox("Filter by frequency", ["All", "daily", "weekly", "once"], key="filter_freq")

# Build today's tasks with pet linkage for actions
today_str = date.today().isoformat()
today_tasks_with_pets = []
for pet in owner.pets:
    for task in pet.get_tasks():
        if task.date != today_str or task.completed:
            continue
        if task.frequency.lower() not in ["daily", "weekly", "once"]:
            continue
        if filter_choice != "All" and task.frequency.lower() != filter_choice:
            continue
        today_tasks_with_pets.append((pet, task))

if today_tasks_with_pets:
    st.dataframe([
        {"Time": task.time, "Description": task.description, "Frequency": task.frequency, "Pet": pet.name}
        for pet, task in today_tasks_with_pets
    ])

    for idx, (pet, task) in enumerate(today_tasks_with_pets):
        cols = st.columns([1, 3, 2, 2, 2])
        cols[0].write(task.time)
        cols[1].write(task.description)
        cols[2].write(task.frequency)
        cols[3].write(pet.name)

        if cols[4].button("Mark Complete", key=f"mark_complete_{pet.name}_{task.description}_{task.time}_{idx}"):
            scheduler.mark_task_complete(task, pet)
            st.success("Task completed!")
            if task.frequency.lower() in ["daily", "weekly"]:
                st.info("Next occurrence scheduled")
            st.rerun()

else:
    st.info("No tasks for today.")

# Conflict detection
conflicts = scheduler.detect_conflicts([task for _, task in today_tasks_with_pets])
if conflicts:
    st.warning("Conflicts detected:")
    for task in conflicts:
        st.write(f"- {task.time}: {task.description} ({task.frequency})")
