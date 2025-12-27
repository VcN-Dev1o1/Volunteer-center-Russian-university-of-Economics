from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path("news/<int:pk>/", views.news_detail, name="news_detail"),
    path("admin/", admin.site.urls),
    path("", include("core.urls")),


    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("checklist/", views.checklist, name="checklist"),
    path("team/", views.team, name="team"),
    path("graduates/", views.graduates, name="graduates"),
    path("dobro/", views.dobro, name="dobro"),

    path("news/", views.news_list, name="news_list"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.views.handler404"
handler500 = "core.views.handler500"
