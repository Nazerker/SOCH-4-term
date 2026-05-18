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