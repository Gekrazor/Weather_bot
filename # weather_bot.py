# weather bot
import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config


bot = telebot.TeleBot("your token")

# main part of code with commands
@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('images/umbrella.webp', 'rb')
	bot.send_sticker(message.chat.id, sti)
	bot.send_message(message.chat.id, f'Greetings, {str(message.from_user.first_name)}!\n/start - run the bot\n/help - bot commands\n/credits - bot`s author\nType name of the city to know weather')

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id, '/start - run the bot\n/help - bot commands\n/credits - bot`s author\nType name of the city to know weather')

@bot.message_handler(commands=['credits'])
def help(message):
	bot.send_message(message.chat.id, '======== \nGekrazor \n========')

@bot.message_handler(content_types=['text'])
def test(message):
	try:
		place = message.text

		config_dict = get_default_config()
		config_dict['language'] = 'en'

		owm = OWM('your token', config_dict)
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(place)
		w = observation.weather

		t = w.temperature("celsius")
		t1 = t['temp']
		t2 = t['feels_like']
		t3 = t['temp_max']
		t4 = t['temp_min']

		wi = w.wind()['speed']
		humi = w.humidity
		cl = w.clouds
		st = w.status
		dt = w.detailed_status
		ti = w.reference_time('iso')
		pr = w.pressure['press']
		vd = w.visibility_distance
		
		# main text
		bot.send_message(message.chat.id, "In " + str(place) + " city" + " temperature " + str(t1) + " °C" + "\n" + 
				"Maximum temperature " + str(t3) + " °C " +"\n" + 
				"Minimal temperature " + str(t4) + " °C " + "\n" + 
				"Feels like " + str(t2) + " °C " + "\n" +
				"Wind speed " + str(wi) + " m/s " + "\n" + 
				"Atmosphere pressure " + str(pr) + " mm.merc.col. " + "\n" + 
				"Humidity " + str(humi) + " %" + "\n" + 
				"Eye range " + str(vd) + "  metrs" + "\n" +
				"Additional info " + str(st) + "\n" + str(dt))

		# stickers depends on status
		if st == 'Clouds':
			sti_clouds = open('images/Clouds.tgs', 'rb')
			bot.send_sticker(message.chat.id, sti_clouds)
		elif st == 'Clear' and t1 >= 25:
			sti_hotsun = open('images/hotsun.tgs', 'rb')
			bot.send_sticker(message.chat.id, sti_hotsun)
		elif st == 'Clear':
			sti_sun = open('images/sun.tgs', 'rb')
			bot.send_sticker(message.chat.id, sti_sun)
		elif st == 'Rain':
			sti_rain = open('images/Rain.tgs', 'rb')
			bot.send_sticker(message.chat.id, sti_rain)
		elif st == 'Fog':
			sti_fog = open('images/fog.tgs', 'rb')
			bot.send_sticker(message.chat.id, sti_fog)
		
		# weather advice
		if t1 <= 10:
			bot.send_message(message.chat.id, "\nWatch out! It's cold outside, wear warmly.")
		elif 10 < t1 <= 15:
			bot.send_message(message.chat.id, "\nCool outside, take a coat.")
		elif 15 < t1 <= 20:
			bot.send_message(message.chat.id, "\nQuite warm, but better to wear a light jacket.")
		elif 15 < t1 <= 20 and st == 'Rain':
			bot.send_message(message.chat.id, "\nQuite warm and rainy. Better to wear a light jacket, don`t forget about umbrella!")
		elif 20 < t1 <= 25 and st == 'Clear':
			bot.send_message(message.chat.id, "\nAmazing weather, enjoy it!")
		elif 20 < t1 <= 25 and st == 'Clouds':
			bot.send_message(message.chat.id, "\nGood weather, but cloudy.")
		elif 25 < t1:
			bot.send_message(message.chat.id, "\nLooks like summer! Hot!")



	except:
		sti_help = open('images/help.webp', 'rb')
		bot.send_sticker(message.chat.id, sti_help)
		bot.send_message(message.chat.id,"No way to find city with that name!")



bot.polling(none_stop=True, interval=0)
