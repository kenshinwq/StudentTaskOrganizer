import os
import json
from models import Task
from json import JSONDecodeError

DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'data', 'tasks.json'
)

def load_tasks():
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if not content:
            data_list = []
        else:
            try:
                data_list = json.loads(content)
            except JSONDecodeError:
                data_list = []
    return [Task.from_dict(item) for item in data_list]

def save_tasks(tasks):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)
