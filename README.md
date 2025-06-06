# Telegram-бот "Розклад занять"

Цей бот дозволяє студентам швидко отримати розклад занять своєї групи у Telegram.

## 🔧 Функціонал

- Вибір групи: ІПЗ або ФІН (через інлайн-кнопки)
- Команда `/today` — розклад на поточний день
- Команда `/tomorrow` — розклад на завтра
- Команда `/week` або кнопка **Тиждень** — розклад на весь тиждень
- Команда `/group` — зміна групи
- Команда `/menu` — меню з вибором дня тижня (через інлайн-кнопки)
- Постійна клавіатура з кнопками `Group` та `Menu` для швидкого доступу

## 🛠️ Технології

- Python 3.10+
- Бібліотека [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot)
- Формат зберігання розкладу: JSON

## 🗂 Структура проєкту

```
telegram_schedule_bot/
├── bot.py              # основний файл з логікою бота
├── schedule.json       # розклад занять для груп
├── users.json          # файл збереження вибору групи користувачем
├── README.md           # опис проєкту
└── requirements.txt    # залежності (створити командою `pip freeze > requirements.txt`)
```

## ▶️ Запуск бота

1. Встановіть бібліотеку:

   ```bash
   pip install python-telegram-bot
   ```

2. Вставте токен у `bot.py`:

   ```python
   TOKEN = "YOUR_BOT_TOKEN_HERE"
   ```

3. Запустіть файл:
   ```bash
   python bot.py
   ```

## 📌 Автор

- Карпенко Дмитро Олександрович
- Група: ІПЗ-22
- Звіт з технологічної практики  
- Тема: **"Розробка Telegram-бота для доступу до розкладу занять"**
