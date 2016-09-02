#!/usr/local/bin/python
# coding=utf-8

import requests
import urllib
import re
from . import xmltodict


def get_real_audio_url(audio_url):
    if 'mp3' in audio_url.lower():
        return audio_url
    real_audio_url = ''
    tmp = re.findall(r'zanmeishi.com/song/(\d+)\.html', audio_url)
    if len(tmp) == 1:
        # This is an url from zanmeishi.com
        audio_id = tmp[0]
        real_audio_url = "http://api.zanmeishi.com/song/p/%s.mp3" % audio_id
    else:
        match = re.search(r'xiami.com/song/(\d+)', audio_url)
        if match and len(match.groups()) > 0:
            # This is an url from xiami.com
            audio_id = match.group(1)
            real_audio_url = '/hymns/xiami/%s/' % match.group(1)
    return real_audio_url
