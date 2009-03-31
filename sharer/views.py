from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic import simple

from sharer.forms import EmailShareForm


def share(request, mimetype="plain", subject_template="sharer/subject.txt", body_template="sharer/body.txt"):
    """
    If this is a POST request, validates the form and sends an email if valid
    If not, renders the blank form
    """
    if request.method == "POST":
        form = EmailShareForm(request.POST, auto_id=None)

        if form.is_valid():
            context = {
                "site": Site.objects.get_current(),
            }

            context.update(form.cleaned_data)

            subject = render_to_string(subject_template, context)
            body = render_to_string(body_template, context)

            email = EmailMessage(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [form.cleaned_data.get("recipient")],
                headers={
                    "Reply-to": form.cleaned_data.get("sender"),
                }
            )

            email.content_subtype = mimetype
            email.send()

            return HttpResponseRedirect(reverse("sharer_done"))
    else:
        form = EmailShareForm(auto_id=None, initial={
            "url": request.GET.get("url", request.META.get("HTTP_REFERER", "")),
            "title": request.GET.get("title", ""),
        })

    return simple.direct_to_template(request, "sharer/form.html", {
        "form": form,
    })


def share_done(request):
    """
    Renders a thank you page
    """
    return simple.direct_to_template(request, "sharer/done.html")
