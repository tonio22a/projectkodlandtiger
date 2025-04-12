from logic import detect_tiger
from PIL import Image
import telebot 

bot = telebot.TeleBot(TOKEN)

# Обработчики команд
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Добрый день! Я бот для определения видов тигров по фото.")

# Обработчик фотографий
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Сохранение фото
        file_info = bot.get_file(message.photo[-1].file_id)
        file_name = file_info.file_path.split('/')[-1]
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Анализ изображения
        image = Image.open(file_name)
        result, score = detect_tiger(image)
        result = result[2:]

        # Отправка результата
        response = f"{result}\nТочность: {score:.2f}"
        bot.reply_to(message, response)
        if {score} < 99:
            bot.send_message(message.chat.id, 'Извините, я не уверен, что это на картинке.')    
        # Дополнительная классификация
        if result.startswith('Амурский'):
            bot.send_message(message.chat.id, '✅ Это Амурский тигр!')
        elif result.startswith('Бенгальский'):
            bot.send_message(message.chat.id, '✅ Это Бенгальский тигр!')
        elif result.startswith('Индокитайский'):
            bot.send_message(message.chat.id, '✅ Это Индокитайский тигр!')
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "Отправьте мне фото тигра для анализа")

if __name__ == "__main__":
    bot.infinity_polling()
