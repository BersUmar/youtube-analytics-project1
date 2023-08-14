import isodate
import datetime
from googleapiclient.discovery import build




class PlayList:
    api_key = 'AIzaSyC0Nw4aXViNRruPbFlpCTimcvqQBtt20mw'
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, id: str):
        self.id = id
        self.playlist_videos = self.youtube.playlists().list(id=self.id,
                                                        part='snippet').execute()
        self.title = self.playlist_videos['items'][0]['snippet']['title']
        # ссылка на плейлист
        self.url = f'https://www.youtube.com/playlist?list={self.id}'

    @property
    def total_duration(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        x = datetime.timedelta(
            days=0,
            seconds=0,
            microseconds=0,
            milliseconds=0,
            minutes=0,
            hours=0,
            weeks=0
        )
        for video in video_response['items']:

            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            x += duration
        return x


    def show_best_video(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.id
                                               ).execute()
        like_counter = 0
        id = ''
        for x in video_ids:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=x
                                                        ).execute()
            likes: int = video_response['items'][0]['statistics']['likeCount']
            if int(likes) >= like_counter:
                like_counter = int(likes)
                id = x
        return f'https://youtu.be/{id}'
