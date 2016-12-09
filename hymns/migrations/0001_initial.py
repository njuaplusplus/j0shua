# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hymn',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('hymn_index', models.IntegerField(default=0, verbose_name='编号')),
                ('hymn_name', models.CharField(verbose_name='歌名', max_length=1000)),
                ('hymn_score', models.ImageField(help_text='必须上传', verbose_name='歌谱', upload_to='scores/%Y/%m/%d')),
                ('hymn_audio', models.CharField(verbose_name='音频', blank=True, null=True, help_text='可不填写', max_length=1000)),
                ('hymn_lyrics', models.CharField(verbose_name='歌词', blank=True, null=True, help_text='可不填写', max_length=1000)),
                ('hymn_pdf', models.FileField(blank=True, null=True, upload_to='pdfs/%Y/%m/%d', help_text='可不填写', verbose_name='PDF 文件')),
                ('hymn_ppt', models.FileField(blank=True, null=True, upload_to='ppts/%Y/%m/%d', help_text='可不填写', verbose_name='PPT 文件')),
                ('hymn_score_uploader_name', models.CharField(verbose_name='歌谱上传者', blank=True, null=True, help_text='若修改了歌谱文件, 请填写你的名字', max_length=100)),
                ('hymn_audio_uploader_name', models.CharField(verbose_name='音频上传者', blank=True, null=True, help_text='若修改了音频文件, 请填写你的名字', max_length=100)),
                ('hymn_lyrics_uploader_name', models.CharField(verbose_name='歌词上传者', blank=True, null=True, help_text='若修改了歌词文件, 请填写你的名字', max_length=100)),
                ('hymn_pdf_uploader_name', models.CharField(verbose_name='PDF 上传者', blank=True, null=True, help_text='若修改了 PDF 文件, 请填写你的名字', max_length=100)),
                ('hymn_ppt_uploader_name', models.CharField(verbose_name='PPT 上传者', blank=True, null=True, help_text='若修改了 PPT 文件, 请填写你的名字', max_length=100)),
                ('hymn_isCandidate', models.BooleanField(default=False, verbose_name='是否候选')),
            ],
        ),
        migrations.CreateModel(
            name='Hymn_Key',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('key_name', models.CharField(verbose_name='曲调', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Weekly_Hymn',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('hymn_date', models.DateField(verbose_name='敬拜日期')),
                ('hymn_order', models.IntegerField(verbose_name='敬拜顺序')),
                ('hymn_pdf', models.FileField(blank=True, null=True, upload_to='pdfs/%Y/%m/%d', help_text='可不填写', verbose_name='PDF 文件')),
                ('hymn_ppt', models.FileField(blank=True, null=True, upload_to='ppts/%Y/%m/%d', help_text='可不填写', verbose_name='PPT 文件')),
                ('hymn_pdf_uploader_name', models.CharField(verbose_name='PDF 上传者', blank=True, null=True, help_text='若修改了 PDF 文件, 请填写你的名字', max_length=100)),
                ('hymn_ppt_uploader_name', models.CharField(verbose_name='PPT 上传者', blank=True, null=True, help_text='若修改了 PPT 文件, 请填写你的名字', max_length=100)),
                ('hymn', models.ForeignKey(to='hymns.Hymn', verbose_name='诗歌')),
            ],
        ),
        migrations.CreateModel(
            name='Worship_Location',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(verbose_name='地点', max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='weekly_hymn',
            name='hymn_place',
            field=models.ForeignKey(to='hymns.Worship_Location', verbose_name='地点'),
        ),
        migrations.AddField(
            model_name='hymn',
            name='hymn_key',
            field=models.ForeignKey(to='hymns.Hymn_Key', verbose_name='曲调'),
        ),
        migrations.AddField(
            model_name='hymn',
            name='hymn_uploader',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='诗歌上传者'),
        ),
    ]
