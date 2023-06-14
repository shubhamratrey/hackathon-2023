from api.responses.base import APIResponseBase
from utils.validators import allowed_methods
from experiments.models import Video


class GetVideoDetailV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')

    def __init__(self, **kwargs):
        super(GetVideoDetailV1, self).__init__(**kwargs)
        self.allowed_methods = ('GET',)

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        video_id = self.get_param('video_id')
        yt_link = self.get_param('yt_link')
        if yt_link:
            try:
                video = Video.objects.get(youtube_url=yt_link)
            except Video.DoesNotExist:
                return data
        elif video_id:
            try:
                video = Video.objects.get(pk=video_id)
            except Video.DoesNotExist:
                return data
        else:
            self.set_404("Param missing", "INVALID_PARAM")
            return data

        data['video'] = video.to_json()
        return data
