import os


from googleapiclient.discovery import build

class Video:
    """Класс для работы с видео из ютуба."""
    api_key: str = 'AIzaSyC0Nw4aXViNRruPbFlpCTimcvqQBtt20mw'

    def __init__(self, video_id: str) -> None:
        """Видео инициализируется id и далее через API"""
        self.__video_id = video_id
        self._init_from_api = self.get_service()
        self.title = self._init_from_api['items'][0]['snippet']['title']
        self.url = self._init_from_api['items'][0]['id']
        self.view_count = self._init_from_api['items'][0]['statistics']['viewCount']
        self.like_count = self._init_from_api['items'][0]['statistics']['likeCount']


    def get_service(self):
        # создать специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=Video.api_key)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.__video_id
                                               ).execute()
        return video_response


    def __str__(self) -> str:
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id