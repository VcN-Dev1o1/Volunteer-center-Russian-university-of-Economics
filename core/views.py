from django.shortcuts import render
from django.utils import timezone
from django.db import models
from .models import News
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import News
from .services import get_hero_news
from .models import SiteSettings

def _settings_obj():
    return SiteSettings.objects.first()

def handler404(request, exception):
    return render(request, "errors/404.html", {"site_settings": _settings_obj()}, status=404)

def handler500(request):
    return render(request, "errors/500.html", {"site_settings": _settings_obj()}, status=500)

HERO_LIMIT = 4

def index(request):
    hero_news = get_hero_news()
    return render(request, "core/index.html", {"hero_news": hero_news})

def about(request):
    return render(request, "core/about.html")

def checklist(request):
    return render(request, "core/checklist.html")

def team(request):
    return render(request, "core/team.html")

def graduates(request):
    return render(request, "core/graduates.html")

def dobro(request):
    return render(request, "core/dobro.html")

def get_hero_news():
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

    items += list(qs[: max(0, HERO_LIMIT - len(items))])
    return items


def news_list(request):
    q = request.GET.get("q", "").strip()
    qs = News.objects.filter(is_published=True)

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(lead__icontains=q) |
            Q(body__icontains=q)
        )

    qs = qs.order_by("-published_at", "-created_at")
    return render(request, "core/news_list.html", {"news_list": qs, "q": q})

def page_not_found_view(request, exception=None):
    return render(
        request,
        "system/under_construction.html",
        status=404
    )

def news_detail(request, pk: int):
    obj = get_object_or_404(News, pk=pk, is_published=True)
    return render(request, "core/news_detail.html", {"news": obj})