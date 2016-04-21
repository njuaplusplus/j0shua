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
    tmp = re.findall('zanmeishi.com/song/(\d+)\.html', audio_url)
    if len(tmp) == 1:
        # This is an url from zanmeishi.com
        audio_id = tmp[0]
        real_audio_url = "http://api.zanmeishi.com/song/p/%s.mp3" % audio_id
    else:
        tmp = re.findall('xiami.com/song/(\d+)\?', audio_url)
        if len(tmp) == 1:
            # This is an url from xiami.com
            audio_id = tmp[0]
            real_audio_url = xiami_audio_url(audio_id)
    return real_audio_url


def xiami_audio_url(id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53',
        'Referer': 'http://www.xiami.com/song/playlist/id/' + id
    }
    url = 'http://www.xiami.com/song/playlist/id/' + id
    try:
        r = requests.get(url,headers=headers)
        r.encode='uft-8'
    except:
        return '连接虾米服务器失败'
    try:
        info = xmltodict.parse(r.text)
        songurl=info['playlist']['trackList']['track']['location']
    except:
        return '获取歌词信息失败，请检查是否有该歌曲ID'
    return xiamidecode(songurl)


def xiamidecode(location):
    num = int(location[0])
    avg_len, remainder = int(len(location[1:]) / num), int(len(location[1:]) % num)
    result = [location[i * (avg_len + 1) + 1: (i + 1) * (avg_len + 1) + 1] for i in range(remainder)]
    result.extend([location[(avg_len + 1) * remainder:][i * avg_len + 1: (i + 1) * avg_len + 1] for i in range(num-remainder)])
    url = urllib.unquote(
        ''.join([''.join([result[j][i] for j in range(num)]) for i in range(avg_len)]) +
        ''.join([result[r][-1] for r in range(remainder)])
    ).replace('^', '0')
    return url
