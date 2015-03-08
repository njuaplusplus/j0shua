#!/usr/local/bin/python
# coding=utf-8

from bibles.models import *

BOOK_NAME = {
        '创世纪' : 'Genesis',
        '出埃及记' : 'Exodus',
        '利未记' : 'Leviticus',
        '民数记' : 'Numbers',
        '申命记' : 'Deuteronomy',
        '约书亚记' : 'Joshua',
        '士师记' : 'Judges',
        '路得记' : 'Ruth',
        '撒母耳记上' : '1_Samuel',
        '撒母耳记下' : '2_Samuel',
        '列王纪上' : '1_Kings',
        '列王纪下' : '2_Kings',
        '历代志上' : '1_Chronicles',
        '历代志下' : '2_Chronicles',
        '以斯拉记' : 'Ezra',
        '尼希米记' : 'Nehemiah',
        '以斯帖记' : 'Esther',
        '约伯记' : 'Job',
        '诗篇' : 'Psalms',
        '箴言' : 'Proverbs',
        '传道书' : 'Ecclesiastes',
        '雅歌' : 'Song_of_Songs',
        '以赛亚书' : 'Isaiah',
        '耶利米书' : 'Jeremiah',
        '耶利米哀歌' : 'Lamentations',
        '以西结书' : 'Ezekiel',
        '但以理书' : 'Daniel',
        '何西阿书' : 'Hosea',
        '约珥书' : 'Joel',
        '阿摩司书' : 'Amos',
        '俄巴底亚书' : 'Obadiah',
        '约拿书' : 'Jonah',
        '弥迦书' : 'Micah',
        '那鸿书' : 'Nahum',
        '哈巴谷书' : 'Habakkuk',
        '西番雅书' : 'Zephaniah',
        '哈该书' : 'Haggai',
        '撒迦利亚书' : 'Zechariah',
        '玛拉基书' : 'Malachi',
        '马太福音' : 'Matthew',
        '马可福音' : 'Mark',
        '路加福音' : 'Luke',
        '约翰福音' : 'John',
        '使徒行传' : 'Acts',
        '罗马书' : 'Romans',
        '哥林多前书' : '1_Corinthians',
        '哥林多后书' : '2_Corinthians',
        '加拉太书' : 'Galatians',
        '以弗所书' : 'Ephesians',
        '腓立比书' : 'Philippians',
        '歌罗西书' : 'Colossians',
        '帖撒罗尼迦前书' : '1_Thessalonians',
        '帖撒罗尼迦后书' : '2_Thessalonians',
        '提摩太前书' : '1_Timothy',
        '提摩太后书' : '2_Timothy',
        '提多书' : 'Titus',
        '腓利门书' : 'Philemon',
        '希伯来书' : 'Hebrews',
        '雅各书' : 'James',
        '彼得前书' : '1_Peter',
        '彼得后书' : '2_Peter',
        '约翰一书' : '1_John',
        '约翰二书' : '2_John',
        '约翰三书' : '3_John',
        '犹大书' : 'Jude',
        '启示录' : 'Revelation',
        }

def init_bible_chn():
    ''' Initialize the Bible chn table.

    '''
    lines = []
    with open('bibles/bible-chn') as inFile:
        for line in inFile:
            lines.append(line.strip().split(' ', 2))

    # make empty verse become the verse before it.
    for i in xrange(len(lines)):
        if len(lines[i]) < 3:
            lines[i].append(lines[i-1][2])
            lines[i-1] = lines[i-1][:2]
        i += 1

    for line in lines:
        book_name = line[0]
        chapternum, versenum = [int(x) for x in line[1].split(':')]
        verse = ''
        if len(line) == 3:
            verse = line[2]
        book = Bible_Book_Name.objects.get_or_create(book_name_zh=book_name,book_name_en=BOOK_NAME[book_name])[0]
        Bible_CHN.objects.get_or_create(versenum=versenum,chapternum=chapternum,book=book,verse=verse)

    # Update the chapternums of each book
    books = Bible_Book_Name.objects.all()
    for book in books:
        book.chapternums = Bible_CHN.objects.filter(book=book).values('chapternum').distinct().count()
        book.save()
    print 'init_bible_chn Done'

def init_bible_niv2011():
    ''' Initialize the Bible niv2011 table.

    '''
    lines = []
    with open('bibles/bible_niv_2011') as inFile:
        for line in inFile:
            lines.append(line.strip().split(' ', 2))

    # make empty verse become the verse before it.
    for i in xrange(len(lines)):
        if len(lines[i]) < 3:
            lines[i].append(lines[i-1][2])
            lines[i-1] = lines[i-1][:2]
        i += 1

    for line in lines:
        book_name = line[0]
        chapternum, versenum = [int(x) for x in line[1].split(':')]
        verse = ''
        if len(line) == 3:
            verse = line[2]
        book = Bible_Book_Name.objects.get(book_name_en=book_name)
        Bible_NIV2011.objects.get_or_create(versenum=versenum,chapternum=chapternum,book=book,verse=verse)

    print 'init_bible_niv2011 Done'
