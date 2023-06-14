from api.responses.base import APIResponseBase
from utils.validators import allowed_methods
from experiments.models import Video
from experiments.celery_tasks import replace_video_audio


class GetVideoDetailV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')

    def __init__(self, **kwargs):
        super(GetVideoDetailV1, self).__init__(**kwargs)
        self.allowed_methods = ('POST', 'GET')

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        video_id = self.kwargs.get('video_id')
        try:
            video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return data
        replace_video_audio(video_id=video_id)
        data.update({
            'id': video.id,
            'title': video.title,
            'slug': video.slug,
            'transcription': video.transcription
        })
        return data
