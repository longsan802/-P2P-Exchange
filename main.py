import os
import asyncio
import ssl
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, ConversationHandler, filters
)
from telegram.error import TelegramError
from config import (
    BOT_TOKEN, ADMIN_IDS, USDT_WALLET, 
    EXCHANGE_RATE, FEE_PERCENTAGE, LANGUAGES,
    WEBHOOK_ENABLED, WEBHOOK_URL, WEBHOOK_SECRET,
    WEBHOOK_HOST, WEBHOOK_PORT, SSL_CERT_PATH, SSL_PRIVKEY_PATH
)
from database import db
from translations import get_text
from datetime import datetime

# Conversation states
LANGUAGE, AMOUNT, TXID, SCREENSHOT, BANK, ACCOUNT_NUMBER, ACCOUNT_NAME, CONFIRM = range(8)

# Screenshot directory
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Store user data temporarily
user_data_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.message.from_user
    db.add_user(user.id, user.username)
    
    lang = db.get_user_language(user.id)
    reply_text = get_text('start', lang, wallet=USDT_WALLET)
    
    # Language selection keyboard
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
         InlineKeyboardButton("🇰🇭 ភាសាខ្មែរ", callback_data='lang_km')],
        [InlineKeyboardButton("🇨🇳 中文", callback_data='lang_zh')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(reply_text, reply_markup=reply_markup)
    return LANGUAGE

async def language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language selection"""
    query = update.callback_query
    await query.answer()
    
    lang = query.data.split('_')[1]
    user = query.from_user
    db.set_user_language(user.id, lang)
    
    welcome_text = get_text('start', lang, wallet=USDT_WALLET)
    await query.edit_message_text(welcome_text)
    
    # Show next steps with buttons
    keyboard = [
        [InlineKeyboardButton(get_text('btn_exchange', lang), callback_data='action_exchange')],
        [InlineKeyboardButton(get_text('btn_check_rate', lang), callback_data='action_rate')],
        [InlineKeyboardButton(get_text('btn_help', lang), callback_data='action_help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        get_text('next_steps', lang),
        reply_markup=reply_markup
    )
    
    return ConversationHandler.END


async def handle_next_steps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle next steps button clicks"""
    query = update.callback_query
    await query.answer()
    
    action = query.data
    user = query.from_user
    lang = db.get_user_language(user.id)
    
    if action == 'action_exchange':
        # Start exchange process
        await new_order(update, context)
    elif action == 'action_rate':
        # Show exchange rate
        rate = db.get_current_rate()
        fee = FEE_PERCENTAGE
        rate_text = get_text('rate', lang, rate=rate, fee=fee)
        await query.message.reply_text(rate_text)
        # Show next steps again
        keyboard = [
            [InlineKeyboardButton(get_text('btn_exchange', lang), callback_data='action_exchange')],
            [InlineKeyboardButton(get_text('btn_check_rate', lang), callback_data='action_rate')],
            [InlineKeyboardButton(get_text('btn_help', lang), callback_data='action_help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            get_text('next_steps', lang),
            reply_markup=reply_markup
        )
    elif action == 'action_help':
        # Show help
        help_text = get_text('help', lang, wallet=USDT_WALLET)
        await query.message.reply_text(help_text)
        # Show next steps again
        keyboard = [
            [InlineKeyboardButton(get_text('btn_exchange', lang), callback_data='action_exchange')],
            [InlineKeyboardButton(get_text('btn_check_rate', lang), callback_data='action_rate')],
            [InlineKeyboardButton(get_text('btn_help', lang), callback_data='action_help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            get_text('next_steps', lang),
            reply_markup=reply_markup
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    user = update.message.from_user
    lang = db.get_user_language(user.id)
    help_text = get_text('help', lang, wallet=USDT_WALLET)
    await update.message.reply_text(help_text)

async def rate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /rate command"""
    user = update.message.from_user
    lang = db.get_user_language(user.id)
    rate = db.get_current_rate()
    fee = FEE_PERCENTAGE
    
    rate_text = get_text('rate', lang, rate=rate, fee=fee)
    await update.message.reply_text(rate_text)

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    user = update.message.from_user
    lang = db.get_user_language(user.id)
    orders = db.get_user_orders(user.id)
    
    if not orders:
        await update.message.reply_text(get_text('order_not_found', lang))
        return
    
    for order in orders[:5]:  # Show last 5 orders
        status_key = f"status_{order[9]}"  # status is at index 9
        status_text = get_text(status_key, lang, order_id=order[0])
        await update.message.reply_text(status_text)

async def new_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start new order process"""
    user = update.message.from_user
    lang = db.get_user_language(user.id)
    
    # Initialize user data
    user_data_store[user.id] = {}
    
    await update.message.reply_text(get_text('enter_amount', lang))
    return AMOUNT

async def process_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process USDT amount input"""
    user = update.message.from_user
    lang = db.get_user_language(user.id)
    
    try:
        amount = float(update.message.text)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        user_data_store[user.id]['amount_usdt'] = amount
        user_data_store[user.id]['amount_khr'] = amount * db.get_current_rate()
        
        await update.message.reply_text(get_text('enter_txid', lang))
        return TXID
    except ValueError:
        await update.message.reply_text(get_text('invalid_amount', lang))
        return AMOUNT

async def process_txid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process transaction ID input"""
    user = update.message.from_user
    lang = db.get_user_language(user.id)
    
    txid = update.message.text.strip()
    user_data_store[user.id]['txid'] = txid
    
    await update.message.reply_text(get_text('upload_screenshot', lang))
    return SCREENSHOT

async def process_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process screenshot upload or skip"""
    user = update.message.from_user
    lang = db.get_user_language(user.id)
    
    # Handle /skip command
    if update.message.text and update.message.text.lower() == '/skip':
        user_data_store[user.id]['screenshot_path'] = None
        await update.message.reply_text(get_text('skip_screenshot', lang))
        await update.message.reply_text(get_text('enter_bank', lang))
        return BANK
    
    # Handle photo upload
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{user.id}_{timestamp}.jpg"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        await file.download_to_drive(filepath)
        user_data_store[user.id]['screenshot_path'] = filepath
        
        await update.message.reply_text(get_text('skip_screenshot', lang))
        await update.message.reply_text(get_text('enter_bank', lang))
        return BANK
    
    await update.message.reply_text(get_text('upload_screenshot', lang))
    return SCREENSHOT

async def process_bank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process bank name input"""
    user = update.message.from_user
    lang = db.get_user_language(user.id)
    
    user_data_store[user.id]['bank_name'] = update.message.text.strip()
    await update.message.reply_text(get_text('enter_account_number', lang))
    return ACCOUNT_NUMBER

async def process_account_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process account number input"""
    user = update.message.from_user
    lang = db.get_user_language(user.id)
    
    user_data_store[user.id]['account_number'] = update.message.text.strip()
    await update.message.reply_text(get_text('enter_account_name', lang))
    return ACCOUNT_NAME

async def process_account_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process account name input"""
    user = update.message.from_user
    lang = db.get_user_language(user.id)
    
    user_data_store[user.id]['account_name'] = update.message.text.strip()
    
    # Calculate fees and totals
    amount_usdt = user_data_store[user.id]['amount_usdt']
    fee_amount = amount_usdt * (FEE_PERCENTAGE / 100)
    received_khr = (amount_usdt - fee_amount) * db.get_current_rate()
    
    # Show confirmation
    confirm_text = get_text('order_confirm', lang,
        amount=amount_usdt,
        rate=db.get_current_rate(),
        fee=FEE_PERCENTAGE,
        fee_amount=fee_amount,
        received=received_khr,
        bank=user_data_store[user.id]['bank_name'],
        account=user_data_store[user.id]['account_number'],
        name=user_data_store[user.id]['account_name']
    )
    
    await update.message.reply_text(confirm_text)
    return CONFIRM

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm and submit order"""
    user = update.message.from_user
    lang = db.get_user_language(user.id)
    data = user_data_store.get(user.id, {})
    
    # Create order in database
    order_id = db.create_order(
        user_id=user.id,
        tx_hash=data.get('txid', ''),
        amount_usdt=data['amount_usdt'],
        amount_khr=data['amount_usdt'] * db.get_current_rate() - (data['amount_usdt'] * (FEE_PERCENTAGE / 100) * db.get_current_rate()),
        bank_name=data['bank_name'],
        account_number=data['account_number'],
        account_name=data['account_name'],
        screenshot_path=data.get('screenshot_path')
    )
    
    # Notify user
    await update.message.reply_text(get_text('order_submitted', lang, order_id=order_id))
    
    # Notify admin
    fee_amount = data['amount_usdt'] * (FEE_PERCENTAGE / 100)
    received_khr = (data['amount_usdt'] - fee_amount) * db.get_current_rate()
    
    tx_info = f"TxID: `{data.get('txid', 'N/A')}`"
    if data.get('screenshot_path'):
        tx_info += f"\n📎 Screenshot attached"
    
    for admin_id in ADMIN_IDS:
        try:
            admin_text = get_text('admin_new_order', 'en',
                order_id=order_id,
                username=user.username or "Unknown",
                user_id=user.id,
                amount=data['amount_usdt'],
                received=received_khr,
                bank=data['bank_name'],
                account=data['account_number'],
                tx_info=tx_info
            )
            
            keyboard = [
                [InlineKeyboardButton(get_text('admin_approve', 'en'), 
                                     callback_data=f"approve_{order_id}"),
                 InlineKeyboardButton(get_text('admin_reject', 'en'), 
                                     callback_data=f"reject_{order_id}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if data.get('screenshot_path'):
                with open(data['screenshot_path'], 'rb') as photo:
                    await context.bot.send_photo(
                        admin_id, photo, 
                        caption=admin_text, 
                        reply_markup=reply_markup,
                        parse_mode='Markdown'
                    )
            else:
                await context.bot.send_message(
                    admin_id, admin_text, 
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        except TelegramError as e:
            print(f"Failed to notify admin {admin_id}: {e}")
    
    # Clean up user data
    user_data_store.pop(user.id, None)
    
    return ConversationHandler.END

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel order process"""
    user = update.message.from_user
    user_data_store.pop(user.id, None)
    
    lang = db.get_user_language(user.id)
    await update.message.reply_text(get_text('cancel', lang))
    
    return ConversationHandler.END

async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin approve/reject callbacks"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    if user.id not in ADMIN_IDS:
        await query.edit_message_text(get_text('not_admin', 'en'))
        return
    
    action, order_id = query.data.split('_')
    order_id = int(order_id)
    order = db.get_order(order_id)
    
    if not order:
        await query.edit_message_text(get_text('order_not_found', 'en'))
        return
    
    # Update order status
    new_status = 'approved' if action == 'approve' else 'rejected'
    db.update_order_status(order_id, new_status)
    
    # Notify user
    user_lang = db.get_user_language(order[1])  # user_id is at index 1
    user_id = order[1]
    
    if action == 'approve':
        await context.bot.send_message(
            user_id, 
            get_text('order_approved_user', user_lang, order_id=order_id)
        )
    else:
        # For rejection, we could add a reason parameter
        await context.bot.send_message(
            user_id, 
            get_text('order_rejected_user', user_lang, order_id=order_id, reason="Contact admin")
        )
    
    # Update admin message
    status_text = f"✅ Order #{order_id} {new_status.upper()}"
    await query.edit_message_text(status_text)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    print(f"Error: {context.error}")

def main():
    """Main function to run the bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Conversation handler for order process
    order_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, new_order)],
        states={
            LANGUAGE: [
                CallbackQueryHandler(language_selection, pattern='^lang_')
            ],
            AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_amount)
            ],
            TXID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_txid)
            ],
            SCREENSHOT: [
                MessageHandler(filters.PHOTO | filters.TEXT, process_screenshot),
                CommandHandler('skip', process_screenshot)
            ],
            BANK: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_bank)
            ],
            ACCOUNT_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_account_number)
            ],
            ACCOUNT_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_account_name)
            ],
            CONFIRM: [
                CommandHandler('confirm', confirm_order),
                CommandHandler('cancel', cancel_order)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel_order)]
    )
    
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('rate', rate_command))
    application.add_handler(CommandHandler('status', status_command))
    application.add_handler(order_conv)
    application.add_handler(CallbackQueryHandler(handle_admin_callback, pattern='^(approve|reject)_'))
    application.add_handler(CallbackQueryHandler(handle_next_steps, pattern='^action_'))
    application.add_error_handler(error_handler)
    
    if WEBHOOK_ENABLED:
        # Webhook mode
        print(f"Starting bot in WEBHOOK mode...")
        print(f"Webhook URL: {WEBHOOK_URL}")
        
        # Build SSL context
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        
        # Check if SSL certificates exist
        if os.path.exists(SSL_CERT_PATH) and os.path.exists(SSL_PRIVKEY_PATH):
            ssl_context.load_cert_chain(
                certfile=SSL_CERT_PATH,
                keyfile=SSL_PRIVKEY_PATH
            )
            print("Loaded SSL certificate from configured paths")
        else:
            # For Render: use HTTP (no SSL) since Render handles SSL termination
            # Or generate self-signed for local testing
            if WEBHOOK_URL.startswith("https://"):
                print("SSL certificates not found. Assuming Render SSL termination (HTTP mode)")
                ssl_context = None
            else:
                # Generate self-signed certificate for testing
                import subprocess
                print("Generating self-signed SSL certificate...")
                subprocess.run([
                    'openssl', 'req', '-x509', '-newkey', 'rsa:2048',
                    '-keyout', SSL_PRIVKEY_PATH, '-out', SSL_CERT_PATH,
                    '-days', '365', '-nodes',
                    '-subj', '/CN=localhost'
                ], check=True, capture_output=True)
                ssl_context.load_cert_chain(
                    certfile=SSL_CERT_PATH,
                    keyfile=SSL_PRIVKEY_PATH
                )
                print("Self-signed SSL certificate generated")
        
        # Set webhook
        if ssl_context:
            application.run_webhook(
                listen=WEBHOOK_HOST,
                port=WEBHOOK_PORT,
                secret_token=WEBHOOK_SECRET,
                webhook_url=WEBHOOK_URL,
                ssl_context=ssl_context,
                drop_pending_updates=True
            )
        else:
            # For Render: run without SSL (Render handles it)
            application.run_webhook(
                listen=WEBHOOK_HOST,
                port=WEBHOOK_PORT,
                secret_token=WEBHOOK_SECRET,
                webhook_url=WEBHOOK_URL,
                drop_pending_updates=True
            )
    else:
        # Polling mode (default)
        print("Starting bot in POLLING mode...")
        application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
