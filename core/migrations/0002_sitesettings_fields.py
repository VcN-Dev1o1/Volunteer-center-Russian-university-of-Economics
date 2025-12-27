from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="hero_autoplay_delay",
            field=models.PositiveSmallIntegerField(
                default=8,
                help_text="Интервал автоперелистывания в секундах.",
                verbose_name="Время смены новостей в слайдере (сек.)",
            ),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="smedia_url",
            field=models.URLField(blank=True, verbose_name="Сайт С-Медиа"),
        ),
        migrations.AddField(
            model_name="sitesettings",
            name="university_url",
            field=models.URLField(blank=True, verbose_name="Сайт университета"),
        ),
    ]