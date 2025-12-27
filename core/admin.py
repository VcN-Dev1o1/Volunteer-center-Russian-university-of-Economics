from django.contrib import admin
from .models import (
    Volunteer,
    VolunteerOfMonth,
    Partner,
    Event,
    Page,
    PhotoAlbum,
    Photo,
    Video,
    SiteConfig,
    News,
    NewsBlock,
    SiteSettings,
)


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "username", "email", "created_at")
    search_fields = ("full_name", "username", "email")
    list_filter = ("faculty",)


@admin.register(VolunteerOfMonth)
class VolunteerOfMonthAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "month", "year")
    list_filter = ("year", "month")
    autocomplete_fields = ("volunteer",)


class NewsBlockInline(admin.TabularInline):
    model = NewsBlock
    extra = 0
    max_num = 10


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_at", "place", "is_public")
    list_filter = ("is_public", "start_at")
    search_fields = ("title", "place")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
    search_fields = ("name",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsBlockInline]
    list_display = ("title", "is_published", "is_pinned", "pin_until", "published_at")
    list_filter = ("is_published", "is_pinned")
    search_fields = ("title", "lead", "body", "editor_name")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_public")
    list_filter = ("is_public",)
    prepopulated_fields = {"slug": ("title",)}


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


@admin.register(PhotoAlbum)
class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    inlines = [PhotoInline]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "youtube_id", "created_at")


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ("key", "title")
    search_fields = ("key", "title")

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "hero_autoplay_delay", "university_url", "smedia_url")