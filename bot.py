import json
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters

SCHEDULE_FILE = 'schedule.json'
USERS_FILE = 'users.json'

default_keyboard = ReplyKeyboardMarkup(
    [["Group", "Menu"]],
    resize_keyboard=True,
    one_time_keyboard=False
)

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_schedule_for_day(group, day_name):
    schedule_data = load_json(SCHEDULE_FILE)
    group_schedule = schedule_data.get(group, {})
    day_schedule = group_schedule.get(day_name, [])
    if not day_schedule:
        return f"На {day_name.lower()} занять немає.\n\nЩоб обрати інший день використовуйте команду /menu"
    
    response = f"📅 Розклад на {day_name} для групи {group}:\n"
    for i, item in enumerate(day_schedule, start=1):
        response += f"{i}. {item['час']} – {item['предмет']} (ауд. {item['аудиторія']})\n"
    response += "\nЩоб обрати інший день використовуйте команду /menu"
    return response

def get_today_day_name():
    days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П’ятниця", "Субота", "Неділя"]
    return days[datetime.datetime.now().weekday()]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Я бот для перегляду розкладу занять.\nОберіть групу за допомогою /group",
        reply_markup=default_keyboard
    )

async def group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ІПЗ", callback_data="group_ІПЗ")],
        [InlineKeyboardButton("ФІН", callback_data="group_ФІН")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Оберіть свою групу:", reply_markup=reply_markup)

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_json(USERS_FILE)
    user_id = str(update.effective_user.id)
    group = users.get(user_id)
    if not group:
        await update.message.reply_text("Спочатку оберіть групу: /group")
        return
    today_name = get_today_day_name()
    schedule_text = get_schedule_for_day(group, today_name)
    await update.message.reply_text(schedule_text, reply_markup=default_keyboard)

async def week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_json(USERS_FILE)
    user_id = str(update.effective_user.id)
    group = users.get(user_id)
    if not group:
        await update.message.reply_text("Спочатку оберіть групу: /group")
        return

    days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П’ятниця"]
    response = ""
    for day in days:
        
        base_text = get_schedule_for_day(group, day)
        cleaned_text = base_text.replace("\nЩоб обрати інший день використовуйте команду /menu", "")
        response += cleaned_text + "\n\n"
    
    await update.message.reply_text(response.strip() + "\nЩоб обрати інший день використовуйте команду /menu", reply_markup=default_keyboard)

async def show_day(update: Update, context: ContextTypes.DEFAULT_TYPE, day_name: str):
    users = load_json(USERS_FILE)
    user_id = str(update.effective_user.id)
    group = users.get(user_id)
    if not group:
        await update.message.reply_text("Спочатку оберіть групу: /group")
        return
    schedule_text = get_schedule_for_day(group, day_name)
    await update.message.reply_text(schedule_text, reply_markup=default_keyboard)

async def monday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_day(update, context, "Понеділок")

async def tuesday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_day(update, context, "Вівторок")

async def wednesday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_day(update, context, "Середа")

async def thursday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_day(update, context, "Четвер")

async def friday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_day(update, context, "П’ятниця")

async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = datetime.datetime.now().weekday()
    tomorrow = ["Понеділок", "Вівторок", "Середа", "Четвер", "П’ятниця", "Субота", "Неділя"][(index + 1) % 7]
    await show_day(update, context, tomorrow)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Понеділок", callback_data="day_Понеділок")],
        [InlineKeyboardButton("Вівторок", callback_data="day_Вівторок")],
        [InlineKeyboardButton("Середа", callback_data="day_Середа")],
        [InlineKeyboardButton("Четвер", callback_data="day_Четвер")],
        [InlineKeyboardButton("П’ятниця", callback_data="day_П’ятниця")],
        [InlineKeyboardButton("Сьогодні", callback_data="today"),
         InlineKeyboardButton("Завтра", callback_data="tomorrow")],
        [InlineKeyboardButton("Тиждень", callback_data="week")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Оберіть день:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = str(query.from_user.id)
    users = load_json(USERS_FILE)
    group = users.get(user_id)

    if data.startswith("group_"):
        group_name = data.split("_")[1]
        users[user_id] = group_name
        save_json(USERS_FILE, users)
        await query.edit_message_text(f"Групу {group_name} збережено! Для вибору дня використовуйте команду /menu")
        # await context.bot.send_message(chat_id=query.message.chat_id, text="", reply_markup=default_keyboard)

    elif data.startswith("day_"):
        if not group:
            await query.edit_message_text("Спочатку оберіть групу: /group")
            return
        day_name = data.split("_")[1]
        text = get_schedule_for_day(group, day_name)
        await query.edit_message_text(text)

    elif data == "today":
        if not group:
            await query.edit_message_text("Спочатку оберіть групу: /group")
            return
        day_name = get_today_day_name()
        text = get_schedule_for_day(group, day_name)
        await query.edit_message_text(text)

    elif data == "tomorrow":
        if not group:
            await query.edit_message_text("Спочатку оберіть групу: /group")
            return
        index = datetime.datetime.now().weekday()
        tomorrow = ["Понеділок", "Вівторок", "Середа", "Четвер", "П’ятниця", "Субота", "Неділя"][(index + 1) % 7]
        text = get_schedule_for_day(group, tomorrow)
        await query.edit_message_text(text)

    elif data == "week":
        if not group:
            await query.edit_message_text("Спочатку оберіть групу: /group")
            return
        days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П’ятниця"]
        response = ""
        for day in days:
            
            base_text = get_schedule_for_day(group, day)
            cleaned_text = base_text.replace("\n\nЩоб обрати інший день використовуйте команду /menu", "")
            response += cleaned_text + "\n\n"
    
        await query.edit_message_text(response.strip() + "\n\nЩоб обрати інший день використовуйте команду /menu")

async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    if text == "group":
        await group(update, context)
    elif text == "menu":
        await menu(update, context)
    else:
        await update.message.reply_text("Використовуйте доступні команди або /menu", reply_markup=default_keyboard)

def main():
    TOKEN = "8147195909:AAFvv5yPzy7KfuWPjV1vjFEIxzqM0UImXPM"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("group", group))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("tomorrow", tomorrow))
    app.add_handler(CommandHandler("week", week))
    app.add_handler(CommandHandler("monday", monday))
    app.add_handler(CommandHandler("tuesday", tuesday))
    app.add_handler(CommandHandler("wednesday", wednesday))
    app.add_handler(CommandHandler("thursday", thursday))
    app.add_handler(CommandHandler("friday", friday))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply_handler))

    print("Бот запущено...")
    app.run_polling()

if __name__ == '__main__':
    main()
