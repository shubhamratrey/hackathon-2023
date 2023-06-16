from api.responses.base import APIResponseBase
from utils.validators import allowed_methods
from experiments.models import Video
from experiments.celery_tasks import extract_title


class UploadVideoV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')

    def __init__(self, **kwargs):
        super(UploadVideoV1, self).__init__(**kwargs)
        self.allowed_methods = ('POST', 'GET')

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        youtube_url = self.get_param('video_url')
        output_language = self.get_param('output_language')
        input_language = self.get_param('input_language')
        uid = self.get_param('uid')
        voice_gender = str(self.get_param('voice_gender')).lower()
        if not (youtube_url or output_language or input_language or voice_gender):
            self.set_404('Param missing', "INVALID_PARAM")
            return data
        # if not uid:
        #     self.set_404('UID missing', "INVALID_UID")
        #     return data
        voice_gender = str(voice_gender).lower()
        voice_gender = "M" if voice_gender == "male" else "F"

        try:
            video = Video.objects.get(youtube_url=youtube_url, input_language=input_language,
                                      output_language=output_language, voice_gender=voice_gender)
        except Video.DoesNotExist:
            pass
        else:
            if video and uid:
                existing_video = Video()
                existing_video.title = video.title
                existing_video.slug = video.slug + "-" + uid
                existing_video.duration = video.duration
                existing_video.youtube_url = video.youtube_url
                existing_video.input_language = video.input_language
                existing_video.output_language = video.output_language
                existing_video.voice_gender = video.voice_gender
                existing_video.status = video.status
                existing_video.owner_id = str(uid)
                existing_video.translated_text = video.translated_text
                existing_video.transcription = video.transcription
                existing_video.voice_id = video.voice_id
                existing_video.media_key = video.media_key
                existing_video.save()

                data['video'] = existing_video.to_json()
                data['message'] = 'Video already exists'
                return data

        video = Video()
        video.output_language = output_language
        video.input_language = input_language
        video.youtube_url = youtube_url
        video.slug = youtube_url
        if uid:
            video.owner_id = str(uid)
        video.voice_gender = voice_gender
        video.save()
        data['message'] = "Link queued"
        data['video'] = video.to_json()
        extract_title.delay(video_id=video.id)
        return data
