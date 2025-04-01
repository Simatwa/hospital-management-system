from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum
from hospital.utils import generate_document_filepath
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here.


class About(models.Model):
    name = models.CharField(
        max_length=40, help_text="The hospital name", default="Smart Hospital"
    )
    short_name = models.CharField(
        max_length=30, help_text="Hospital abbreviated name", default="SH"
    )
    slogan = models.TextField(
        help_text=_("Hospital's slogan"), default="We treat but God heals."
    )
    details = models.TextField(
        help_text=_("Hospital details"),
        default="Welcome to our hospital. We are committed to providing the best healthcare services.",
        null=False,
        blank=False,
    )
    location_name = models.CharField(
        max_length=200, help_text=_("Hospital location name(s)"), default="Meru - Kenya"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=0.000000,
        help_text=_("Latitude of the hospital location"),
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        default=0.000000,
        help_text=_("Longitude of the hospital location"),
    )
    founded_in = models.DateField(
        help_text=_("Date when the hospital was founded"), default=timezone.now
    )
    founder_name = models.CharField(
        max_length=50, help_text=_("Name of the hospital founder"), default="GoK"
    )
    mission = models.TextField(
        help_text=_("Hospital's mission statement"),
        default="To provide quality healthcare services to all.",
    )
    vision = models.TextField(
        help_text=_("Hospital's vision statement"),
        default="To be the leading healthcare provider in the region.",
    )
    email = models.EmailField(
        max_length=50,
        help_text="Website's admin email",
        null=True,
        blank=True,
        default="admin@hospital.com",
    )
    phone_number = models.CharField(
        max_length=50,
        help_text="Hospital's hotline number",
        null=True,
        blank=True,
        default="0200000000",
    )
    facebook = models.URLField(
        max_length=100,
        help_text=_("Hospital's Facebook profile link"),
        null=True,
        blank=True,
        default="https://www.facebook.com/",
    )
    twitter = models.URLField(
        max_length=100,
        help_text=_("Hospital's X (formerly Twitter) profile link"),
        null=True,
        blank=True,
        default="https://www.x.com/",
    )
    linkedin = models.URLField(
        max_length=100,
        help_text=_("Hospital's Facebook profile link"),
        null=True,
        blank=True,
        default="https://www.linkedin.com/",
    )
    instagram = models.URLField(
        max_length=100,
        help_text=_("Hospital's Instagram profile link"),
        null=True,
        blank=True,
        default="https://www.instagram.com/",
    )
    tiktok = models.URLField(
        max_length=100,
        help_text=_("Hospital's Tiktok profile link"),
        null=True,
        blank=True,
        default="https://www.tiktok.com/",
    )
    youtube = models.URLField(
        max_length=100,
        help_text=_("Hospital's Youtube profile link"),
        null=True,
        blank=True,
        default="https://www.youtube.com/",
    )
    logo = models.ImageField(
        help_text=_("Hospital logo  (preferrably 64*64px png)"),
        upload_to=generate_document_filepath,
        default="/static/hospital/img/logo.png",
    )
    wallpaper = models.ImageField(
        help_text=_("Hospital wallpaper image"),
        upload_to=generate_document_filepath,
        default="default/surgery-1822458_1920.jpg",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the hospital details was created"),
    )

    def __str__(self):
        return self.name


class ServiceFeedback(models.Model):
    class FeedbackRate(Enum):
        EXCELLENT = "Excellent"
        GOOD = "Good"
        AVERAGE = "Average"
        POOR = "Poor"
        TERRIBLE = "Terrible"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    sender = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, help_text=_("Feedback sender")
    )
    message = models.TextField(help_text=_("Response body"))
    rate = models.CharField(
        max_length=15, choices=FeedbackRate.choices(), help_text=_("Feedback rating")
    )
    show_in_index = models.BooleanField(
        default=True,
        help_text=_("Display this feedback in website's feedback sections."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
    )

    def __str__(self):
        return f"{self.rate} feedback from {self.sender}"


class Gallery(models.Model):
    title = models.CharField(max_length=50, help_text=_("Gallery title"))
    details = models.TextField(help_text=_("What about this gallery?"))
    location_name = models.CharField(
        max_length=100, help_text=_("Event location name"), default="Hospital"
    )
    picture = models.ImageField(
        help_text=_("Gallery photograph"),
        upload_to=generate_document_filepath,
        default="default/surgery-1822458_1920.jpg",
    )
    video_link = models.URLField(
        max_length=100, help_text=_("YouTube video link"), null=True, blank=True
    )
    date = models.DateField(help_text="Gallery date", default=timezone.now)
    show_in_index = models.BooleanField(
        default=True, help_text=_("Display this gallery in website's gallery section.")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when the gallery was last updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the gallery was created"),
    )

    def __str__(self):
        return f"{self.title} in {self.location_name} on {self.date}"

    class Meta:
        verbose_name_plural = _("Galleries")


class News(models.Model):
    class NewsCategory(Enum):
        GENERAL = "General"
        HEALTH = "Health"
        EVENTS = "Events"
        ANNOUNCEMENTS = "Announcements"

        @classmethod
        def choices(cls):
            return [(key.value, key.name) for key in cls]

    title = models.CharField(max_length=80, help_text=_("News title"))
    category = models.CharField(
        max_length=20,
        choices=NewsCategory.choices(),
        default=NewsCategory.GENERAL.value,
        help_text=_("Select the category of the news"),
    )
    content = RichTextField(help_text=_("News in detail"))
    summary = models.TextField(help_text=_("News in brief"))
    cover_photo = models.ImageField(
        help_text=_("News cover photo"),
        upload_to=generate_document_filepath,
        default="default/news-3584901_66059.jpg",
    )
    document = models.FileField(
        help_text=_("Any relevant file attached to the news"),
        upload_to=generate_document_filepath,
        null=True,
        blank=True,
    )
    video_link = models.URLField(
        max_length=100,
        help_text=_("Youtube video link relatint to the news"),
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(default=True, help_text=_("Publish this news."))
    views = models.IntegerField(
        default=0, help_text=_("Number of times the news has been requested.")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when the news was last updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the news was created"),
    )

    class Meta:
        verbose_name_plural = _("News")

    def __str__(self):
        return f"'{self.title}' on {self.created_at.strftime('%d-%b-%Y %H:%M:%S')}"

    def save(self, *args, **kwargs):
        if not self.id:  # new entry
            # Consider mailing subscribers
            pass
        super().save(*args, **kwargs)


class Subscriber(models.Model):
    email = models.EmailField(help_text=_("Email address"), unique=True)
    token = models.UUIDField(help_text="Subscription confirmation token", unique=True)
    is_verified = models.BooleanField(default=False, help_text=_("Verification status"))

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when the gallery was last updated"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the gallery was created"),
    )

    def __str__(self):
        return self.email
