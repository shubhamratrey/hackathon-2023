import sys
from functools import WRAPPER_ASSIGNMENTS

import json
from functools import wraps

from django.http import HttpResponse


def available_attrs(fn):
    """
    Return the list of functools-wrappable attributes on a callable.
    This is required as a workaround for http://bugs.python.org/issue3445
    under Python 2.
    """
    if sys.version_info[0] == 3:
        return WRAPPER_ASSIGNMENTS
    else:
        return tuple(a for a in WRAPPER_ASSIGNMENTS if hasattr(fn, a))


def login_required(function):
    @wraps(function, assigned=available_attrs(function))
    def wrapped_function(request, *args, **kwargs):
        # user = request.user
        # if request.user.is_authenticated:
        #     return function(request, *args, **kwargs)

        if request.GET.get('uid', None):
            return function(request, *args, **kwargs)

        if request.path.startswith('/'):
            return HttpResponse(json.dumps({
                'status': 'error',
                'status_code': 401,
                'message': 'Login required to access this resource'}),
                content_type='application/json',
                status=401)

    return wrapped_function
