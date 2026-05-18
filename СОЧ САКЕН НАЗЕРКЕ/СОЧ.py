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