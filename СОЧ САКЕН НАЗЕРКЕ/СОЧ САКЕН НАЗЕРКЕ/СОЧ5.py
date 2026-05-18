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
from telebot import types


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("📄 Notes list")
    btn2 = types.KeyboardButton("➕ Create note")
    btn3 = types.KeyboardButton("✏️ Change")
    btn4 = types.KeyboardButton("❌ Delete note")
    btn5 = types.KeyboardButton("ℹ️ Help")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)

    return markup
{
"notes": []
}
from keyboards.menu import main_menu


def register_start_handlers(bot):

    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(
            message.chat.id,
            "👋 Welcome to note bot!\n\n"
            "Choose action:",
            reply_markup=main_menu()
        )
       
        from telebot import types
from utils import json_manager
from keyboards import menu
TOKEN = "8938333971:AAE_TKei4ZSLvF2MVwbWjKzU8flLEjNgfS0"
user_states = {}

def register_notes_handlers(bot):
    
    
    @bot.message_handler(func=lambda message: message.text == "📄 List of notes")
    def show_notes_list(message):
        notes = json_manager.load_notes()
        if not notes:
            bot.send_message(message.chat.id, "📭 You dont have notes yet.")
            return
        
        bot.send_message(
            message.chat.id, 
            "📋 Choose a note to read:", 
            reply_markup=menu.get_notes_inline_keyboard(notes, "view")
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("view_"))
    def view_note_callback(call):
        note_id = int(call.data.split("_")[1])
        notes = json_manager.load_notes()
        note = next((n for n in notes if n["id"] == note_id), None)
        
        if note:
            response = (
                f"📌 **{note['title']}**\n\n"
                f"{note['text']}\n\n"
                f"📅 _Дата: {note['created_at']}_"
            )
            bot.send_message(call.message.chat.id, response, parse_mode="Markdown")
        else:
            bot.send_message(call.message.chat.id, "❌ Note not found.")
        bot.answer_callback_query(call.id)

   
    @bot.message_handler(func=lambda message: message.text == "➕ Create note")
    def create_note_start(message):
        msg = bot.send_message(message.chat.id, "✍️ Enter a  **name** for a new note:", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_note_title)

    def process_note_title(message):
        title = message.text
        msg = bot.send_message(message.chat.id, "📝 Now enter notes **text**:", parse_mode="Markdown")
        bot.register_next_step_handler(msg, process_note_text, title)

    def process_note_text(message, title):
        text = message.text
        json_manager.add_note(title, text)
        bot.send_message(message.chat.id, "✅ Note saved!")

  
    @bot.message_handler(func=lambda message: message.text == "❌ Delete note")
    def delete_note_start(message):
        notes = json_manager.load_notes()
        if not notes:
            bot.send_message(message.chat.id, "📭 Nothing to delete.")
            return
        
        bot.send_message(
            message.chat.id, 
            "🗑 Choose a note you wish to delete:", 
            reply_markup=menu.get_notes_inline_keyboard(notes, "confirm_del")
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_del_"))
    def confirm_delete_callback(call):
        note_id = int(call.data.split("_")[2])
        
        
        markup = types.InlineKeyboardMarkup()
        btn_yes = types.InlineKeyboardButton("✅ Yes, delete" \, callback_data=f"del_yes_{note_id}")
        btn_no = types.InlineKeyboardButton("❌ Cancel", callback_data="del_no")
        markup.row(btn_yes, btn_no)
        
        bot.send_message(call.message.chat.id, "⚠️ Are you sure?", reply_markup=markup)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("del_"))
    def execute_delete_callback(call):
        if call.data == "del_no":
            bot.send_message(call.message.chat.id, "❌ Deleting canceled.")
        elif call.data.startswith("del_yes_"):
            note_id = int(call.data.split("_")[2])
            if json_manager.delete_note(note_id):
                bot.send_message(call.message.chat.id, "🗑 Note succesfully deleted.")
            else:
                bot.send_message(call.message.chat.id, "❌ Error when deleting.")
        bot.answer_callback_query(call.id)

   
    @bot.message_handler(func=lambda message: message.text == "✏️ Redact")
    def edit_note_start(message):
        notes = json_manager.load_notes()
        if not notes:
            bot.send_message(message.chat.id, "No notes to redact.")
            return
        
        bot.send_message(
            message.chat.id, 
            "✏️ Select a note to redact:", 
            reply_markup=menu.get_notes_inline_keyboard(notes, "edit_select")
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("edit_select_"))
    def edit_choice_callback(call):
        note_id = int(call.data.split("_")[2])
        
        markup = types.InlineKeyboardMarkup()
        btn_title = types.InlineKeyboardButton("📝 Change name", callback_data=f"field_title_{note_id}")
        btn_text = types.InlineKeyboardButton("📄 Change text", callback_data=f"field_text_{note_id}")
        markup.row(btn_title, btn_text)
        
        bot.send_message(call.message.chat.id, "What exactly do you want to change?", reply_markup=markup)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("field_"))
    def edit_field_callback(call):
        _, field, note_id = call.data.split("_")
        note_id = int(note_id)
        
        field_name = "name" if field == "title" else "text"
        msg = bot.send_message(call.message.chat.id, f"✍️ Enter a new **{field_name}** for note:", parse_mode="Markdown")
        
        bot.register_next_step_handler(msg, process_edit_value, note_id, field)
        bot.answer_callback_query(call.id)

    def process_edit_value(message, note_id, field):
        new_value = message.text
        if json_manager.edit_note(note_id, field, new_value):
            bot.send_message(message.chat.id, "✨ Note succesfully updated!")
        else:
            bot.send_message(message.chat.id, "❌ Something went wrong when updating.")
from keyboards.menu import main_menu


def register_help_handlers(bot):

    @bot.message_handler(commands=["help"])
    def help_command(message):
        text = (
            "ℹ️ Список команд:\n\n"
            "/start — starting bot\n"
            "/help — help\n\n"
            "📄 Looking at notes\n"
            "➕ Creating notes\n"
            "✏️ Redacting notes\n"
            "❌ Deleting notes"
        )

        bot.send_message(
            message.chat.id,
            text,
            reply_markup=main_menu()
        )

    @bot.message_handler(func=lambda m: m.text == "ℹ️ Помощь")
    def help_button(message):
        help_command(message)