import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

tasks = [
    ("Walk Dexter 10am", False),
    ("Hoover floor", False),
    ("Mop floor", False),
    ("Walk Dexter 2PM", False),
    ("Fix printer", False),
    ("Walk Dexter 6pm", False),
    ("Walk Dexter 10pm", False)
]

def main(stdscr):
    stdscr.nodelay(True)
    selected = 0

    while True:
        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            selected = min(selected + 1, len(tasks))
        elif key == ord('x'):
            break
        elif key == curses.KEY_UP:
            selected = max(selected - 1, 0)
        elif key == ord(' ') and selected < len(tasks):
            tasks[selected] = (tasks[selected][0], not tasks[selected][1])
        elif key == ord(' ') and selected == len(tasks):
            add_new_task(stdscr, selected + 2, tasks)
        elif key == ord('d') and selected < len(tasks):
            del tasks[selected]
            selected = max(0, selected - 1)
            if selected == len(tasks) - 1:
                selected += 1
        elif key == ord('r') and selected < len(tasks):
            rename_task(stdscr, selected + 2, tasks, selected)

        render_screen(stdscr, selected, tasks)

def add_new_task(stdscr, y, tasks):
    inp = curses.newwin(1, 50, y, 0)
    txtb = inp.subwin(1, 25, y, 22)
    inp.addstr("Please input new task:")
    tb = Textbox(txtb)
    inp.refresh()
    tb.edit()
    new_task = tb.gather().strip()
    if new_task:
        tasks.append((new_task, False))

def rename_task(stdscr, y, tasks, selected_index):
    inp = curses.newwin(1, 50, y, 0)
    txtb = inp.subwin(1, 25, y, 22)
    inp.addstr("Rename task to:")
    tb = Textbox(txtb)
    inp.refresh()
    tb.edit()
    new_task_name = tb.gather().strip()
    if new_task_name:
        tasks[selected_index] = (new_task_name, tasks[selected_index][1])

def render_screen(stdscr, selected, tasks):
    stdscr.clear()
    curses.curs_set(0)

    stdscr.addstr(0, 0, "Todo List", curses.A_UNDERLINE)
    for i, (task, completed) in enumerate(tasks):
        y = i + 2
        stdscr.addstr(y, 0, f"{i+1})")
        attr = curses.A_BLINK if i == selected else 0
        stdscr.addstr(y, 3, task, attr)
        stdscr.addstr(y, 28, "[X]" if completed else "[ ]")

    add_new_item_text = "Add new item!"
    attr = curses.A_BLINK if selected == len(tasks) else 0
    stdscr.addstr(len(tasks) + 2, 0, add_new_item_text, attr)

    controls_text = "Controls: ↑↓ navigate, Space toggle/add, d delete, r rename, x exit"
    stdscr.addstr(len(tasks) + 3, 0, controls_text)

    stdscr.move(len(tasks) + 2, len(add_new_item_text))

    stdscr.refresh()

wrapper(main)
