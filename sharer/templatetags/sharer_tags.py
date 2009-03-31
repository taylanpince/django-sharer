from django import template
from django.template.defaultfilters import urlencode

from sharer.forms import EmailShareForm
from sharer.models import SocialNetwork


register = template.Library()


@register.inclusion_tag("sharer/includes/widget.html", takes_context=True)
def share(context, title="", url=""):
    """
    Renders the share widget
    """
    networks = SocialNetwork.objects.all()

    if not url:
        url = context.get("SHARE_URI", "")

    form = EmailShareForm(auto_id=None, initial={
        "url": url,
        "title": title,
    })

    return {
        "networks": networks,
        "title": title,
        "url": url,
        "form": form,
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
