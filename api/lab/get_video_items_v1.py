from api.responses.base import APIResponseBase
from django.core.paginator import Paginator, InvalidPage
from utils.validators import allowed_methods
from experiments.models import Video


class GetVideoItemsV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')
    __page_size__ = 20

    def __init__(self, **kwargs):
        super(GetVideoItemsV1, self).__init__(**kwargs)
        self.allowed_methods = ('GET',)

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        page_no = self.get_sanitized_int(self.request.GET.get('page', 1)) or 1
        page_size = self.get_sanitized_int(self.request.GET.get('page_size')) or self.__page_size__
        if not page_no:
            self.set_bad_req("Invalid page number: {}".format(page_no), 'INVALID_PAGE')
            return data
        owner_id = self.get_param("uid")
        if owner_id == "all":
            videos = Video.objects.all().order_by('-id')
        else:
            videos = Video.objects.filter(owner_id=owner_id).order_by('-id')
        paginator = Paginator(videos, page_size)
        try:
            paginated_languages = paginator.page(page_no)
        except InvalidPage:
            self.set_bad_req('Invalid page.', 'INVALID_PAGE')
            return data
        videos = []
        for video in paginated_languages:
            doc = video.to_json()
            videos.append(doc)
        data['videos'] = videos
        data['n_pages'] = paginator.num_pages
        data['n_videos'] = paginator.count
        if (self.__page_size__ * page_no) < paginator.count:
            data['next_page'] = page_no + 1
        data['page'] = page_no
        return data
