from urlparse import urljoin

from django import template
from django.contrib.sites.models import Site
from django.template.defaultfilters import urlencode

from sharer.forms import EmailShareForm
from sharer.models import SocialNetwork
from sharer.settings import ENABLE_EMAILS


register = template.Library()


@register.inclusion_tag("sharer/includes/widget.html", takes_context=True)
def share(context, title="", url=""):
    """
    Renders the share widget
    """
    networks = SocialNetwork.objects.all()

    if not url:
        url = context.get("SHARE_URI", "")

    if url.startswith("/"):
        site = Site.objects.get_current()

        if site:
            url = urljoin("http://%s" % site.domain, url)

    return {
        "networks": networks,
        "title": title,
        "url": url,
        "ENABLE_EMAILS": ENABLE_EMAILS,
        "MEDIA_URL": context.get("MEDIA_URL", ""),
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE", ""),
    }


@register.simple_tag
def share_url(network, title="", url=""):
    """
    Builds a network url with given variables
    """
    return network.url % {
        "url": urlencode(url),
        "title": urlencode(title),
    }
