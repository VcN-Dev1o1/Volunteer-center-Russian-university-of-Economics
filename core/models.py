from django.db import models
from django.utils import timezone
from django.urls import reverse


class Volunteer(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    username = models.CharField("Логин", max_length=150, blank=True)
    email = models.EmailField("E-mail", blank=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    faculty = models.CharField("Факультет / институт", max_length=255, blank=True)
    about = models.TextField("О себе", blank=True)
    created_at = models.DateTimeField("Дата регистрации", default=timezone.now)

    class Meta:
        verbose_name = "Волонтёр"
        verbose_name_plural = "Волонтёры"

    def __str__(self):
        return self.full_name


class VolunteerOfMonth(models.Model):
    volunteer = models.ForeignKey(
        Volunteer,
        on_delete=models.CASCADE,
        related_name="month_awards",
        verbose_name="Волонтёр",
    )
    month = models.PositiveSmallIntegerField("Месяц")   # 1–12
    year = models.PositiveSmallIntegerField("Год")
    description = models.TextField("Описание / заслуги")

    class Meta:
        verbose_name = "Волонтёр месяца"
        verbose_name_plural = "Волонтёры месяца"
        unique_together = ("month", "year")

    def __str__(self):
        return f"{self.volunteer} — {self.month:02}.{self.year}"


class Partner(models.Model):
    name = models.CharField("Название партнёра", max_length=255)
    logo = models.ImageField("Логотип", upload_to="partners/", blank=True, null=True)
    url = models.URLField("Сайт", blank=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField("Название мероприятия", max_length=255)
    description = models.TextField("Описание")
    start_at = models.DateTimeField("Дата и время начала")
    end_at = models.DateTimeField("Дата и время окончания", blank=True, null=True)
    place = models.CharField("Место проведения", max_length=255)
    is_public = models.BooleanField("Показывать на сайте", default=True)

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ["-start_at"]

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=180)
    lead = models.TextField(blank=True)
    body = models.TextField()  # можно заменить на RichText позже
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    editor_name = models.CharField("Автор/редактор", max_length=120, blank=True, default="ВЦ РЭУ")


    # публикация
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(auto_now_add=True)

    # закреп
    is_pinned = models.BooleanField(default=False)
    pin_until = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"pk": self.pk})

    @property
    def is_pin_active(self):
        if not self.is_pinned:
            return False
        if not self.pin_until:
            return True  # закреп бессрочный, если хочешь
        return self.pin_until > timezone.now()

    def publish(self):
        if not self.published_at:
            self.published_at = timezone.now()
        self.is_published = True
        self.save(update_fields=["is_published", "published_at"])


class Page(models.Model):
    title = models.CharField("Заголовок страницы", max_length=255)
    slug = models.SlugField("URL-адрес", unique=True)
    body = models.TextField("Содержимое")
    is_public = models.BooleanField("Показывать на сайте", default=True)

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"

    def __str__(self):
        return self.title


class PhotoAlbum(models.Model):
    title = models.CharField("Название альбома", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = "Фотоальбом"
        verbose_name_plural = "Фотоальбомы"

    def __str__(self):
        return self.title


class Photo(models.Model):
    album = models.ForeignKey(
        PhotoAlbum,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="Альбом",
    )
    image = models.ImageField("Фото", upload_to="photos/")
    caption = models.CharField("Подпись", max_length=255, blank=True)

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def __str__(self):
        return self.caption or f"Фото #{self.pk}"


class Video(models.Model):
    title = models.CharField("Название видео", max_length=255)
    youtube_id = models.CharField("YouTube ID", max_length=50)
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField("Дата добавления", default=timezone.now)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def __str__(self):
        return self.title


class SiteConfig(models.Model):
    key = models.CharField("Техническое название", max_length=100, unique=True)
    title = models.CharField("Название настройки", max_length=255)
    value = models.TextField("Значение (RU)", blank=True)
    value_en = models.TextField("Значение (EN)", blank=True)

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"

    def __str__(self):
        return self.title

class NewsBlock(models.Model):
    TEXT = "text"
    IMAGE = "image"
    TYPES = [
        (TEXT, "Текст"),
        (IMAGE, "Фото"),
    ]

    news = models.ForeignKey("News", related_name="blocks", on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(default=1)
    block_type = models.CharField(max_length=10, choices=TYPES, default=TEXT)

    text = models.TextField(blank=True)
    image = models.ImageField(upload_to="news/blocks/", blank=True, null=True)

    class Meta:
        ordering = ["order"]

    def clean(self):
        # минимальная валидация по типу
        if self.block_type == self.TEXT and not self.text:
            from django.core.exceptions import ValidationError
            raise ValidationError({"text": "Для текстового блока нужен текст."})
        if self.block_type == self.IMAGE and not self.image:
            from django.core.exceptions import ValidationError
            raise ValidationError({"image": "Для фото-блока нужна картинка."})

class SiteSettings(models.Model):
    not_found_image = models.ImageField(upload_to="site/", blank=True, null=True)
    hero_autoplay_delay = models.PositiveSmallIntegerField(
        "Время смены новостей в слайдере (сек.)",
        default=8,
        help_text="Интервал автоперелистывания в секундах.",
    )
    university_url = models.URLField("Сайт университета", blank=True)
    smedia_url = models.URLField("Сайт С-Медиа", blank=True)

    def __str__(self):
        return "Site settings"
