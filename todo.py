import streamlit as st
import json
import os
from datetime import datetime

FILE_NAME = "tasks.json"

# ------------- HELPER FUNCTIONS ------------- #

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(task, due_date, category):
    if task:
        task_obj = {
            "task": task,
            "completed": False,
            "due_date": due_date,
            "category": category
        }
        st.session_state.tasks.append(task_obj)
        save_tasks(st.session_state.tasks)

def complete_task(index):
    st.session_state.tasks[index]["completed"] = True
    save_tasks(st.session_state.tasks)

def delete_task(index):
    st.session_state.tasks.pop(index)
    save_tasks(st.session_state.tasks)

# ------------- INIT SESSION STATE ------------- #

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# ------------- UI ------------- #

st.title("📅 To-Do List")

# Add New Task
with st.expander("➕ Add New Task"):
    new_task = st.text_input("Task Description")
    due_date = st.date_input("Due Date")
    category = st.text_input("Category (optional)")
    if st.button("Add Task"):
        add_task(new_task, str(due_date), category)
        st.success("Task added!")

st.divider()

# Filter Options
st.subheader("🔍 Filter Tasks")
filter_option = st.radio("Show:", ["All", "Active", "Completed"], horizontal=True)

# Apply Filter
if filter_option == "Active":
    tasks_to_show = [t for t in st.session_state.tasks if not t["completed"]]
elif filter_option == "Completed":
    tasks_to_show = [t for t in st.session_state.tasks if t["completed"]]
else:
    tasks_to_show = st.session_state.tasks

# Show Tasks
st.subheader("📋 Your Tasks")
if tasks_to_show:
    for i, task_data in enumerate(tasks_to_show):
        task_index = st.session_state.tasks.index(task_data)
        cols = st.columns([4, 2, 2, 1, 1])
        with cols[0]:
            st.markdown(f"{'✅ ' if task_data['completed'] else '🔲 '} **{task_data['task']}**")
        with cols[1]:
            st.markdown(f"📅 Due: `{task_data['due_date']}`")
        with cols[2]:
            st.markdown(f"🏷️ Category: `{task_data['category'] or 'None'}`")
        with cols[3]:
            if not task_data["completed"] and cols[3].button("✅", key=f"done{i}"):
                complete_task(task_index)
        with cols[4]:
            if cols[4].button("❌", key=f"delete{i}"):
                delete_task(task_index)
else:
    st.info("No tasks to display for this filter.")

