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

# Owner section
st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
if st.button("Update Owner Name"):
    owner.name = owner_name
    st.success("Owner name updated!")

# Add Pet section
st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", key="pet_name")
pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species")
if st.button("Add Pet"):
    new_pet = Pet(pet_name, pet_species)
    owner.add_pet(new_pet)
    st.success(f"Added pet: {pet_name} ({pet_species})")

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
        task = Task(task_desc, task_time, task_freq)
        pet = next(p for p in owner.pets if p.name == selected_pet)
        pet.add_task(task)
        st.success(f"Added task '{task_desc}' to {selected_pet}")
else:
    st.warning("Add a pet first to add tasks.")

st.divider()

# Today's Schedule
st.subheader("Today's Schedule")
todays_tasks = scheduler.get_todays_tasks()
if todays_tasks:
    task_data = [
        {
            "Time": task.time,
            "Description": task.description,
            "Frequency": task.frequency,
            "Completed": "Yes" if task.completed else "No"
        }
        for task in todays_tasks
    ]
    st.table(task_data)
else:
    st.info("No tasks for today.")

# Conflict detection
conflicts = scheduler.detect_conflicts(todays_tasks)
if conflicts:
    st.warning("Conflicts detected:")
    for task in conflicts:
        st.write(f"- {task.time}: {task.description} ({task.frequency})")
