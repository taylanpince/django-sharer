from django.conf import settings


ENABLE_EMAILS = getattr(settings, "SHARER_ENABLE_EMAILS", True)