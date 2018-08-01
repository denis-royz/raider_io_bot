import asyncio
import logging
import configuration.config as config

from urllib.parse import urlparse
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling
from service.user_service import UserService
from service.raider_io_api_service import RaiderIoService


API_TOKEN = config.get('api-token')

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
bot = Bot(token=API_TOKEN, loop=loop)
dp = Dispatcher(bot)
userService = UserService()
raiderIoService = RaiderIoService()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    logging.info('send_welcome')
    await message.reply("Hi!\nI'm Raider IO bot!.")


@dp.message_handler(regexp='^https://raider.io/characters/')
async def subscribe(message: types.Message):
    user_id = message.from_user.id
    user = userService.authorize_or_create(telegram_id=user_id)
    params = urlparse(message.text).path.split('/')
    region = params[2]
    realm = params[3]
    character_name = params[4]

    userService.subscribe(user, region, realm, character_name)

    await bot.send_message(message.chat.id, 'Subscribe. {region}:{character_name}-{realm}'
                           .format(region=region, character_name=character_name, realm=realm))


@dp.message_handler(commands=['update'])
async def update(message: types.Message):
    user_id = message.from_user.id
    user = userService.authorize_or_create(telegram_id=user_id)
    subscriptions = userService.get_subscriptions(user)
    raiderIoService.update(subscriptions)
    await bot.send_message(message.chat.id, 'Subscriptions update scheduled. (Only eu-Gordunni server is supported)')


@dp.message_handler(commands=['affix'])
async def update(message: types.Message):
    user_id = message.from_user.id
    userService.authorize_or_create(telegram_id=user_id)
    result = raiderIoService.get_mythic_affixes()
    template = 'Weekly Mythic Plus Affixes: {affix_1}, {affix_2}, {affix_3}%s' \
               '\n(+4) {affix_1}\n{affix_1_desc}' \
               '\n(+7) {affix_2}\n{affix_2_desc}' \
               '\n(+10) {affix_3}\n{affix_3_desc}' \
               '\nPowered by Raider.IO - Raid & Mythic Plus Rankings'
    response_text = template.format(affix_1=result['affix_details'][0]['name'],
                                    affix_2=result['affix_details'][1]['name'],
                                    affix_3=result['affix_details'][2]['name'],
                                    affix_1_desc=result['affix_details'][0]['description'],
                                    affix_2_desc=result['affix_details'][1]['description'],
                                    affix_3_desc=result['affix_details'][2]['description'])
    await bot.send_message(message.chat.id, response_text)


@dp.message_handler(commands=['subscriptions', 'sub'])
async def get_subscriptions(message: types.Message):
    user_id = message.from_user.id
    user = userService.authorize_or_create(telegram_id=user_id)
    subscriptions = userService.get_subscriptions(user)
    response_text = 'You have {0} subscriptions'.format(len(subscriptions))
    for sub in subscriptions:
        response_text += '\n  Subscribed for {0}-{1}'.format(sub['character_name'], sub['realm'])
    await bot.send_message(message.chat.id, response_text)


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, 'I am sorry. Can not handle this message')


if __name__ == '__main__':
    start_polling(dp, loop=loop, skip_updates=True)
