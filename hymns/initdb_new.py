#!/usr/bin/python
# coding=utf-8

from hymns.models import *

origin_key_id = {'11': '#Fm', '10': 'Bm', '13': 'Fm', '12': 'Dm', '15': 'bE', '14': 'bB', '16': 'Unknown', '1': 'C', '3': 'E', '2': 'D', '5': 'G', '4': 'F', '7': 'B', '6': 'A', '9': 'Em', '8': 'Am'}

def init_hymn_keyDB():
    for key in origin_key_id.values():
        Hymn_Key.objects.get_or_create(key_name=key)
    print 'init_hymn_keyDB Donw!\n'

def get_hymns_dict():
    with open('hymns/hymn_data') as inFile:
        for line in inFile:
            tmpa = line.strip().split(',')
            hymn_key = Hymn_Key.objects.get(key_name=origin_key_id[tmpa[3]].strip())
            Hymn.objects.get_or_create(hymn_index=tmpa[1].strip(), hymn_name=tmpa[2].strip(), hymn_key=hymn_key)
