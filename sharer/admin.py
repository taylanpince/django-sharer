from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from sharer.models import SocialNetwork


class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ("name", "active", )
    list_filter = ["active", ]

    save_on_top = True

    fieldsets = (
        (None, {
            "fields": ("name", "icon", "url", "active", )
        }),
    )


admin.site.register(SocialNetwork, SocialNetworkAdmin)
