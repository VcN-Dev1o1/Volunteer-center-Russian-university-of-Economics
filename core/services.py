from django.db import models
from django.utils import timezone
from .models import News

HERO_LIMIT = 4

def get_hero_news(limit: int = HERO_LIMIT):
    now = timezone.now()

    pinned = (
        News.objects.filter(is_published=True, is_pinned=True)
        .filter(models.Q(pin_until__isnull=True) | models.Q(pin_until__gt=now))
        .order_by("-published_at", "-created_at")
        .first()
    )

    qs = News.objects.filter(is_published=True).order_by("-published_at", "-created_at")

    items = []
    if pinned:
        items.append(pinned)
        qs = qs.exclude(pk=pinned.pk)

    items += list(qs[: max(0, limit - len(items))])
    return items
