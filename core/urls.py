from django.contrib import admin
from django.urls import path
from core.views import index
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="home"),
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("checklist/", views.checklist, name="checklist"),
    path("team/", views.team, name="team"),
    path("graduates/", views.graduates, name="graduates"),
    path("dobro/", views.dobro, name="dobro"),
    path("news/", views.news_list, name="news_list"),
    path("news/<int:pk>/", views.news_detail, name="news_detail"),
]

app_name = "core"


