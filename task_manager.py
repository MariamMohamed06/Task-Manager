import json
import os
from tkinter import messagebox


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.file_name = os.path.join(os.path.dirname(__file__), "tasks.json")

# save tasks fe file json 
    def save_tasks(self):
        try:
            with open(self.file_name, "w") as file:
                json.dump(self.tasks, file, indent=4)
        except PermissionError:
            messagebox.showerror("Error", "You do not have permission to save the tasks.")
        except OSError:
            messagebox.showerror("Error", "Could not save the tasks file.")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong while saving the tasks:\n{e}")

# make sure that all ids s7 w not repeated
    def load_tasks(self):
        try:
            with open(self.file_name, "r") as file:
                self.tasks = json.load(file)

            used_ids = set()
            ids_changed = False

            for task in self.tasks:
                task_id = task.get("id")

                if not isinstance(task_id, int) or task_id in used_ids:
                    task["id"] = max(used_ids, default=0) + 1
                    ids_changed = True

                used_ids.add(task["id"])

            if ids_changed:
                self.save_tasks()

        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "The tasks file is not valid.")
            self.tasks = []
        except PermissionError:
            messagebox.showerror("Error", "Permission denied while opening the tasks file.")
            self.tasks = []
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong while loading tasks:\n{e}")
            self.tasks = []

# add new task
    def add_task(self, name, priority, category, time):
        new_id = max([task["id"] for task in self.tasks], default=0) + 1
        task = {"id": new_id, "title": name, "completed": False, "priority": priority, "category": category, "time": time}

        self.tasks.append(task) # add to list
        self.save_tasks() #  save to json file

#delete task
    def delete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task) #remove it from list
                break
        self.save_tasks() # save changes in json file

# complete task (Marked as complete)
    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                break
        self.save_tasks()

#edit task
    def update_task(self, task_id, name, priority, category, time):
        for task in self.tasks: 
            if task["id"] == task_id:
                task["title"] = name
                task["priority"] = priority
                task["category"] = category
                task["time"] = time
                break
        self.save_tasks()

#calculate all statistics numbers (Total tasks , in progress tasks , completed tasks , urget tasks "priority"")
    def get_statistics(self):
        total = len(self.tasks)
        completed = 0
        in_progress = 0
        urgent = 0

        for task in self.tasks:
            if task["completed"]:
                completed += 1
            else:
                in_progress += 1

            if task["priority"] == "Urgent":
                urgent += 1

        return total, completed, in_progress, urgent  # return statistics numebrs