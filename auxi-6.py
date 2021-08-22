import telebot
from telebot import types
import time

#токен бота + канал
bot = telebot.TeleBot("1772121119:AAF_1WwuykNuA7RQvtNUJJ50wIIYII21v28")
channel = "@plain_law"

#Приветственное письмо с просьбой подписаться + кнопка проверки подписки
@bot.message_handler(commands=['start'])
def start_message(message):

	bot.send_message(message.chat.id, "Привет! Меня зовут Окси. Я помогу тебе сформулировать твой вопрос, а затем передам его юристам!")

	time.sleep (1.5)

	#Создаем кнопку для проверки подписки 

	check = types.InlineKeyboardMarkup()
	check.add(types.InlineKeyboardButton(text="Проверить подписку", callback_data = "Проверить подписку"))

	#Отправляем сообщение с подпиской

	bot.send_message(message.chat.id, text = "Перед тем как начать, подпишись на канал наших хороших друзей - t.me/plain_law!\
	Именно благодаря их помощи наш проект может существовать и развиваться!", reply_markup=check)

# Проверка подписки 
@bot.callback_query_handler(func=lambda call: True)
def callback_check(call):
	if call.data == "Проверить подписку":
		bot.answer_callback_query(call.id)
		status = ['creator', 'administrator', 'member']
		if bot.get_chat_member(channel, call.from_user.id).status in status:
			bot.send_message(call.message.chat.id, "Спасибо за подписку!")
			short_descripton (call.message)
		else:
			bot.send_message(call.message.chat.id, "Проверь еще раз наличие подписки...")

	if call.data == "Отменить": 
		bot.answer_callback_query(call.id)
		bot.send_message (call.message.chat.id, "Нажмите /start, чтобы начать заново!")

	if call.data == "Отправить":
		bot.answer_callback_query(call.id)
		conclusion (call.message)

	if call.data == "Ответить":
		bot.answer_callback_query(call.id)
		f = call.message.text.split("\n")[0]
		questioning(call.message, f)

def short_descripton (message):
	bot.send_message(message.chat.id, "Приступим к твоему вопросу! Для начала опиши вопрос в одном предложении.\
	Старайся писать максимально кратко и четко. Например, если тебе отказываются возвращать деньги за телефон\
	в магазине – пиши «Магазин отказывается возвращать купленный телефон».")
	bot.register_next_step_handler(message, full_description)

def full_description (message):
	sd = message.text + "\n"
	bot.send_message(message.chat.id, "Теперь добавь полное изложение вопроса.\
	Постарайся максимально детально описать свою проблему. При изложении удели особое внимание фактам.\
	Такими фактами могут быть, например, время, место или особенности обстоятельств. В конфликтных ситуациях\
	постарайся указать все стороны конфликта, их действия.")
	bot.register_next_step_handler(message, documents_ask, sd)

def documents_ask (message, sd):
	fd = message.text + "\n"
	bot.send_message(message.chat.id, "Укажи, имеются ли какие-нибудь документы, которые могут подтвердить или опровергнуть твою историю?\
	Если таких документов нет – пиши «документы отсутствуют».")
	bot.register_next_step_handler(message, result, sd, fd)

def result (message, sd, fd):
	docs = message.text + "\n"
	bot.send_message(message.chat.id, "В конце, опиши результат которого ты хотел бы достичь?\
	Например, вернуть деньги.")
	bot.register_next_step_handler(message, check, sd, fd, docs)

def check (message, sd, fd, docs):
	res = message.text + "\n"
	check = types.InlineKeyboardMarkup()
	check.add(types.InlineKeyboardButton(text = "Отправить", callback_data = "Отправить"))
	check.add(types.InlineKeyboardButton(text="Отменить", callback_data = "Отменить"))

	bot.send_message (message.chat.id, text = "*Краткое описание: \n*" + sd + "*Полное описание: \n*" +
		fd + "*Наличие документов: \n*" + docs + "*Желаемый результат: \n*" + res, parse_mode="Markdown", reply_markup = check)
	bot.send_message(message.chat.id, "Проверьте указанные данные. Если все хорошо, напишите 'Отправить'. Если нет - нажмите /start и начните заново.")

def conclusion (message):

	text = message.text.split("\n")
	raw_case = []

	titles = ["Краткое описание: ", "Полное описание: ", "Наличие документов: ", "Желаемый результат: "]
	btitles = []
	for title in titles:
		btitle = "*" + title + "*"
		btitles.append(btitle)

	for index, elem in enumerate(text):
		if elem in titles:
			text[index] = btitles [0]
			btitles.pop(0)

	for i in text: 
		new_text = i + '\n'
		raw_case.append (new_text)

	case = ''.join(raw_case)

	answer = types.InlineKeyboardMarkup()
	answer.add(types.InlineKeyboardButton(text = "Ответить", callback_data = "Ответить"))

	bot.send_message (-1001376884558, text = str(message.chat.id) + "\n" + "\n" + case, parse_mode="Markdown", reply_markup = answer)
	bot.send_message(-1001376884558, text = "Чтобы ответить, нажмите кнопку.")
	bot.send_message(message.chat.id, "Отличная работа. Наша команда скоро приступит к рассмотрению твоей ситуации!\
	Для того, чтобы добавить новое обращение - нажми /start")

def questioning (message, f):
	client = f
	bot.send_message (-1001376884558, "Введите ответ:")
	bot.register_next_step_handler (message, answering, client)

def answering (message, client): 
	bot.send_message (client, text = "*Ответ на ваше обращение:\n\n*" + message.text, parse_mode="Markdown")
	bot.send_message(-1001376884558, text = "Ваш ответ отправлен!")

bot.polling()
