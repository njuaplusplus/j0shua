#!/usr/bin/python
# coding=utf-8

from hymns.models import *
from django.contrib.auth.models import User

origin_key_id = {'11': '#Fm', '10': 'Bm', '13': 'Fm', '12': 'Dm', '15': 'bE', '14': 'bB', '16': 'Unknown', '1': 'C', '3': 'E', '2': 'D', '5': 'G', '4': 'F', '7': 'B', '6': 'A', '9': 'Em', '8': 'Am'}

def init_hymn_keyDB():
    # for key in origin_key_id.values():
    for key in ('C', 'D', 'E', 'F', 'G', 'A', 'B', 'Am', 'Em', 'Bm', '#Fm', 'Dm', 'Fm', 'bB', 'bE', 'Unknown'):
        Hymn_Key.objects.get_or_create(key_name=key)
    print('init_hymn_keyDB Done!')

def init_hymnsDB():
    ''' Initialize the Hymns table.

    This needs the origin_key_id dict and the initialized Hymn_Key table.
    '''
    with open('hymns/hymn_data') as inFile:
        for line in inFile:
            tmpa = line.strip().split(',')
            hymn_key = Hymn_Key.objects.get(key_name=origin_key_id[tmpa[3]].strip())
            Hymn.objects.get_or_create(hymn_index=tmpa[1].strip(), hymn_name=tmpa[2].strip(), hymn_key=hymn_key, hymn_uploader=User.objects.get(username='aplusplus'), hymn_isCandidate=False)

def init_weekly_hymnDB():
    import datetime
    origin_hymn_id = {}
    with open('hymns/hymn_data') as inFile:
        for line in inFile:
            tmpa = line.strip().split(',')
            origin_hymn_id[tmpa[0].strip()] = tmpa[2].strip()
    with open('hymns/weekly_hymn_data') as inFile:
        for line in inFile:
            tmpa = line.strip().split(',')
            hymn_name = origin_hymn_id[tmpa[-1].strip()]
            hymn = Hymn.objects.get(hymn_name=hymn_name)
            Weekly_Hymn.objects.get_or_create(hymn_date=datetime.date(int(tmpa[1]),int(tmpa[2]),int(tmpa[3])), hymn_order=tmpa[4], hymn_place=Worship_Location.objects.get(pk=1), hymn=hymn)
    print('init_weekly_hymnDB Done!')

def restore_weekly_hymnDB():
    import datetime
    data = ['2014,04,04,1,1,99',
            '2014,04,04,2,1,42',
            '2014,04,04,3,1,28',
            '2014,04,12,1,1,59',
            '2014,04,12,2,1,89',
            '2014,04,12,3,1,18',
            '2014,04,19,1,1,69',
            '2014,04,19,2,1,90',
            '2014,04,19,3,1,11',
            '2014,05,10,1,1,23',
            '2014,05,10,2,1,65',
            '2014,05,10,3,1,31',
            '2014,05,31,1,1,50',
            '2014,05,31,2,1,2',
            '2014,05,31,3,1,55',
            '2014,09,07,1,1,109',
            '2014,09,07,2,1,27',
            '2014,09,07,3,1,110',
            '2014,09,14,1,1,31',
            '2014,09,14,2,1,112',
            '2014,09,14,3,1,42',
            '2014,09,21,1,2,69',
            '2014,09,21,2,2,52',
            '2014,09,21,3,2,36',
            '2014,09,21,1,1,113',
            '2014,09,21,2,1,82',
            '2014,09,21,3,1,114']
    for l in data:
        tmpa = l.strip().split(',')
        Weekly_Hymn.objects.create(hymn_date=datetime.date(int(tmpa[0]),int(tmpa[1]), int(tmpa[2])), hymn_order=tmpa[3],  hymn_place=Worship_Location.objects.get(pk=tmpa[4]), hymn=Hymn.objects.get(pk=tmpa[5]))
    print("restore_weekly_hymnDB Done!")

def add_hymn_score(rootDir=r'/Users/aplusplus/Desktop/MusicScores/'):
    img_extensions = {".jpg", ".png", ".gif"}
    import os
    from django.core.files import File
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path):
            (hymn_index, hymn_name) = lists.split('.')
            hymn_index = int(hymn_index)
            hymn = Hymn.objects.get(hymn_index=hymn_index, hymn_name=hymn_name)
            for f in os.listdir(path):
                if not f[0] == '.' and any(f.endswith(ext) for ext in img_extensions) and f.startswith(hymn_name):
                    # print hymn.hymn_name, f
                    with open(os.path.join(path, f)) as inFile:
                        hymn.hymn_score.save(f, File(inFile))
                        hymn.hymn_score_uploader_name = 'aplusplus'
                        hymn.save()

def add_hymn_audio(rootDir=r'/Users/aplusplus/Desktop/MusicScores/'):
    import os
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path):
            (hymn_index, hymn_name) = lists.split('.')
            hymn_index = int(hymn_index)
            hymn = Hymn.objects.get(hymn_index=hymn_index, hymn_name=hymn_name)
            for f in os.listdir(path):
                if not f[0] == '.' and f.endswith('txt') and f.startswith(hymn_name):
                    # print hymn.hymn_name, f
                    with open(os.path.join(path, f)) as inFile:
                        hymn.hymn_audio = inFile.readline().strip()
                        hymn.hymn_audio_uploader_name = 'aplusplus'
                        hymn.save()

def initAll():
    init_hymn_keyDB()
    init_hymnsDB()
    init_weekly_hymnDB()
    print('initAll Done!')
