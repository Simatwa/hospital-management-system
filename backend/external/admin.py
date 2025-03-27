from django.contrib import admin
from external.models import About, ServiceFeedback, Gallery, News, Subscriber
from django.utils.translation import gettext_lazy as _

# Register your models here.


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "founded_in", "founder_name", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "short_name", "slogan", "details")}),
        (
            _("Location"),
            {"fields": ("location_name", "latitude", "longitude")},
        ),
        (
            _("History"),
            {"fields": ("founded_in", "founder_name")},
        ),
        (
            _("Statements"),
            {"fields": ("mission", "vision")},
        ),
        (
            _("Contact"),
            {
                "fields": (
                    "phone_number",
                    "email",
                )
            },
        ),
        (
            _("Social Media"),
            {
                "fields": (
                    "facebook",
                    "twitter",
                    "linkedin",
                    "instagram",
                    "tiktok",
                    "youtube",
                )
            },
        ),
        (
            _("Media"),
            {"fields": ("logo", "wallpaper")},
        ),
    )


@admin.register(ServiceFeedback)
class ServiceFeedbackAdmin(admin.ModelAdmin):
    list_display = ("sender", "rate", "show_in_index", "updated_at", "created_at")
    search_fields = ("sender__username", "message")
    list_filter = ("rate", "show_in_index", "updated_at", "created_at")
    list_editable = ("show_in_index",)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("title", "picture", "show_in_index", "date", "updated_at")
    search_fields = ("title",)
    list_filter = ("date", "created_at")
    list_editable = ("show_in_index",)

    fieldsets = (
        (None, {"fields": ("title", "details", "location_name", "date")}),
        (_("Media & Display"), {"fields": ("picture", "video_link", "show_in_index")}),
    )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "views", "created_at")
    list_filter = ("category", "created_at", "updated_at", "views")
    search_fields = ("title", "summary")
    fieldsets = (
        (
            None,
            (
                {
                    "fields": (
                        "title",
                        "category",
                        "content",
                        "summary",
                    )
                }
            ),
        ),
        (_("Media"), ({"fields": ("cover_photo", "document", "video_link")})),
    )
    list_editable = ("is_published",)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "is_verified",
        "updated_at",
        "created_at",
    )
    list_filter = ("is_verified", "updated_at", "created_at")
    search_fields = ("email",)
