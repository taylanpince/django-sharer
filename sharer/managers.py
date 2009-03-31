from django.db import models


class SocialNetworkManager(models.Manager):
    """
    A custom manager that only returns active social networks
    """
    def get_query_set(self):
        return super(SocialNetworkManager, self).get_query_set().filter(active=True)
