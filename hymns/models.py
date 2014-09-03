from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Hymn_Key(models.Model):
    key_name = models.CharField(max_length=10)
    def __unicode__(self):
        return  self.key_name

class Hymn(models.Model):
    hymn_index = models.IntegerField(default=0)
    hymn_name = models.CharField(max_length=1000)
    hymn_key = models.ForeignKey(Hymn_Key)
    hymn_score = models.ImageField(upload_to='scores/%Y/%m/%d')
    hymn_audio = models.CharField(max_length=1000, null=True, blank=True)
    hymn_lyrics = models.CharField(max_length=1000, null=True, blank=True)
    hymn_pdf = models.FileField(upload_to='pdfs/%Y/%m/%d', null=True, blank=True)
    hymn_ppt = models.FileField(upload_to='ppts/%Y/%m/%d', null=True, blank=True)
    hymn_uploader = models.ForeignKey(User)
    hymn_score_uploader_name = models.CharField(max_length=100, null=True, blank=True)
    hymn_audio_uploader_name = models.CharField(max_length=100, null=True, blank=True)
    hymn_lyrics_uploader_name = models.CharField(max_length=100, null=True, blank=True)
    hymn_pdf_uploader_name = models.CharField(max_length=100, null=True, blank=True)
    hymn_ppt_uploader_name = models.CharField(max_length=100, null=True, blank=True)
    def __unicode__(self):
        return self.hymn_name

class Weekly_Hymn(models.Model):
    hymn_date = models.DateField('Hymn Date')
    hymn_order = models.IntegerField()
    hymn = models.ForeignKey(Hymn)
    def __unicode__(self):
        return "%s_%s" % (self.hymn_date, self.hymn.hymn_name)

class Candidate_Hymn(models.Model):
    hymn_index = models.IntegerField(default=0)
    hymn_name = models.CharField(max_length=1000)
    hymn_key = models.ForeignKey(Hymn_Key)
    hymn_score = models.ImageField(upload_to='tmp_scores/%Y/%m/%d')
    hymn_audio = models.CharField(max_length=1000, null=True, blank=True)
    hymn_lyrics = models.CharField(max_length=1000, null=True, blank=True)
    hymn_pdf = models.FileField(upload_to='pdfs/%Y/%m/%d', null=True, blank=True)
    hymn_ppt = models.FileField(upload_to='ppts/%Y/%m/%d', null=True, blank=True)
    hymn_uploader = models.ForeignKey(User)
    hymn_score_uploader_name = models.CharField(max_length=100, null=True, blank=True)
    hymn_audio_uploader_name = models.CharField(max_length=100, null=True, blank=True)
    hymn_lyrics_uploader_name = models.CharField(max_length=100, null=True, blank=True)
    hymn_pdf_uploader_name = models.CharField(max_length=100, null=True, blank=True)
    hymn_ppt_uploader_name = models.CharField(max_length=100, null=True, blank=True)
    def __unicode__(self):
        return self.hymn_name
