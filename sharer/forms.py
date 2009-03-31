from django import forms
from django.utils.translation import ugettext_lazy as _


class EmailShareForm(forms.Form):
    recipient = forms.EmailField(label=_("To"), widget=forms.TextInput(attrs={"class": "text"}))
    sender = forms.EmailField(label=_("From"), widget=forms.TextInput(attrs={"class": "text"}))
    message = forms.CharField(label=_("Message"), widget=forms.Textarea, required=False)
    url = forms.CharField(label=_("URL"), widget=forms.HiddenInput, required=False)
    title = forms.CharField(label=_("Title"), widget=forms.HiddenInput, required=False)
