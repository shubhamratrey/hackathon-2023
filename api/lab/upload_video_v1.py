from api.responses.base import APIResponseBase
from utils.validators import allowed_methods
from experiments.models import Video
from experiments.celery_tasks import separate_audio_from_file


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
        if not (youtube_url or output_language or input_language):
            self.set_404('Param missing', "INVALID_PARAM")
            return data

        if Video.objects.filter(youtube_url=youtube_url, input_language=input_language,
                                output_language=output_language).exists():
            self.set_404('Video already exists', "INVALID_VIDEO_URL")
            return data

        video = Video()
        video.output_language = output_language
        video.input_language = input_language
        video.youtube_url = youtube_url
        video.save()
        data['message'] = "Link queued"
        data['video_id'] = video.id
        data['video_youtube_link'] = video.youtube_url
        separate_audio_from_file.delay(video_id=video.id)
        return data
