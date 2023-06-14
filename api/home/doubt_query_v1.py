from api.responses.base import APIResponseBase
from utils.validators import allowed_methods


class DoubtQueryV1(APIResponseBase):
    __versions_compatible__ = ('1', '1.0')

    def __init__(self, **kwargs):
        super(DoubtQueryV1, self).__init__(**kwargs)
        self.allowed_methods = ('GET',)

    @allowed_methods
    def get_or_create_data(self):
        data = {}
        data['text'] = "Success"
        return data
