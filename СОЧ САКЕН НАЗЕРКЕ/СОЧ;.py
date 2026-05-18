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