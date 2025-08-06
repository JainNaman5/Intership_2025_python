# Simple To-Do List Application

tasks = []

def load_tasks():
    """Load tasks from file"""
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                task = line.strip()
                if task:
                    tasks.append(task)
        print(f"Loaded {len(tasks)} tasks")
    except FileNotFoundError:
        print("No previous tasks found. Starting fresh!")

def save_tasks():
    """Save tasks to file"""
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")

def add_task():
    """Add a new task"""
    task = input("Enter a new task: ")
    if task:
        tasks.append(task)
        save_tasks()
        print("Task added!")
    else:
        print("Task cannot be empty!")

def view_tasks():
    """Display all tasks"""
    if not tasks:
        print("No tasks found!")
        return
    
    print("\n--- YOUR TO-DO LIST ---")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
    print("-" * 25)

def remove_task():
    """Remove a task"""
    if not tasks:
        print("No tasks to remove!")
        return
    
    view_tasks()
    try:
        task_num = int(input("Enter task number to remove: "))
        if 1 <= task_num <= len(tasks):
            removed = tasks.pop(task_num - 1)
            save_tasks()
            print(f"Removed: {removed}")
        else:
            print("Invalid task number!")
    except ValueError:
        print("Please enter a valid number!")

def show_menu():
    """Display menu options"""
    print("\n=== TO-DO LIST MANAGER ===")
    print("1. Add Task")
    print("2. View Tasks") 
    print("3. Remove Task")
    print("4. Exit")

def main():
    """Main program"""
    print("Welcome to Simple To-Do List!")
    load_tasks()
    
    while True:
        show_menu()
        choice = input("Choose option (1-4): ")
        
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            remove_task()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please choose 1-4.")

# Run the program
if __name__ == "__main__":
    main()