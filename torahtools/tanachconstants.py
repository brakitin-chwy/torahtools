# -*- coding: utf-8 -*-
"""
Created on Tue May 26 21:16:13 2015

@author: rakitin

Provides various classes and constants used by other torahtools files.
"""


from collections import namedtuple

BookInfo = namedtuple('BookInfo',
                      ['name', 'abbrev', 'filename', 'chapters', 'verses'])

BibleCit = namedtuple('BibleCit', ['book', 'chapter', 'verse'])

TORAH_START = BibleCit(book='Genesis', chapter=1, verse=1)

TORAH_END = BibleCit(book='Deuteronomy', chapter=34, verse=12)

HEBREW_LETTERS = "אבגדהוזחטיכךלמםנןסעפףצץקרשת"

ALL_TANACH_CHARS = 'וצךץ֟שֹ֣֩ע֑גֲֻֽ֕֒פנ֤֠ףרֱֿ֨לבםהֶ֦֘זס֖֡/ֺּ֛֜֓אק֥ ֝מיַ֔ד֮ן֙\u200dֳִֵכ׀ְ֗ׄ׃תׁׂ֞טָ֪֧֚־ח'  # @IgnorePep8

GEMATRIA = {
    'א': 1,
    'ב': 2,
    'ג': 3,
    'ד': 4,
    'ה': 5,
    'ו': 6,
    'ז': 7,
    'ח': 8,
    'ט': 9,
    'י': 10,
    'ך': 20,
    'כ': 20,
    'ל': 30,
    'ם': 40,
    'מ': 40,
    'ן': 50,
    'נ': 50,
    'ס': 60,
    'ע': 70,
    'ף': 80,
    'פ': 80,
    'ץ': 90,
    'צ': 90,
    'ק': 100,
    'ר': 200,
    'ש': 300,
    'ת': 400}

TANACH_PATH = "http://www.tanach.us/Books/"

TORAH_BOOKS = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]

PROPHETS_BOOKS = ['Joshua', 'Judges', '1 Samuel', '2 Samuel', '1 Kings',
                  '2 Kings', 'Isaiah', 'Jeremiah', 'Ezekiel', 'Hosea',
                  'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum',
                  'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi']

WRITINGS_BOOKS = ['1 Chronicles', '2 Chronicles', 'Psalms', 'Job', 'Proverbs',
                  'Ruth', 'Song of Songs', 'Ecclesiastes', 'Lamentations',
                  'Esther', 'Daniel', 'Ezra', 'Nehemiah']

ALL_BOOKS = TORAH_BOOKS + PROPHETS_BOOKS + WRITINGS_BOOKS

VERSE_TAGS = {"all": ["w", "q", "k", "samekh", "pe", "reversednun", "x"],
              "ketiv": ["w", "k"],
              "qere": ["w", "q"],
              "words": ["w", "q", "k"],
              "nonotes": ["w", "q", "k", "samekh", "pe", "reversednun"]
              }

__all__ = ["BookInfo",
           "BibleCit",
           "TORAH_START",
           "TORAH_END",
           "HEBREW_LETTERS",
           "ALL_TANACH_CHARS",
           "GEMATRIA",
           "TANACH_PATH",
           "TORAH_BOOKS",
           "PROPHETS_BOOKS",
           "WRITINGS_BOOKS",
           "ALL_BOOKS",
           "VERSE_TAGS"]

# end of file
