#!/usr/bin/python
# coding=utf-8
from musics.models import Music_Key, Music, Score
import os

mkeyDict = {}

def initMusic_KeyDB():
    for key in ('C', 'D', 'E', 'F', 'G', 'A', 'B', 'Am', 'Em', 'Bm', '#Fm', 'Dm', 'Fm', 'bB', 'bE', 'Unknown'):
        Music_Key(key_name=key).save()
    print 'initMusic_KeyDB Done!\n'

def readMusicNamesFiles(file_name):

    if not os.path.exists(file_name):
        print "%s doesn't exist" % file_name
        return
    f = file(file_name)
    while True:
        line = f.readline().rstrip().split(',')
        line = [x.strip() for x in line]
        if len(line) < 5:
            break
        if len(line[0]) > 0:
            key_name = line[0]
        # print key_name
        for music_name in line[1:]:
            if len(music_name) > 0:
                # print music_name
                mkeyDict[music_name] = key_name

def initMusic_ScoreDB(rootDir, music):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        # print path
        if os.path.isdir(path):
            (music_index, music_name) = lists.split('.')
            music_index = int(music_index)
            print '%d--%s' % (music_index, music_name)
            if lists in mkeyDict:
                music_key = Music_Key.objects.get(key_name=mkeyDict[lists])
            else:
                music_key = Music_Key.objects.get(key_name='Unknown')
            music = Music.objects.get_or_create(music_index=music_index, music_name=music_name, music_key=music_key)[0]
            initMusic_ScoreDB(path, music)
        elif not lists[0] == '.':
            print lists
            if not music.score_set.filter(score_name=lists):
                music.score_set.create(score_name=lists, score_url=lists)

def initAudioDB(rootDir, music):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        # print path
        if os.path.isdir(path):
            (music_index, music_name) = lists.split('.')
            music_index = int(music_index)
            print '%d--%s' % (music_index, music_name)
            music = Music.objects.get(music_index=music_index, music_name=music_name)
            initAudioDB(path, music)
        elif not lists[0] == '.':
            # print lists
            if lists.endswith("txt") and not music.audio_set.filter(audio_name=lists):
                f = file(path)
                lineno = 1
                lyric = []
                while True:
                    line = f.readline()
                    audio_url = line.strip()
                    break
#                     if len(line) == 0: # Zero length indicates EOF
#                         break
#                     line = line.strip()
#                     if lineno == 1:
#                         audio_url = line
#                         lineno = 0
#                     elif len(line) > 0:
#                         lyric.append(line)
                    #print line,
                    # Notice comma to avoid automatic newline added by Python
                f.close() # close the file
#                music.audio_set.create(audio_name=lists, audio_url=audio_url,lyric='\n'.join(lyric))
                # No lyrics at first
                music.audio_set.create(audio_name=lists, audio_url=audio_url, lyric='Nothing')

def rebuildAll():
    initMusic_KeyDB()
    readMusicNamesFiles('/Users/aplusplus/Projects/eclipse/RetrieveMusicScores/musicNames.csv')
    initMusic_ScoreDB('/Users/aplusplus/Projects/eclipse/RetrieveMusicScores/MusicScores', None)
