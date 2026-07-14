# ============================================================
#  To-Do List Application (Mini Project)
#  Language : Python 3
#  Storage  : tasks.json (JSON file for persistence)
# ============================================================

import json
import os

FILE_NAME = "tasks.json"   # File used to store tasks permanently


# ---------- File Handling ----------

def load_tasks():
    """Load tasks from the JSON file. Return an empty list if file missing."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # If file is corrupted or unreadable, start fresh
        return []


def save_tasks(tasks):
    """Save the tasks list back to the JSON file."""
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)


# ---------- Core Operations ----------

def add_task(tasks):
    """Add a new task to the list."""
    title = input("Enter task title: ").strip()
    if not title:
        print("❌ Task title cannot be empty.\n")
        return
    task = {
        "id": len(tasks) + 1,       # Task number
        "title": title,             # Task title
        "completed": False          # Completion status
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task '{title}' added successfully.\n")


def view_tasks(tasks):
    """Display all tasks in a neat table format."""
    if not tasks:
        print("📭 No tasks found. Add one first!\n")
        return
    print("\n----------------------------------------------------")
    print(f"{'No.':<5}{'Status':<12}{'Title'}")
    print("----------------------------------------------------")
    for i, task in enumerate(tasks, start=1):
        status = "✔ Done" if task["completed"] else "✘ Pending"
        print(f"{i:<5}{status:<12}{task['title']}")
    print("----------------------------------------------------\n")


def mark_completed(tasks):
    """Mark a chosen task as completed."""
    view_tasks(tasks)
    if not tasks:
        return
    index = get_valid_index(len(tasks), "Enter task number to mark completed: ")
    if index is None:
        return
    tasks[index]["completed"] = True
    save_tasks(tasks)
    print(f"✅ Task '{tasks[index]['title']}' marked as completed.\n")


def delete_task(tasks):
    """Delete a task from the list."""
    view_tasks(tasks)
    if not tasks:
        return
    index = get_valid_index(len(tasks), "Enter task number to delete: ")
    if index is None:
        return
    removed = tasks.pop(index)
    # Re-number the remaining tasks
    for i, task in enumerate(tasks, start=1):
        task["id"] = i
    save_tasks(tasks)
    print(f"🗑  Task '{removed['title']}' deleted.\n")


def edit_task(tasks):
    """Edit the title of an existing task."""
    view_tasks(tasks)
    if not tasks:
        return
    index = get_valid_index(len(tasks), "Enter task number to edit: ")
    if index is None:
        return
    new_title = input("Enter new title: ").strip()
    if not new_title:
        print("❌ Title cannot be empty.\n")
        return
    old_title = tasks[index]["title"]
    tasks[index]["title"] = new_title
    save_tasks(tasks)
    print(f"✏  Task '{old_title}' updated to '{new_title}'.\n")


def search_task(tasks):
    """Search tasks by a keyword in the title."""
    if not tasks:
        print("📭 No tasks to search.\n")
        return
    keyword = input("Enter keyword to search: ").strip().lower()
    if not keyword:
        print("❌ Keyword cannot be empty.\n")
        return
    matches = [t for t in tasks if keyword in t["title"].lower()]
    if not matches:
        print(f"🔍 No tasks found matching '{keyword}'.\n")
        return
    print(f"\n🔍 Found {len(matches)} matching task(s):")
    print("----------------------------------------------------")
    for task in matches:
        status = "✔ Done" if task["completed"] else "✘ Pending"
        print(f"{task['id']:<5}{status:<12}{task['title']}")
    print("----------------------------------------------------\n")


# ---------- Helper ----------

def get_valid_index(length, prompt):
    """Ask user for a task number and validate it. Returns 0-based index or None."""
    try:
        num = int(input(prompt))
        if 1 <= num <= length:
            return num - 1
        print("❌ Invalid task number.\n")
    except ValueError:
        print("❌ Please enter a valid integer.\n")
    return None


# ---------- Main Menu ----------

def show_menu():
    print("========== TO-DO LIST MENU ==========")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Completed")
    print("4. Delete Task")
    print("5. Edit Task")
    print("6. Search Task")
    print("7. Exit")
    print("=====================================")


def main():
    tasks = load_tasks()
    while True:
        show_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            mark_completed(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            edit_task(tasks)
        elif choice == "6":
            search_task(tasks)
        elif choice == "7":
            print("👋 Goodbye! Your tasks are saved.")
            break
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 7.\n")


# Entry point of the program
if __name__ == "__main__":
    main()