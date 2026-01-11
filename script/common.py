import json
import os
import shutil
from kivy.utils import platform
from kivy.app import App

base_dir = os.path.dirname(__file__)

def get_writable_file_path(filename):
    """Returns the path to a writable file. Copies from assets if necessary."""
    if platform == 'android':
        app = App.get_running_app()
        # Fallback if App is not yet running (unlikely for these calls)
        storage_dir = app.user_data_dir if app else "."
        target_dir = os.path.join(storage_dir, "json")
    else:
        target_dir = os.path.join(base_dir, "json")
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        
    target_path = os.path.join(target_dir, filename)
    
    # If file doesn't exist in writable path, try to copy from assets (base_dir/json)
    if not os.path.exists(target_path):
        source_path = os.path.join(base_dir, "json", filename)
        if os.path.exists(source_path):
            try:
                shutil.copy2(source_path, target_path)
            except Exception as e:
                print(f"Error copying file {filename}: {e}")
                # Fallback: try to just open and write if copy fails?
                # Or just return None/source path so at least we can read?
                # For now just print error.
                pass
             
    return target_path

def get_settings(value):
    setting_path = get_writable_file_path("settings.json")

    if os.path.exists(setting_path):
        with open(setting_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                return data.get(value)
            except json.JSONDecodeError:
                 print(f"JSON Decode Error in {setting_path}")
                 return None
    else:
        return None

def get_subject_json(type):
    # Questions are read-only, keep loading from assets
    if type == "math":
        setting_path = os.path.join(base_dir, "questions", "math.json")
    elif type == "social":
        setting_path = os.path.join(base_dir, "questions", "socialStudy.json")
    elif type == "science":
        setting_path = os.path.join(base_dir, "questions", "science.json")
    else:
        return None

    if os.path.exists(setting_path):
        with open(setting_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    else:
        return None

def get_rewards():
    path = get_writable_file_path("rewards.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None
    return None

def add_reward(subject,point):
    path = get_writable_file_path("rewards.json")
    # Ensure file exists/is copied
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    data[subject] = data[subject] + point
    data["total"] = data["total"] + point
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def set_setting(key, value):
    setting_path = get_writable_file_path("settings.json")
    
    if os.path.exists(setting_path):
        with open(setting_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        data[key] = value
        
        with open(setting_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

def reset_rewards():
    path = get_writable_file_path("rewards.json")
    # 初期データ
    data = {
        "total": 0,
        "math": 0,
        "social": 0,
        "science": 0
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_texts():
    return {
        "next_button": "次へ",
        "correct_answer": "せいかい",
        "wrong_answer": "ちがうよ",
        "try_again": "やりなおう",
        "try_input": "こたえをいれてね",
        "determine_button": "けってい"
    }