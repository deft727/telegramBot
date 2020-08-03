import config
import logging
import asyncio
from datetime import datetime
from aiogram import Bot,Dispatcher,executor,types
from sqliter import SQLiter
from pars import StopGame
logging.basicConfig(level=logging.INFO)

bot=Bot(token=config.API_TOKEN)
dp=Dispatcher(bot)

db = SQLiter('db.db')
sg=StopGame('lastkey.txt')

@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, 1)

	await message.answer("Вы успешно подписались на рассылку!")

@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber(message.from_user.id, 0)
		await message.answer("Вы итак не подписаны.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, 0)
		
		await message.answer("Вы успешно отписаны от рассылки.")

async def scheduled(wait_for):

	while True:

		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_games = sg.new_games()

		if(new_games):
			# если игры есть, переворачиваем список и итерируем
			# new_games.reverse()
			for ng in new_games:
				nfo = sg.game_info(ng)

				# получаем список подписчиков бота
				subscriptions = db.get_subscriptions()

				# отправляем всем новость
				for s in subscriptions:
					with open(sg.download_image(nfo['image']), 'rb') as photo:
						await bot.send_photo(
							s[1],
							photo,
							caption = nfo['title'] + "\n"  + nfo['excerpt'] + "\n" + nfo['price']+ "\n" +nfo['opisanie']+  "\n\n" + nfo['link'],
							disable_notification = True
						)

				
				# обновляем ключ
				sg.update_lastkey(nfo['id'])

# запускаем лонг поллинг
if __name__ == '__main__':
	dp.loop.create_task(scheduled(10)) 
	executor.start_polling(dp, skip_updates=True)