import os
import json
from datetime import datetime

FILE_PATH = "notes.json"

def init_json():
    
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump({"notes": []}, f, ensure_ascii=False, indent=2)

def load_notes() -> list:
   
    init_json()
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("notes", [])
    except json.JSONDecodeError:
        return []

def save_notes(notes: list):
    
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump({"notes": notes}, f, ensure_ascii=False, indent=2)

def add_note(title: str, text: str):
    
    notes = load_notes()
    
    note_id = max([note["id"] for note in notes], default=0) + 1
    
    new_note = {
        "id": note_id,
        "title": title,
        "text": text,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    notes.append(new_note)
    save_notes(notes)

def delete_note(note_id: int) -> bool:
    
    notes = load_notes()
    initial_length = len(notes)
    notes = [note for note in notes if note["id"] != note_id]
    
    if len(notes) < initial_length:
        save_notes(notes)
        return True
    return False

def edit_note(note_id: int, key: str, new_value: str) -> bool:
    
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            note[key] = new_value
            note["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M") 
            save_notes(notes)
            return True
    return False