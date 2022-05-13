import vk
from tokens import VK_TOKEN
from database import DataBase

db = DataBase('IT-FEST DataBase.sqlite')


class VkParser:
    def __init__(self):
        self.session = vk.Session(access_token=VK_TOKEN)
        self.api = vk.API(self.session, v=5.131, lang="ru", timeout=10)
        self.events_dict_reverse = {1: '#TechnoCom',
                                    2: '#ITfest_2022',
                                    3: '#IASF2022',
                                    4: '#ФестивальОКК',
                                    5: '#Нейрофест',
                                    6: '#НевидимыйМир',
                                    7: '#КонкурсНИР',
                                    8: '#VRARFest3D'
                                    }
        # Словарь соответствует номеру мероприятия в боте и айдишнику мероприятия в ВК
        self.events_dict = {1: '-210998761',
                            2: '-210985709',
                            3: '-196557207',
                            4: '-211638918',
                            5: '-211803420',
                            6: '-200248443',
                            7: '-200248443',
                            8: '-200248443'
                            }

        # Словарь соответствует номеру мероприятия в боте и айдишнику последнего поста в ВК
        self.last_ids = {}
        self.get_last_id_posts()

    def get_last_id_posts(self):
        """Получает и записывает айди последних постов в словарь."""
        for k, v in self.events_dict.items():
            posts = self.api.wall.get(owner_id=v, count=1)
            if posts['items']:
                post = posts['items'][0]
                self.last_ids[k] = post['id']
            else:
                self.last_ids[k] = -1

    def get_last_post(self, event_number):
        """Получает последний пост и возвращает список с айди поста, картинкой и текстом."""
        posts = self.api.wall.get(owner_id=self.events_dict[event_number], count=1)
        if posts['items']:
            post = posts['items'][0]
            data = [post['id']]
            photo = ''
            video = ''
            if 'attachments' in post:
                if post['attachments']:
                    for attr in post['attachments']:
                        if attr['type'] == 'photo':
                            photo = attr['photo']['sizes'][-1]['url']
                        if attr['type'] == 'video':
                            video = attr['video']['image'][-1]['url']
            if photo:
                data.append(photo)
            elif video:
                data.append(video)
            data.append(post['text'])
            return data
        return None

