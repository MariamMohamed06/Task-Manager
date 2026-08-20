# 📝 Task Manager

A modern desktop Task Manager built with Python and CustomTkinter.

## ✨ Features

- Add new tasks
- Edit existing tasks
- Delete tasks
- Mark tasks as completed or in progress
- Search for tasks
- Filter tasks by status, priority, and category
- Display task statistics
- Save and load tasks using JSON
- Stable task IDs
- Modern dark-themed graphical interface

## 🛠️ Technologies

- Python
- CustomTkinter
- Tkinter
- JSON


## 📁 Project Structure

```text
Task Manager/
│
├── main.py
├── task_app.py
├── task_manager.py
├── tasks.json
├── README.md
└── .gitignore

## 📂 File Description

### `main.py`
Responsible for starting the application and running the main Task Manager window.

### `task_app.py`
Handles the graphical user interface (GUI), including:
- Creating the main window
- Displaying task cards
- Adding and editing tasks
- Searching for tasks
- Filtering tasks
- Completing and deleting tasks
- Updating task statistics
- Validating task input

### `task_manager.py`
Handles task data and business logic, including:
- Adding tasks
- Updating tasks
- Deleting tasks
- Completing tasks
- Loading tasks from JSON
- Saving tasks to JSON
- Generating task statistics
- Managing unique task IDs

### `tasks.json`
Stores the task data locally in JSON format so tasks are saved when the application is closed.

##  How to Run

1. Install Python.

2. Install CustomTkinter:

pip install customtkinter

3. Run the application:

python main.py


