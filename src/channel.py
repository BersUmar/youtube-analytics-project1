import json
from googleapiclient.discovery import build


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = 'AIzaSyC0Nw4aXViNRruPbFlpCTimcvqQBtt20mw'

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    # , customUrl, subscriberCount: int, videoCount: int, viewCount: int
    def __init__(self, channel_id: str) -> None:
        channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.customUrl = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.viewCount = channel["items"][0]["statistics"]["viewCount"]
        self.subscriberCount = int(channel["items"][0]["statistics"]["subscriberCount"])
        self.videoCount = channel["items"][0]["statistics"]["videoCount"]

    def __str__(self) -> str:
        return f'{self.title}{self.customUrl}'

    def __add__(self, other: int) -> int:
        return self.subscriberCount + other.subscriberCount

    def __sub__(self, other: int) -> int:
        return self.subscriberCount - other.subscriberCount

    def __mul__(self, other: int):
        return self.subscriberCount * other.subscriberCount

    def __truediv__(self, other: int) -> float:
        return self.subscriberCount / other.subscriberCount

    def __lt__(self, other: int) -> bool:
        return self.subscriberCount < other.subscriberCount

    def __le__(self, other: int) -> bool:
        return self.subscriberCount <+ other.subscriberCount

    def __gt__(self, other: int) -> bool:
        return self.subscriberCount > other.subscriberCount

    def __ge__(self, other: int) -> bool:
        return self.subscriberCount >= other.subscriberCount



    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_id = self.__channel_id
        channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = channel["items"]["snippet"]["title"]
        self.description = channel["items"]["snippet"]["description"]
        printj(channel)

    @classmethod
    def get_service(cls):
        # создать специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=Channel.api_key)
        return youtube

    def to_json(self, f):
        task1 = {
            'id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'view_count': self.viewCount,
            'subscriber_count': self.subscriberCount,
            'video_count': self.videoCount,
            'url': self.customUrl
        }
        with open(f, 'w', encoding='utf-8') as file:
            json.dump(task1, file, indent=2, ensure_ascii=False)
