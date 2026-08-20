import customtkinter as ctk
from tkinter import messagebox

from task_manager import TaskManager
class TaskApp:
    def __init__(self):
        self.app = ctk.CTk() 
        self.app.title("Task Manager") # title app

        self.app.geometry("1150x700") # app dimensions

        self.app.configure(fg_color="#0B1020") # background color

        self.task_manager = TaskManager()
        self.task_manager.load_tasks() # loading tasks

        self.filtered_tasks = self.task_manager.tasks.copy() # copy tasks

        self.search_after_id = None 

        self.create_header()
        self.create_statistics()
        self.update_statistics()
        self.create_search()
        self.create_tasks()

# header function
    def create_header(self):
        #header frame
        header = ctk.CTkFrame(self.app, fg_color="#0B1020")
        header.pack(fill="x", padx=30, pady=25)

        #header title
        title = ctk.CTkLabel(header, text="Task Manager", font=("Arial", 30, "bold"))
        title.pack(anchor="w")

        # header subtitle
        subtitle = ctk.CTkLabel(header, text="Organize your work, achieve your goals", font=("Arial", 16), text_color="#8B91A5")
        subtitle.pack(anchor="w", pady=(5, 0))

        #"New Task" button
        new_button = ctk.CTkButton(header, text="+ New Task", width=140, height=45, corner_radius=10, font=("Arial", 16, "bold"), fg_color="#18A9E8", hover_color="#168FD0", command=self.add_task)
        new_button.place(relx=1.0, rely=0.5, anchor="e")

# statistics frame
    def create_statistics(self):
        cards_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30, pady=10)

# Create task statistics cards
        self.total_card, self.total_number = self.create_card(cards_frame, "Total Tasks", "0")
        self.completed_card, self.completed_number = self.create_card(cards_frame, "Completed", "0")
        self.progress_card, self.progress_number = self.create_card(cards_frame, "In Progress", "0")
        self.urgent_card, self.urgent_number = self.create_card(cards_frame, "Urgent", "0")

        self.total_card.grid(row=0, column=0, padx=10, sticky="ew")
        self.completed_card.grid(row=0, column=1, padx=10, sticky="ew")
        self.progress_card.grid(row=0, column=2, padx=10, sticky="ew")
        self.urgent_card.grid(row=0, column=3, padx=10, sticky="ew")

# Configure equal column widths for the cards
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)
        cards_frame.grid_columnconfigure(3, weight=1)

# search frame
    def create_search(self):
        search_frame = ctk.CTkFrame(self.app, fg_color="#151C2F", corner_radius=15)
        search_frame.pack(fill="x", padx=30, pady=20)
        # search bar
        self.search_entry = ctk.CTkEntry(search_frame, width=600, height=45, placeholder_text="⌕  Search tasks...", fg_color="#151C2F", border_color="#252D42")
        self.search_entry.pack(side="left", padx=15, pady=15)
        self.search_entry.bind("<KeyRelease>", self.search_tasks)
        # Create status filter menu
        self.status_menu = ctk.CTkOptionMenu(search_frame, values=["All Status", "In Progress", "Completed"], width=140, height=40)
        self.status_menu.pack(side="left", padx=5)
        self.status_menu.configure(command=self.filter_tasks)
        # Create status priority menu
        self.priority_menu = ctk.CTkOptionMenu(search_frame, values=["All Priorities", "Low", "Medium", "High", "Urgent"], width=140, height=40, fg_color="#1769AA", button_color="#155A8A", button_hover_color="#2079B5")
        self.priority_menu.pack(side="left", padx=5)
        self.priority_menu.configure(command=self.filter_tasks)
        # Create status category menu
        self.category_menu = ctk.CTkOptionMenu(search_frame, values=["All Categories", "Work", "Study", "Personal"], width=140, height=40, fg_color="#1769AA", button_color="#155A8A", button_hover_color="#2079B5")
        self.category_menu.pack(side="left", padx=5)
        self.category_menu.configure(command=self.filter_tasks)

#tasks frame 
    def create_tasks(self):
        self.tasks_frame = ctk.CTkScrollableFrame(self.app, fg_color="transparent")
        self.tasks_frame.pack(fill="both", expand=True, padx=30, pady=10)
        self.show_task_cards()

# Display task cards
    def show_task_cards(self, tasks=None):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        if tasks is None:
            tasks = self.task_manager.tasks
        for task in tasks:
            status = "Completed" if task["completed"] else "In Progress"
            card = self.create_task_card(self.tasks_frame, task["id"], task["title"], status, task["priority"], task["category"], task["time"])
            card.pack(fill="x", padx=10, pady=10)

    def create_task_card(self, parent, task_id, name, status, priority, category, time):
         # Set the color based on task priority
        if priority == "Urgent":
            line_color = "#EF4444"
        elif priority == "High":
            line_color = "#F97316"
        elif priority == "Medium":
            line_color = "#EAB308"
        else:
            line_color = "#22C55E"

        # Create the task card
        card = ctk.CTkFrame(parent, width=350, height=150, corner_radius=15, fg_color="#151C2F", border_width=1, border_color="#252D42")
        color_line = ctk.CTkFrame(card, width=5, height=150, fg_color=line_color, corner_radius=5)
        color_line.place(x=0, y=0)

        # Add task title 
        title = ctk.CTkLabel(card, text=name, font=("Arial", 16, "bold"), wraplength=500)
        title.pack(anchor="w", padx=25, pady=(15, 5))

        # Create task information section
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(anchor="w", padx=25, pady=5)

        # Display task status
        status_label = ctk.CTkLabel(info_frame, text=status, font=("Arial", 12), fg_color="#1769AA", corner_radius=10)
        status_label.pack(side="left", padx=3)

        # Display task priority
        priority_label = ctk.CTkLabel(info_frame, text=priority, font=("Arial", 12), fg_color=line_color, corner_radius=10)
        priority_label.pack(side="left", padx=3)

        # Display task category
        category_label = ctk.CTkLabel(info_frame, text=category, font=("Arial", 12), fg_color="#5540A8", corner_radius=10)
        category_label.pack(side="left", padx=3)

         # Display task time
        time_label = ctk.CTkLabel(card, text="◷  " + time, font=("Arial", 13), text_color="#8B91A5")
        time_label.pack(anchor="w", padx=25, pady=3)

         # Create button section
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(anchor="e", padx=15, pady=3)

        # Create delete button
        delete_button = ctk.CTkButton(button_frame, text="Delete", width=65, height=26, corner_radius=8, font=("Arial", 12, "bold"), fg_color="#EF4444", hover_color="#DC2626", command=lambda: self.delete_task(task_id))
        delete_button.pack(side="left", padx=5)

 # Set complete button properties based on task status
        if status == "Completed":
            button_text = "In Progress"
            button_color = "#F97316"
            hover_color = "#EA580C"
        else:
            button_text = "Complete"
            button_color = "#22C55E"
            hover_color = "#16A34A"

        # Create complete button
        complete_button = ctk.CTkButton(button_frame, text=button_text, width=80, height=26, font=("Arial", 12, "bold"), fg_color=button_color, hover_color=hover_color, command=lambda: self.complete_task(task_id))
        complete_button.pack(side="left", padx=5)

         # Create edit button
        edit_button = ctk.CTkButton(button_frame, text="Edit", width=60, height=26, font=("Arial", 12, "bold"), fg_color="#3B82F6", hover_color="#2563EB", command=lambda: self.edit_task(task_id))
        edit_button.pack(side="left", padx=5)

        return card
    
# Create a statistics card with an icon, label, and number
    def create_card(self, parent, name, number):
        if name == "Total Tasks":
            icon = "☷"
            icon_color = "#2196F3"
        elif name == "Completed":
            icon = "✓"
            icon_color = "#22C55E"
        elif name == "In Progress":
            icon = "◷"
            icon_color = "#EAB308"
        else:
            icon = "!"
            icon_color = "#EF4444"

        card = ctk.CTkFrame(parent, width=250, height=95, corner_radius=15, fg_color="#151C2F", border_width=1, border_color="#252D42")

        icon_frame = ctk.CTkFrame(card, width=40, height=40, corner_radius=10, fg_color="#202A40")
        icon_frame.pack(side="left", padx=15, pady=15)

        icon_label = ctk.CTkLabel(icon_frame, text=icon, font=("Arial", 18, "bold"), text_color=icon_color)
        icon_label.place(relx=0.5, rely=0.5, anchor="center")

        text_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_frame.pack(side="left", pady=10)

        label = ctk.CTkLabel(text_frame, text=name, font=("Arial", 13), text_color="#858CA0")
        label.pack(anchor="w")

        number_label = ctk.CTkLabel(text_frame, text=number, font=("Arial", 24, "bold"))
        number_label.pack(anchor="w")

        return card, number_label

    def add_task(self):
        task_window = ctk.CTkToplevel(self.app)
        task_window.title("New Task")

        task_window.geometry("500x560")
# Configure the task window
        task_window.configure(fg_color="#07152A")
        task_window.transient(self.app)
        task_window.grab_set()
        task_window.focus_force()
        task_window.lift()
#title section
        title_frame = ctk.CTkFrame(task_window, fg_color="transparent")
        title_frame.pack(fill="x", padx=35, pady=(25, 10))

        icon = ctk.CTkLabel(title_frame, text="⊕", font=("Arial", 28, "bold"), text_color="white", fg_color="#1677E8", corner_radius=12, width=50, height=50)
        icon.pack(side="left")

        title_text = ctk.CTkLabel(title_frame, text="New Task", font=("Arial", 24, "bold"))
        title_text.pack(side="left", padx=15)

# Create task name input
        name_label = ctk.CTkLabel(task_window, text="Task name", font=("Arial", 14, "bold"))
        name_label.pack(anchor="w", padx=35, pady=(20, 8))

        name_entry = ctk.CTkEntry(task_window, width=430, height=48, placeholder_text="Enter task name", fg_color="#07152A", border_color="#1769AA", border_width=2)
        name_entry.pack(padx=35)

# Create priority and category options
        options_frame = ctk.CTkFrame(task_window, fg_color="transparent")
        options_frame.pack(fill="x", padx=35, pady=(35, 0))

        priority_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        priority_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        priority_label = ctk.CTkLabel(priority_frame, text="Priority", font=("Arial", 14, "bold"))
        priority_label.pack(anchor="w", pady=(0, 8))

        priority_menu = ctk.CTkOptionMenu(priority_frame, values=["Low", "Medium", "High", "Urgent"], height=48, fg_color="#0B2A50", button_color="#0B2A50", button_hover_color="#1769AA")
        priority_menu.set("Medium")
        priority_menu.pack(fill="x")
        
        category_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        category_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))

        category_label = ctk.CTkLabel(category_frame, text="Category", font=("Arial", 14, "bold"))
        category_label.pack(anchor="w", pady=(0, 8))

        category_menu = ctk.CTkOptionMenu(category_frame, values=["Work", "Study", "Personal"], height=48, fg_color="#0B2A50", button_color="#0B2A50", button_hover_color="#1769AA")
        category_menu.set("Study")
        category_menu.pack(fill="x")

# Create time input
        time_label = ctk.CTkLabel(task_window, text="Time", font=("Arial", 14, "bold"))
        time_label.pack(anchor="w", padx=35, pady=(35, 8))

        time_entry = ctk.CTkEntry(task_window, width=430, height=48, placeholder_text="Example: 2 hours", fg_color="#07152A", border_color="#1769AA", border_width=2)
        time_entry.pack(padx=35)

# Save and validate the new task
        def save():
            try:
                # Get task details from the input fields
                name = name_entry.get().strip()
                priority = priority_menu.get()
                category = category_menu.get()
                time = time_entry.get().strip()
                # Check if the task name is empty
                if name == "":
                    messagebox.showwarning("Missing Task Name", "Please enter a task name.")
                    return
                # Check if the task already exists
                for task in self.task_manager.tasks:
                    if task["title"].lower() == name.lower():
                        messagebox.showwarning("Duplicate Task", "This task already exists.")
                        return
                # Check if the time is empty
                if time == "":
                    messagebox.showwarning("Missing Time", "Please enter the task time.")
                    return
                # Validate the time format
                if not self.validate_time(time):
                    messagebox.showwarning("Invalid Time","Please enter a valid time like 2 hours or 30 min.")
                    return
                # Validate the selected priority
                if priority not in ["Low", "Medium", "High", "Urgent"]:
                    messagebox.showwarning("Invalid Priority", "Please select a valid priority.")
                    return
                # Validate the selected category
                if category not in ["Work", "Study", "Personal"]:
                    messagebox.showwarning("Invalid Category", "Please select a valid category.")
                    return
                
                # Add the new task and refresh
                self.task_manager.add_task(name, priority, category, time)
                self.update_statistics()
                self.refresh_tasks()
                task_window.destroy()
            except Exception:
                messagebox.showerror("Error", "Something went wrong while adding the task.")

         # save button
        save_button = ctk.CTkButton(task_window, text="▣  Save Task", width=430, height=50, corner_radius=8, font=("Arial", 14, "bold"), fg_color="#1677E8", hover_color="#1264C5", command=save)
        save_button.pack(padx=35, pady=25)

# edit function
    def edit_task(self, task_id):
        for task in self.task_manager.tasks:
            if task["id"] == task_id:
                task_window = ctk.CTkToplevel(self.app)
                task_window.title("Edit Task")

                task_window.geometry("500x560")

                task_window.configure(fg_color="#07152A")
                task_window.transient(self.app)
                task_window.grab_set()
                task_window.focus_force()
                task_window.lift()

                header = ctk.CTkFrame(task_window, fg_color="transparent")
                header.pack(fill="x", padx=35, pady=(25, 20))

                icon = ctk.CTkLabel(header, text="✎", font=("Arial", 28, "bold"), text_color="white", fg_color="#1677E8", corner_radius=12, width=50, height=50)
                icon.pack(side="left")

                title = ctk.CTkLabel(header, text="Edit Task", font=("Arial", 24, "bold"))
                title.pack(side="left", padx=15)

                name_label = ctk.CTkLabel(task_window, text="Task name", font=("Arial", 14, "bold"))
                name_label.pack(anchor="w", padx=35, pady=(5, 8))
                name_entry = ctk.CTkEntry(task_window, width=430, height=48, font=("Arial", 14), fg_color="#07152A", border_color="#1769AA", border_width=2)
                name_entry.insert(0, task["title"])
                name_entry.pack(padx=35)

                options_frame = ctk.CTkFrame(task_window, fg_color="transparent")
                options_frame.pack(fill="x", padx=35, pady=(25, 0))

                priority_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
                priority_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

                priority_label = ctk.CTkLabel(priority_frame, text="Priority", font=("Arial", 14, "bold"))
                priority_label.pack(anchor="w", pady=(0, 8))

                priority_menu = ctk.CTkOptionMenu(priority_frame, values=["Low", "Medium", "High", "Urgent"], height=48, font=("Arial", 14), fg_color="#0B2A50", button_color="#0B2A50", button_hover_color="#1769AA")
                priority_menu.set(task["priority"])
                priority_menu.pack(fill="x")

                category_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
                category_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))

                category_label = ctk.CTkLabel(category_frame, text="Category", font=("Arial", 14, "bold"))
                category_label.pack(anchor="w", pady=(0, 8))
                
                category_menu = ctk.CTkOptionMenu(category_frame, values=["Work", "Study", "Personal"], height=48, font=("Arial", 14), fg_color="#0B2A50", button_color="#0B2A50", button_hover_color="#1769AA")
                category_menu.set(task["category"])
                category_menu.pack(fill="x")

                time_label = ctk.CTkLabel(task_window, text="Time", font=("Arial", 14, "bold"))
                time_label.pack(anchor="w", padx=35, pady=(25, 8))

                time_entry = ctk.CTkEntry(task_window, width=430, height=48, font=("Arial", 14), fg_color="#07152A", border_color="#1769AA", border_width=2)
                time_entry.insert(0, task["time"])
                time_entry.pack(padx=35)

                # save of edit function
                def save():
                    try:
                        name = name_entry.get().strip()
                        priority = priority_menu.get()
                        category = category_menu.get()
                        time = time_entry.get().strip()
                        if name == "":
                            messagebox.showwarning("Missing Task Name", "Please enter a task name.")
                            return
                        
                        for old_task in self.task_manager.tasks:
                            if old_task["id"] != task_id and old_task["title"].lower() == name.lower():
                                messagebox.showwarning("Duplicate Task", "This task already exists.")
                                return
                            
                        if time == "":
                            messagebox.showwarning("Missing Time", "Please enter the task time.")
                            return
                        
                        if not self.validate_time(time):
                            messagebox.showwarning("Invalid Time", "Please enter a valid time.")
                            return
                        
                        self.task_manager.update_task(task_id, name, priority, category, time)
                        self.update_statistics()
                        self.refresh_tasks()
                        task_window.destroy()
                    except Exception:
                        messagebox.showerror("Error", "Something went wrong while editing the task.")

                save_button = ctk.CTkButton(task_window, text="▣  Save Task", width=430, height=50, corner_radius=8, font=("Arial", 14, "bold"), fg_color="#1677E8", hover_color="#1264C5", command=save)
                save_button.pack(padx=35, pady=25)
                break

#delete function
    def delete_task(self, task_id):
        try:
            # ask for confirmation before delete
            answer = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
            if answer:
                # delete the task and refresh
                self.task_manager.delete_task(task_id)
                self.update_statistics()
                self.refresh_tasks()
        except Exception:
            messagebox.showerror("Error", "Something went wrong while deleting the task.")

# complete task function
    def complete_task(self, task_id):
        try:
            self.task_manager.complete_task(task_id)
            self.update_statistics()
            self.refresh_tasks()
        except Exception:
            messagebox.showerror("Error", "Something went wrong while updating the task.")

# search for task
    def search_tasks(self, event=None):
        if self.search_after_id is not None:
            self.app.after_cancel(self.search_after_id)
        self.search_after_id = self.app.after(200, self.filter_tasks)

#filter function
    def filter_tasks(self, choice=None):
        self.search_after_id = None
        tasks = []

# Get the current filter values
        text = self.search_entry.get().strip().lower()

        status = self.status_menu.get()
        priority = self.priority_menu.get()
        category = self.category_menu.get()

# Check each task against the selected filters
        for task in self.task_manager.tasks:
            if text and text not in task["title"].lower():
                continue
            if status == "Completed" and not task["completed"]:
                continue
            if status == "In Progress" and task["completed"]:
                continue
            if priority != "All Priorities" and task["priority"] != priority:
                continue
            if category != "All Categories" and task["category"] != category:
                continue
            tasks.append(task)

        #update the filtered task list
        self.filtered_tasks = tasks
        self.show_task_cards(tasks)

# Refresh the displayed tasks
    def refresh_tasks(self):
        self.filter_tasks()

# Update the task statistics
    def update_statistics(self):
        total, completed, in_progress, urgent = self.task_manager.get_statistics()
        self.total_number.configure(text=str(total))
        self.completed_number.configure(text=str(completed))
        self.progress_number.configure(text=str(in_progress))
        self.urgent_number.configure(text=str(urgent))

# Validate the task time format
    def validate_time(self, time):
        time = time.strip().lower()
        parts = time.split()
        if len(parts) != 2:
            return False
        try:
            value = float(parts[0])
        except ValueError:
            return False
        if value <= 0:
            return False
        unit = parts[1]
        valid_units = ["hour", "hours", "hr", "hrs", "minute", "minutes", "min", "mins"]
        return unit in valid_units

    def run(self):
        self.app.mainloop()