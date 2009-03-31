from django import template

from sharer.models import SocialNetwork


register = template.Library()


@register.inclusion_tag("sharer/includes/widget.html", takes_context=True)
def share(context, title="", url=""):
    """
    Renders the share widget
    """
    networks = SocialNetwork.objects.all()

    if not url:
        url = context.get("SHARE_URI", None)

    return {
        "networks": networks,
        "title": title,
        "url": url,
        "MEDIA_URL": context.get("MEDIA_URL", None),
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE", None),
    }


@register.simple_tag
def share_url(network, title="", url=""):
    """
    Builds a network url with given variables
    """
    return network.url % {
        "url": url,
        "title": title,
    }
