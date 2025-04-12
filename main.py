from logic import detect_tiger
from PIL import Image
import telebot 
import random
from config import Token

bot = telebot.TeleBot(Token)

AMUR_FACTS = [
    'Это самый крупный подвид тигра - длина тела до 3.8 метров!',
    'Единственный тигр, освоивший жизнь в снегах ❄️',
    'В природе осталось всего около 600 особей',
    'Может развивать скорость до 50 км/ч',
    'Рисунок полос уникален, как отпечатки пальцев у человека'
]

BENGAL_FACTS = [
    'Национальное животное Индии и Бангладеш',
    'Белые тигры - генетическая мутация этого вида',
    'Умеют прекрасно плавать и нырять 🏊',
    'Самцы защищают территорию до 100 км²',
    'Изображен на древнеиндийских монетах 1 века н.э.'
]

INDOCHINESE_FACTS = [
    'Самый загадочный и малоизученный подвид',
    'Имеет более темный окрас и узкие полосы',
    'Обожает купаться в водоемах днем 💦',
    'Основная угроза - браконьерство для медицины',
    'В дикой природе осталось менее 250 особей'
]

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Добрый день! Я бот для определения видов тигров по фото.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        file_name = file_info.file_path.split('/')[-1]
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        image = Image.open(file_name)
        result, score = detect_tiger(image)
        result = result[2:]

        if score <= 1:
            score *= 100

        response = f"{result}\nТочность: {score:.2f}%"
        bot.reply_to(message, response)

        if score < 53:
            bot.send_message(message.chat.id, "Извините, я не уверен, что именно этот вид на данной картинке.")
        else:
            if result.startswith('Амурский'):
                fact = random.choice(AMUR_FACTS)
                bot.send_message(message.chat.id, f'✅ Это Амурский тигр!\n\n🐅 Интересный факт: {fact}')
            
            elif result.startswith('Бенгальский'):
                fact = random.choice(BENGAL_FACTS)
                bot.send_message(message.chat.id, f'✅ Это Бенгальский тигр!\n\n🔥 Интересный факт: {fact}')
            
            elif result.startswith('Индокитайский'):
                fact = random.choice(INDOCHINESE_FACTS)
                bot.send_message(message.chat.id, f'✅ Это Индокитайский тигр!\n\n🌴 Интересный факт: {fact}')

    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, "Отправьте мне фото тигра для анализа")

if __name__ == "__main__":
    bot.infinity_polling()