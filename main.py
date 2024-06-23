import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random
import string

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dictionary to store redeem codes and their prizes
redeem_codes = {}

# Generate a redeem code
def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Use /create_code <prize> to create a redeem code.')

# Create redeem code command handler
def create_code(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text('Usage: /create_code <prize>')
        return
    
    prize = context.args[0]
    code = generate_code()
    redeem_codes[code] = prize
    update.message.reply_text(f'Redeem code created: {code}')

# Redeem code command handler
def redeem(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text('Usage: /redeem <code>')
        return
    
    code = context.args[0]
    if code in redeem_codes:
        prize = redeem_codes.pop(code)
        update.message.reply_text(f'Congratulations! You have claimed: {prize}')
    else:
        update.message.reply_text('Invalid or already claimed code.')

def main() -> None:
    # Telegram bot token
    TOKEN = '7108764954:AAFbBqX-vGNsXkfz6Q20-3RPUFWccGA9Xkc'

    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("create_code", create_code))
    dispatcher.add_handler(CommandHandler("redeem", redeem))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
