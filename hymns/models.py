#!/usr/local/bin/python
# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from django import forms
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit
from django.utils.translation import ugettext as _

# Create your models here.


class Hymn_Key(models.Model):
    key_name = models.CharField('曲调', max_length=10)

    def __str__(self):
        return self.key_name


class Hymn(models.Model):
    hymn_index = models.IntegerField('编号', default=0)
    hymn_name = models.CharField('歌名', max_length=1000)
    hymn_key = models.ForeignKey(Hymn_Key, verbose_name='曲调')
    hymn_score = models.ImageField('歌谱', upload_to='scores/%Y/%m/%d', help_text='必须上传', null=True, blank=True)
    hymn_audio = models.CharField('音频', max_length=1000, null=True, blank=True, help_text='可不填写')
    hymn_lyrics = models.CharField('歌词', max_length=1000, null=True, blank=True, help_text='可不填写')
    hymn_pdf = models.FileField('PDF 文件', upload_to='pdfs/%Y/%m/%d', null=True, blank=True, help_text='可不填写')
    hymn_ppt = models.FileField('PPT 文件', upload_to='ppts/%Y/%m/%d', null=True, blank=True, help_text='可不填写')
    hymn_uploader = models.ForeignKey(User, verbose_name='诗歌上传者')
    hymn_score_uploader_name = models.CharField('歌谱上传者', max_length=100, null=True, blank=True, help_text='若修改了歌谱文件, 请填写你的名字')
    hymn_audio_uploader_name = models.CharField('音频上传者', max_length=100, null=True, blank=True, help_text='若修改了音频文件, 请填写你的名字')
    hymn_lyrics_uploader_name = models.CharField('歌词上传者', max_length=100, null=True, blank=True, help_text='若修改了歌词文件, 请填写你的名字')
    hymn_pdf_uploader_name = models.CharField('PDF 上传者', max_length=100, null=True, blank=True, help_text='若修改了 PDF 文件, 请填写你的名字')
    hymn_ppt_uploader_name = models.CharField('PPT 上传者', max_length=100, null=True, blank=True, help_text='若修改了 PPT 文件, 请填写你的名字')
    hymn_isCandidate = models.BooleanField('是否候选', default=False)
    hymn_compressed_score = ImageSpecField(
        source='hymn_score',
        processors=[ResizeToFit(1920, 65535, False)],
        format='JPEG',
        options={'quality': 80}
    )
    hymn_score_url = models.CharField(
        verbose_name=_('原图的七牛key'),
        help_text=_('不超过 255 个字符'),
        max_length=255,
        blank=True
    )
    hymn_compressed_score_url = models.CharField(
        verbose_name=_('1920x的七牛key'),
        help_text=_('不超过 255 个字符'),
        max_length=255,
        blank=True
    )

    def __str__(self):
        return self.hymn_name


class Worship_Location(models.Model):
    location_name = models.CharField('地点', max_length=1000)

    def __str__(self):
        return self.location_name


class Weekly_Hymn(models.Model):
    hymn_date = models.DateField('敬拜日期')
    hymn_order = models.IntegerField('敬拜顺序')
    hymn_place = models.ForeignKey(Worship_Location, verbose_name='地点')
    hymn = models.ForeignKey(Hymn, verbose_name='诗歌')
    hymn_pdf = models.FileField('PDF 文件', upload_to='pdfs/%Y/%m/%d', null=True, blank=True, help_text='可不填写')
    hymn_ppt = models.FileField('PPT 文件', upload_to='ppts/%Y/%m/%d', null=True, blank=True, help_text='可不填写')
    hymn_pdf_uploader_name = models.CharField('PDF 上传者', max_length=100, null=True, blank=True, help_text='若修改了 PDF 文件, 请填写你的名字')
    hymn_ppt_uploader_name = models.CharField('PPT 上传者', max_length=100, null=True, blank=True, help_text='若修改了 PPT 文件, 请填写你的名字')

    def __str__(self):
        return "%s_%s" % (self.hymn_date, self.hymn.hymn_name)


class Hymn_Form(forms.ModelForm):
    class Meta:
        model = Hymn
        fields = [ 'hymn_index', 'hymn_name', 'hymn_key', 'hymn_audio', 'hymn_audio_uploader_name', 'hymn_pdf', 'hymn_pdf_uploader_name', 'hymn_ppt', 'hymn_ppt_uploader_name' ]
        widgets = {
            'hymn_index' : forms.NumberInput(attrs={'class':'form-control'}),
            'hymn_name' : forms.TextInput(attrs={'class':'form-control'}),
            'hymn_key' : forms.Select(attrs={'class':'form-control'}),
            'hymn_audio' : forms.TextInput(attrs={'class':'form-control'}),
            'hymn_audio_uploader_name' : forms.TextInput(attrs={'class':'form-control'}),
            'hymn_pdf' : forms.FileInput(attrs={'class':'form-control'}),
            'hymn_pdf_uploader_name' : forms.TextInput(attrs={'class':'form-control'}),
            'hymn_ppt' : forms.FileInput(attrs={'class':'form-control'}),
            'hymn_ppt_uploader_name' : forms.TextInput(attrs={'class':'form-control'}),
        }


class Weekly_Hymn_Form(forms.ModelForm):
    class Meta:
        model = Weekly_Hymn
        fields = [ 'hymn_pdf', 'hymn_pdf_uploader_name', 'hymn_ppt', 'hymn_ppt_uploader_name' ]
