import sys, os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)

from storage import load_tasks, save_tasks
from ui import MainView

def main():
    tasks = load_tasks()
    app = MainView(tasks)
    app.mainloop()
    save_tasks(tasks)

if __name__ == "__main__":
    main()
