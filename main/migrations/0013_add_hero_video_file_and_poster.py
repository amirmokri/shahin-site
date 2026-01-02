# Generated manually for video file support

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_hero_image_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='hero_video_file',
            field=models.FileField(blank=True, null=True, upload_to='site/videos/', verbose_name='فایل ویدیو تبلیغاتی (MP4)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='hero_video_poster',
            field=models.ImageField(blank=True, null=True, upload_to='site/videos/', verbose_name='تصویر پیش‌نمایش ویدیو'),
        ),
    ]

