#!/usr/bin/python
# coding=utf-8

from hymns.models import Hymn
import os
import requests

def export_scores():
    hymns = Hymn.objects.all()
    score_directory=ur'/DjangoProject/j0shua.org/j0shua/爱的约书亚/歌谱/'
    if os.path.exists(score_directory):
        for hymn in hymns:
            if hymn.hymn_score:
                filename = u'%03d%s%s' % (hymn.id, hymn.hymn_name, hymn.hymn_score.url[-4:])
                new_filename = u'1%03d%s' % (hymn.hymn_index, filename)
                filename = os.path.join(score_directory, filename)
                new_filename = os.path.join(score_directory, new_filename)
                if not os.path.exists(new_filename):
                    if not os.path.exists(filename):
                        hymn.hymn_score.open()
                        with open(filename, 'wb') as outfile:
                            outfile.write(hymn.hymn_score.read())
                        hymn.hymn_score.close()
                        print u'%s score has saved' % hymn.hymn_name
                    os.rename(filename, new_filename)
            else:
                print u'%s has no score' % hymn.hymn_name

def export_audios():
    hymns = Hymn.objects.all()
    audio_directory=ur'/DjangoProject/j0shua.org/j0shua/爱的约书亚/歌曲/'
    if os.path.exists(audio_directory):
        for hymn in hymns:
            if hymn.hymn_audio:
                r = requests.get(hymn.hymn_audio, stream=True)
                chunk_size = 1024
                filename = u'%03d%s%s' % (hymn.id, hymn.hymn_name, hymn.hymn_audio[-4:])
                new_filename = u'1%03d%s' % (hymn.hymn_index, filename)
                filename = os.path.join(audio_directory, filename)
                new_filename = os.path.join(audio_directory, new_filename)
                if not os.path.exists(new_filename):
                    if not os.path.exists(filename):
                        with open(filename, 'wb') as fd:
                            for chunk in r.iter_content(chunk_size):
                                fd.write(chunk)
                        print u'%s audio has saved' % hymn.hymn_name
                    os.rename(filename, new_filename)
            else:
                print u'%s has no audio' % hymn.hymn_name

def rename():
    rootDir = ur'/DjangoProject/j0shua.org/j0shua/爱的约书亚/'
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path):
            for f in os.listdir(path):
                if not f[0] == '.' and not f[0] == '1':
                    old_filename = os.path.join(path, f)
                    new_filename = os.path.join(path, u'1%s' % f)
                    os.rename(old_filename, new_filename)
