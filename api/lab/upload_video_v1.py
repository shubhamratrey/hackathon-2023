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
        if not (youtube_url or output_language or input_language):
            self.set_404('Param missing', "INVALID_PARAM")
            return data

        try:
            video = Video.objects.get(youtube_url=youtube_url, input_language=input_language,
                                      output_language=output_language)
        except Video.DoesNotExist:
            pass
        else:
            if video:
                data['video'] = video.to_json()
                data['message'] = 'Video already exists'
                return data

        # if Video.objects.filter(youtube_url=youtube_url, input_language=input_language,
        #                         output_language=output_language).exists():
        #     self.set_404('Video already exists', "INVALID_VIDEO_URL")
        #     return data

        video = Video()
        video.output_language = output_language
        video.input_language = input_language
        video.youtube_url = youtube_url
        video.slug = youtube_url
        video.save()
        data['message'] = "Link queued"
        data['video'] = video.to_json()
        extract_title.delay(video_id=video.id)
        return data
