#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime

# Constants
TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def get_new_id(tasks):
    return max([task['id'] for task in tasks], default=0) + 1

def add_task(description):
    tasks = load_tasks()
    new_task = {
        'id': get_new_id(tasks),
        'description': description,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    print(f"Task with ID {task_id} not found")

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully")

def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}")
            return
    print(f"Task with ID {task_id} not found")

def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    
    if not tasks:
        print("No tasks found")
        return

    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}")

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    parser.add_argument('action', choices=['add', 'update', 'delete', 'mark-in-progress', 'mark-done', 'list'])
    parser.add_argument('params', nargs='*', help="Additional parameters for the action")

    args = parser.parse_args()

    try:
        if args.action == 'add':
            if len(args.params) != 1:
                raise ValueError("Add action requires a task description")
            add_task(args.params[0])
        elif args.action == 'update':
            if len(args.params) != 2:
                raise ValueError("Update action requires task ID and new description")
            update_task(int(args.params[0]), args.params[1])
        elif args.action == 'delete':
            if len(args.params) != 1:
                raise ValueError("Delete action requires a task ID")
            delete_task(int(args.params[0]))
        elif args.action == 'mark-in-progress':
            if len(args.params) != 1:
                raise ValueError("Mark-in-progress action requires a task ID")
            mark_task(int(args.params[0]), 'in-progress')
        elif args.action == 'mark-done':
            if len(args.params) != 1:
                raise ValueError("Mark-done action requires a task ID")
            mark_task(int(args.params[0]), 'done')
        elif args.action == 'list':
            if len(args.params) > 1:
                raise ValueError("List action accepts at most one parameter (status)")
            status = args.params[0] if args.params else None
            list_tasks(status)
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()

def create_readme():
    readme_content = '''# Task Tracker CLI

A simple command-line interface for managing tasks.

## Features

- Add, update, and delete tasks
- Mark tasks as in-progress or done
- List all tasks or filter by status

## Usage

```
python task
```
'''
