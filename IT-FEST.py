# Нужные импорты, импорт базы данных и парсера.
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from database import DataBase
from tokens import TG_TOKEN
from vkparser import VkParser
import aiocron

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)
db = DataBase('IT-FEST DataBase.sqlite')
parser = VkParser()
parser.get_last_id_posts()


# Словарь для реализации кнопок.
events_dict = {'TechnoCom': 1,
               'IT-fest_2022': 2,
               'IASF2022': 3,
               'ФестивальОКК': 4,
               'Нейрофест': 5,
               'НевидимыйМир': 6,
               'КонкурсНИР': 7,
               'VRARFest3D': 8
               }


# Словарь для получения списка подписанных пользователей и получения постов.
events_dict_reverse = {1: 'TechnoCom',
                       2: 'IT-fest_2022',
                       3: 'IASF2022',
                       4: 'ФестивальОКК',
                       5: 'Нейрофест',
                       6: 'НевидимыйМир',
                       7: 'КонкурсНИР',
                       8: 'VRARFest3D'
                       }


# Словарь для проверки хештега в посте.
events_dict_tags = {1: '#TechnoCom',
                    2: '#ITfest_2022',
                    3: '#IASF2022',
                    4: '#ФестивальОКК',
                    5: '#Нейрофест',
                    6: '#НевидимыйМир',
                    7: '#КонкурсНИР',
                    8: '#VRARFest3D'
                    }


# Словарь для отправки ссылки на пост.
events_posts_urls = {1: 'https://vk.com/technocom2022?w=wall-210998761_',
                     2: 'https://vk.com/itfest2022?w=wall-210985709_',
                     3: 'https://vk.com/aerospaceproject?w=wall-196557207_',
                     4: 'https://vk.com/okk_fest?w=wall-211638918_',
                     5: 'https://vk.com/neurofest2022?w=wall-211803420_',
                     6: 'https://vk.com/nauchim.online?w=wall-200248443_',
                     7: 'https://vk.com/nauchim.online?w=wall-200248443_',
                     8: 'https://vk.com/nauchim.online?w=wall-200248443_'}

# Кнопки отписки/подписки мероприятий.
buttons_inline = InlineKeyboardMarkup(row_width=4)
button_subscribe_all = InlineKeyboardButton(text='Подписаться на все',
                                            callback_data='button_subscribe')
button_unsubscribe_all = InlineKeyboardButton(text='Отписаться от всего',
                                              callback_data='button_unsubscribe')
button_TechnoCom = InlineKeyboardButton(text='TechnoCom', callback_data='TechnoCom')
button_IT_fest_2022 = InlineKeyboardButton(text='IT-fest_2022', callback_data='IT-fest_2022')
button_IASF2022 = InlineKeyboardButton(text='IASF2022 ', callback_data='IASF2022')
button_FestivalOKK = InlineKeyboardButton(text='ФестивальОКК', callback_data='ФестивальОКК')
button_Neirofest = InlineKeyboardButton(text='Нейрофест', callback_data='Нейрофест')
button_NevidimiyMir = InlineKeyboardButton(text='НевидимыйМир', callback_data='НевидимыйМир')
button_ConcursNIR = InlineKeyboardButton(text='КонкурсНИР', callback_data='КонкурсНИР')
button_VRARFest3D = InlineKeyboardButton(text='VRARFest3D', callback_data='VRARFest3D')

# Добавление кнопок.
buttons_inline.add(button_TechnoCom, button_IT_fest_2022, button_IASF2022, button_FestivalOKK,
                   button_Neirofest, button_NevidimiyMir, button_ConcursNIR, button_VRARFest3D,
                   button_subscribe_all, button_unsubscribe_all)

# Кнопки клавиатуры.
keyboard_button_start = KeyboardButton('Старт')
keyboard_button_contacts = KeyboardButton('Контакты')
keyboard_button_events = KeyboardButton('Мероприятия')
keyboard_button_subscribe = KeyboardButton('Подписаться/Отписаться')
keyboard_button_help = KeyboardButton('Помощь')

# Добавление кнопок.
buttons = ReplyKeyboardMarkup(resize_keyboard=True).add(keyboard_button_start,
                                                        keyboard_button_contacts,
                                                        keyboard_button_events,
                                                        keyboard_button_subscribe,
                                                        keyboard_button_help)


# Команда старт для начала работы с ботом.
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if message.chat.id == message.from_user.id:
        user_first_name = message['from']['first_name']
        user_last_name = message['from']['last_name']
        db.get_user_by_chat_id(message.chat.id)
        db.add_user(message.chat.id)
        if user_last_name:
            await message.reply('Здравствуйте, {} {}. Я чат-бот для подписки на новостные '
                                'мероприятия по хештегам '
                                'из ВКонтакте.'.format(user_first_name, user_last_name),
                                reply_markup=buttons)
        else:
            await message.reply('Здравствуйте, {}. Я чат-бот для подписки на новостные '
                                'мероприятия по хештегам '
                                'из ВКонтакте.'.format(user_first_name),
                                reply_markup=buttons)


# Команда для получения способов связи.
@dp.message_handler(commands=['contacts'])
async def contacts(message: types.Message):
    if message.chat.id == message.from_user.id:
        await message.reply('Если у вас возникли какие-либо вопросы, то вот наши контакты:\n'
                            'Группа ВКонтакте Научим.online https://vk.com/nauchim.online\n'
                            'Сайт с мероприятиями https://www.научим.online',
                            disable_web_page_preview=True)


# Команда для получения мероприятий.
@dp.message_handler(commands=['events'])
async def events(message: types.Message):
    if message.chat.id == message.from_user.id:
        await message.reply('Список мероприятий для подписки:\n'
                            '1. TechnoCom,\n'
                            '2. IT-fest_2022,\n'
                            '3. IASF2022,\n'
                            '4. ФестивальОКК,\n'
                            '5. Нейрофест,\n'
                            '6. НевидимыйМир,\n'
                            '7. КонкурсНИР,\n'
                            '8. VRARFest3D.')


# Команда для подписки.
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if message.chat.id == message.from_user.id:
        subscribed_list = list()
        events = db.get_events(message.chat.id)
        t = 1
        if events:
            for i in events:
                if int(i):
                    subscribed_list.append(events_dict_reverse[t])
                t += 1
        text = ''
        if len(subscribed_list) == 8:
            text = 'Вы подписаны на все новости.'
        elif subscribed_list:
            text = f'Выберите новости на которые хотите подписаться/отписаться.\n\n' \
                   f'Вы подписаны: {", ".join(subscribed_list)}\n\n'
        else:
            text = 'Выберите новости на которые хотите подписаться/отписаться.\n\n'
        await message.answer(text=text, reply_markup=buttons_inline)


# Команда для помощи в навигации функционала бота.
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    if message.chat.id == message.from_user.id:
        await message.reply('/start - Включение бота и возможность узнать его функционал.\n'
                            '/contacts - Как связаться?\n'
                            '/events - Мероприятия бота\n'
                            '/subscribe - Подписка/Отписка от мероприятий')


# Проверка наличие новых постов в группах и отправка их пользователю раз в час.
@aiocron.crontab('*/1 * * * *')
async def send_posts():
    for k, v in events_dict_reverse.items():
        post = parser.get_last_post(k)
        if post:
            if post[0] > parser.last_ids[k]:
                # Проверка наличия хештегов в посте и отправка постов.
                button_links = InlineKeyboardMarkup(row_width=1)
                button_link = InlineKeyboardButton(text='Пост', url=f'{events_posts_urls[k]}'
                                                                    f'{post[0]}')
                button_links.add(button_link)
                users = db.get_subscribed_users(k)
                if len(post) == 3:
                    if events_dict_tags[k] in post[2]:
                        for user_id in users:
                            user_id = user_id[0]
                            if len(post[2]) > 1024:
                                await bot.send_photo(photo=post[1], chat_id=user_id)
                                await bot.send_message(text=post[2], chat_id=user_id,
                                                       disable_web_page_preview=True,
                                                       reply_markup=button_links)
                            else:
                                await bot.send_photo(photo=post[1], caption=post[2], chat_id=user_id,
                                                     reply_markup=button_links)
                else:
                    if events_dict_tags[k] in post[1]:
                        for user_id in users:
                            user_id = user_id[0]
                            await bot.send_message(text=post[1], chat_id=user_id,
                                                   disable_web_page_preview=True,
                                                   reply_markup=button_links)
                parser.last_ids[k] = post[0]


# Реализация работы кнопок для подписки/отписки.
@dp.callback_query_handler(lambda c: c.data)
async def subscribe_events_button(callback_query: types.CallbackQuery):
    subscribed_list = list()
    if callback_query.data == 'button_unsubscribe':
        await bot.answer_callback_query(callback_query.id)
        db.update_subscribe_all(callback_query.message.chat.id, 0)
        await bot.edit_message_text(text='Вы отписались от всех новостей.',
                                    chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons_inline)

    elif callback_query.data == 'button_subscribe':
        await bot.answer_callback_query(callback_query.id)
        db.update_subscribe_all(callback_query.message.chat.id, 1)
        await bot.edit_message_text(text='Вы подписались на все новости.',
                                    chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    reply_markup=buttons_inline)
    else:
        await bot.answer_callback_query(callback_query.id)
        k = db.update_subscribe(callback_query.message.chat.id, events_dict[callback_query.data])
        if k:
            text = f'Вы подписались на {callback_query.data}'
        else:
            text = f'Вы отписались от {callback_query.data}'
        event = db.get_events(callback_query.message.chat.id)
        t = 1
        for i in event:
            if i:
                subscribed_list.append(events_dict_reverse[t])
            t += 1

        if len(subscribed_list) == 8:
            await bot.edit_message_text(text='Вы подписаны на все новости.',
                                        reply_markup=buttons_inline,
                                        chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id)
        elif subscribed_list:
            await bot.edit_message_text(
                text='Выберите новости на которые хотите подписаться/отписаться.\n'
                     f'{text}\n\n'
                     f'Вы подписаны: {", ".join(subscribed_list)}\n\n',
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                reply_markup=buttons_inline)

        else:
            await bot.edit_message_text(
                text='Выберите новости на которые хотите подписаться/отписаться.\n'
                     f'{text}\n\n',
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                reply_markup=buttons_inline)
        subscribed_list.clear()


# Получение сообщений и ответ на кнопки клавиатуры. Выполняет все тоже самое, что и команды.
@dp.message_handler()
async def catch_messages(message: types.Message):
    if message.chat.id == message.from_user.id:
        try:
            if message.text == 'Старт':
                user_first_name = message['from']['first_name']
                user_last_name = message['from']['last_name']
                db.get_user_by_chat_id(message.chat.id)
                db.add_user(message.chat.id)
                if user_last_name:
                    await message.reply('Здравствуйте, {} {}. Я чат-бот для подписки на новостные '
                                        'мероприятия по хештегам '
                                        'из ВКонтакте.'.format(user_first_name, user_last_name),
                                        reply_markup=buttons)
                else:
                    await message.reply('Здравствуйте, {}. Я чат-бот для подписки на новостные '
                                        'мероприятия по хештегам '
                                        'из ВКонтакте.'.format(user_first_name),
                                        reply_markup=buttons)

            elif message.text == 'Контакты':
                await message.reply(
                    'Если у вас возникли какие-либо вопросы, то вот наши контакты:\n'
                    'Группа ВКонтакте Научим.online https://vk.com/nauchim.online\n'
                    'Сайт с мероприятиями https://www.научим.online',
                    disable_web_page_preview=True)

            elif message.text == 'Мероприятия':
                await message.reply('Список мероприятий для подписки:\n'
                                    '1. TechnoCom,\n'
                                    '2. IT-fest_2022,\n'
                                    '3. IASF2022,\n'
                                    '4. ФестивальОКК,\n'
                                    '5. Нейрофест,\n'
                                    '6. НевидимыйМир,\n'
                                    '7. КонкурсНИР,\n'
                                    '8. VRARFest3D.')
            elif message.text == 'Подписаться/Отписаться':
                if message.chat.id == message.from_user.id:
                    subscribed_list = list()
                    events = db.get_events(message.chat.id)
                    t = 1
                    if events:
                        for i in events:
                            if int(i):
                                subscribed_list.append(events_dict_reverse[t])
                            t += 1
                    text = ""
                    if len(subscribed_list) == 8:
                        text = "Вы подписаны на все новости."
                    elif subscribed_list:
                        text = f'Выберите новости на которые хотите подписаться/отписаться.\n\n' \
                               f'Вы подписаны: {", ".join(subscribed_list)}\n\n'
                    else:
                        text = 'Выберите новости на которые хотите подписаться/отписаться.\n\n'
                    await message.answer(text=text, reply_markup=buttons_inline)

            elif message.text == 'Помощь':
                await message.reply('/start - Включение бота и возможность узнать его функционал.\n'
                                    '/contacts - Как связаться?\n'
                                    '/events - Мероприятия бота\n'
                                    '/subscribe - Подписка/Отписка от мероприятий')

        except:
            pass


if __name__ == '__main__':
    executor.start_polling(dp)
