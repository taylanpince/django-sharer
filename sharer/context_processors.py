def share_uri(request):
    """
    A context processor that adds the absolute URL to the context
    """
    return {
        "SHARE_URI": request.build_absolute_uri(),
    }
