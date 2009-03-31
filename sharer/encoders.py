from django.utils import simplejson
from django.utils.encoding import force_unicode
from django.utils.functional import Promise


class LazyEncoder(simplejson.JSONEncoder):
    """
    Convert lazy translations before being passed on to simplejson's encoder
    """
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)

        return obj
