import sys
import signal
import shlex
import os
import re
from datetime import datetime, timedelta

# --- Constants & ANSI Colors ---
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[32m"
COLOR_RED = "\033[31m"
COLOR_CYAN = "\033[36m"
COLOR_MAGENTA = "\033[35m"
COLOR_YELLOW = "\033[33m"
COLOR_WHITE = "\033[37m"
COLOR_BOLD = "\033[1m"
COLOR_DIM = "\033[2m"
COLOR_BG_CYAN = "\033[46m"
COLOR_BG_RED = "\033[41m"

# Symbols (ASCII fallbacks)
SYM_CHECK = "[X]"
SYM_PENDING = "[ ]"
SYM_BULLET = ">"
SYM_LINE = "-"
SYM_STAR = "*"

# Priority Mapping
PRIORITIES = {"HIGH": 1, "MEDIUM": 2, "LOW": 3}
PRIO_COLORS = {
    "HIGH": f"{COLOR_BG_RED}{COLOR_WHITE}{COLOR_BOLD} HIGH {COLOR_RESET}",
    "MEDIUM": f"{COLOR_YELLOW}{COLOR_BOLD} MED  {COLOR_RESET}",
    "LOW": f"{COLOR_DIM} LOW  {COLOR_RESET}"
}

# --- In-Memory Storage ---
tasks = []
next_id = 1

# --- Foundational Utilities ---

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_message(text, color=COLOR_CYAN):
    print(f"{color}{text}{COLOR_RESET}")

def print_error(text):
    print(f"  {COLOR_RED}{COLOR_BOLD}Error:{COLOR_RESET} {COLOR_RED}{text}{COLOR_RESET}")

def print_success(text):
    print(f"  {COLOR_GREEN}{COLOR_BOLD}Success:{COLOR_RESET} {COLOR_GREEN}{text}{COLOR_RESET}")

def print_warning(text):
    print(f"  {COLOR_YELLOW}{COLOR_BOLD}Warning:{COLOR_RESET} {COLOR_YELLOW}{text}{COLOR_RESET}")

# --- Datetime Helpers ---

def parse_date(date_str):
    if not date_str or date_str.upper() == "NONE":
        return None

    if date_str.lower() == "today":
        return datetime.now().replace(hour=23, minute=59)
    if date_str.lower() == "tomorrow":
        return (datetime.now() + timedelta(days=1)).replace(hour=23, minute=59)

    formats = ["%Y-%m-%d %H:%M", "%Y-%m-%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return "INVALID"

def format_date(dt):
    if not dt:
        return f"{COLOR_DIM}No Deadline{COLOR_RESET}"

    now = datetime.now()
    date_str = dt.strftime("%Y-%m-%d %H:%M")

    if dt < now:
        return f"{COLOR_RED}{COLOR_BOLD}{date_str} (OVERDUE){COLOR_RESET}"
    return f"{COLOR_WHITE}{date_str}{COLOR_RESET}"

# --- Table Layout & Listing ---

def print_banner():
    banner = f"""
    {COLOR_CYAN}{COLOR_BOLD}+------------------------------------------------------------+
    |  {COLOR_WHITE}EVOLUTION OF TODO{COLOR_CYAN}  {COLOR_DIM}|{COLOR_CYAN}  {COLOR_YELLOW}PHASE I: FULL PROGRESSION{COLOR_CYAN}        |
    +------------------------------------------------------------+{COLOR_RESET}
    """
    print(banner)

def print_status_bar():
    completed = sum(1 for t in tasks if t['completed'])
    total = len(tasks)
    overdue = sum(1 for t in tasks if not t['completed'] and t['due_date'] and t['due_date'] < datetime.now())

    status = f"  {COLOR_BG_CYAN}{COLOR_BOLD} STATUS {COLOR_RESET} " \
             f"{COLOR_DIM}Total:{COLOR_RESET} {COLOR_BOLD}{total}{COLOR_RESET} " \
             f"{COLOR_GREEN}Done:{COLOR_RESET} {COLOR_BOLD}{completed}{COLOR_RESET} " \
             f"{COLOR_RED}Overdue:{COLOR_RESET} {COLOR_BOLD}{overdue}{COLOR_RESET}"
    print(status + "\n")

def view_tasks(task_list=None, query_info=None):
    display_list = task_list if task_list is not None else tasks

    if not display_list:
        if query_info:
            print_warning(f"No tasks found for: {query_info}")
        else:
            print("\n  " + f"{COLOR_YELLOW}{SYM_BULLET} {COLOR_DIM}Your list is empty.{COLOR_RESET}\n")
        return

    if query_info:
        print(f"  {COLOR_CYAN}{COLOR_BOLD}Results for:{COLOR_RESET} {COLOR_WHITE}{query_info}{COLOR_RESET}\n")

    print_status_bar()

    # Header
    cols = f"  {COLOR_BOLD}{'ID':<3}  {'Pri':<6}  {'Status':<10}  {'Task Title':<20}  {'Due Date':<20}  {'Tag'}{COLOR_RESET}"
    print(cols)
    print("  " + f"{COLOR_DIM}{SYM_LINE * 85}{COLOR_RESET}")

    for task in display_list:
        prio_label = PRIO_COLORS.get(task['priority'], task['priority'])
        status_color = COLOR_GREEN if task['completed'] else COLOR_RED
        status_sym = SYM_CHECK if task['completed'] else SYM_PENDING
        status_text = "Done" if task['completed'] else "Pending"

        style = COLOR_DIM if task['completed'] else COLOR_BOLD
        tag_str = f"{COLOR_MAGENTA}#{task['tag']}{COLOR_RESET}" if task['tag'] else ""

        row = f"  {COLOR_CYAN}{task['id']:>3}{COLOR_RESET}  " \
              f"{prio_label}  " \
              f"{status_color}{status_sym} {status_text:<7}{COLOR_RESET}  " \
              f"{style}{task['title']:<20}{COLOR_RESET}  " \
              f"{format_date(task['due_date']):<20}  " \
              f"{tag_str}"
        print(row)

    print("\n  " + f"{COLOR_DIM}{SYM_LINE * 85}{COLOR_RESET}\n")

# --- Task Operations ---

def add_task(title, description="", priority="MEDIUM", tag="", due_str=None, recurring=None):
    global next_id
    if not title.strip():
        print_error("Task title cannot be empty.")
        return

    priority = priority.upper()
    if priority not in PRIORITIES:
        priority = "MEDIUM"

    due_date = parse_date(due_str)
    if due_date == "INVALID":
        print_error(f"Invalid date format: {due_str}. Use YYYY-MM-DD or HH:MM.")
        due_date = None

    task = {
        'id': next_id,
        'title': title.strip(),
        'description': description.strip(),
        'completed': False,
        'priority': priority,
        'tag': tag.upper(),
        'due_date': due_date,
        'recurring': recurring.upper() if recurring else None
    }
    tasks.append(task)
    print_success(f"Task '{title}' added! ID: {next_id}")
    next_id = len(tasks) + 1

def handle_recurring(task_id):
    for task in tasks:
        if task['id'] == task_id and task['recurring'] and task['due_date']:
            interval = timedelta(days=1) if task['recurring'] == "DAILY" else timedelta(weeks=1)
            new_due = task['due_date'] + interval
            add_task(task['title'], task['description'], task['priority'], task['tag'], new_due.strftime("%Y-%m-%d %H:%M"), task['recurring'])
            print_message(f"  {SYM_STAR} Recurring task scheduled for: {new_due.strftime('%Y-%m-%d')}", COLOR_MAGENTA)

def toggle_complete(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            status = "completed" if task['completed'] else "pending"
            print_success(f"Task {task_id} is now {status}.")
            if task['completed']:
                handle_recurring(task_id)
            return
    print_error(f"Task with ID {task_id} not found.")

def delete_task(task_id):
    global tasks, next_id
    deleted_task = None
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            deleted_task = tasks.pop(i)
            break

    if deleted_task:
        for i, task in enumerate(tasks):
            task['id'] = i + 1
        next_id = len(tasks) + 1
        print_success(f"Task deleted. List re-indexed.")
    else:
        print_error(f"Task ID {task_id} not found.")

def search_tasks(query):
    query = query.upper()
    results = [t for t in tasks if query in t['title'].upper() or query in t['tag'].upper() or query in t['description'].upper()]
    view_tasks(results, query)

def sort_tasks(criterion):
    global tasks
    criterion = criterion.lower()
    if criterion == "due":
        tasks.sort(key=lambda x: (x['due_date'] is None, x['due_date']))
    elif criterion == "priority":
        tasks.sort(key=lambda x: PRIORITIES.get(x['priority'], 2))
    elif criterion == "title":
        tasks.sort(key=lambda x: x['title'].lower())
    else:
        print_error("Invalid sort criterion. Use: due, priority, or title.")
        return
    print_success(f"Tasks sorted by {criterion}.")
    view_tasks()

def show_help():
    print("\n  " + f"{COLOR_BOLD}{COLOR_WHITE}COMMAND GUIDE{COLOR_RESET}")
    print("  " + f"{COLOR_DIM}{SYM_LINE * 40}{COLOR_RESET}")
    commands = [
        ("add <t> [d] [p] [tag] [due]", "Add a task (p: high/med/low)"),
        ("list", "View all tasks"),
        ("complete <id>", "Toggle status (triggers recurring)"),
        ("delete <id>", "Remove a task"),
        ("search <q>", "Search in titles and tags"),
        ("sort <crit>", "Sort by: due, priority, title"),
        ("clear", "Clear screen"),
        ("quit", "Exit application")
    ]
    for cmd, desc in commands:
        print(f"  {COLOR_CYAN}{cmd:<25}{COLOR_RESET} {COLOR_DIM}{SYM_BULLET} {desc}{COLOR_RESET}")
    print("  " + f"{COLOR_DIM}{SYM_LINE * 40}{COLOR_RESET}\n")

# --- Main Interface ---

def main():
    clear_console()
    print_banner()
    print_message("  Welcome to the Advanced Todo CLI!", COLOR_BOLD)
    print_message("  Type 'help' to get started.\n", COLOR_DIM)

    # Initial Overdue Check
    overdue_count = sum(1 for t in tasks if not t['completed'] and t['due_date'] and t['due_date'] < datetime.now())
    if overdue_count > 0:
        print_warning(f"You have {overdue_count} overdue tasks! Run 'list' to see them.")

    while True:
        try:
            prompt = f"  {COLOR_CYAN}{COLOR_BOLD}todo{COLOR_RESET} {COLOR_DIM}»{COLOR_RESET} "
            user_input = input(prompt).strip()
            if not user_input: continue

            try:
                parts = shlex.split(user_input)
            except ValueError as e:
                print_error(f"Input error: {e}")
                continue

            cmd = parts[0].lower()

            if cmd == "quit":
                print_message("\n  Goodbye! Productivity awaits.", COLOR_GREEN)
                break
            elif cmd == "help":
                show_help()
            elif cmd == "list":
                print("")
                view_tasks()
            elif cmd == "add":
                # args: title, [desc], [prio], [tag], [due], [recurring]
                args = parts[1:] + [None] * 5
                add_task(args[0], args[1] or "", args[2] or "MEDIUM", args[3] or "", args[4], args[5])
            elif cmd == "complete":
                if len(parts) > 1: toggle_complete(int(parts[1]))
                else: print_error("Missing ID.")
            elif cmd == "delete":
                if len(parts) > 1: delete_task(int(parts[1]))
                else: print_error("Missing ID.")
            elif cmd == "search":
                if len(parts) > 1: search_tasks(parts[1])
                else: print_error("Missing query.")
            elif cmd == "sort":
                if len(parts) > 1: sort_tasks(parts[1])
                else: print_error("Usage: sort [due|priority|title]")
            elif cmd == "clear":
                clear_console()
                print_banner()
            else:
                print_error(f"Unknown: '{cmd}'")

        except KeyboardInterrupt:
            print_message("\n\n  Interrupted. Goodbye!", COLOR_GREEN)
            sys.exit(0)
        except Exception as e:
            print_error(f"System error: {e}")

if __name__ == "__main__":
    main()
