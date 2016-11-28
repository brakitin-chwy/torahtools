# -*- coding: utf-8 -*-
"""
Created on Wed May 27 09:38:38 2015

@author: rakitin

Defines the TanachXML base class, and TanachIdx and TanachHdr subclasses.

TanachXML provides basic html access and XML parsing of files located at
www.tanach.us/books/.

TanachIdx loads www.tanach.us/Books/TanachIndex.xml by default. It also parses
the file and stores the information as an ElementTree called idx_by_name.
Finally, a number of methods are defined that help use the index, especially
to validate biblical citations.

TanachHdr is forthcoming.
"""


from urllib.request import urlopen
from xml.etree import ElementTree as ET
from collections import OrderedDict
import re
from .tanachconstants import *  # @UnusedWildImport

__all__ = ["TanachXML",
           "TanachIdx",
           "TanachHdr"]


class TanachXML:
    def __init__(self, path):
        self.path = path
        with urlopen(self.path) as url_file:
            self.tree = ET.parse(url_file)
        self.teiHeader_node = self.tree.find("teiHeader")
        self.tanach_node = self.tree.find(".//tanach")

    def __str__(self):
        return ' '.join(["Main Title:",
                         self.teiHeader_node.find(
                          ".//title[@type='main']").text,
                         "\nFilename:",
                         self.teiHeader_node.find(
                          ".//title[@type='filename']").text,
                         "\nVersion:",
                         self.teiHeader_node.find(".//version").text,
                         "\nDate:",
                         self.teiHeader_node.find(".//date").text])

    def print_hdr_node(self):
            print(ET.tostring(self.teiHeader_node, encoding="unicode"))

    def print_tanach_node(self):
            print(ET.tostring(self.tanach_node, encoding="unicode"))


class TanachIdx(TanachXML):
    def __init__(self,
                 path=TANACH_PATH + "TanachIndex.xml"):
        TanachXML.__init__(self, path)
        self.idx_by_name = OrderedDict()
        for book in self.tanach_node.iter("book"):
            book_name = book.find(".//name").text
            book_abbrev = book.find(".//abbrev").text
            book_filename = book.find(".//filename").text
            book_chapters = int(book.find(".//cs").text)
            book_verses = [int(verse.text) for verse in book.findall(".//vs")]
            self.idx_by_name[book_name] = BookInfo(book_name,
                                                   book_abbrev,
                                                   book_filename,
                                                   book_chapters,
                                                   book_verses)

    def get_book_name(self, cit_book):
        if (type(cit_book) is not str):
            raise ValueError("Argument 'cit_book' must be a string")
        r_key = re.compile(cit_book.lower())
        book = [book for book in self.idx_by_name.keys() if
                r_key.match(book.lower())]
        if (book):
            if (len(book) == 1):
                return book[0]
            else:
                raise ValueError("Argument cit_book=(\'{0}\') yields multiple"
                                 " valid bible book names. Try a more "
                                 "specific value.".format(cit_book))
        else:
            raise KeyError("{0} is not a valid book.".format(cit_book))

    def get_book_chapters(self, cit_book):
        book = self.get_book_name(cit_book)
        return self.idx_by_name[book].chapters

    def get_chapter_verses(self, cit_book, chapter):
        book = self.get_book_name(cit_book)
        if (self.get_book_chapters(book) >= chapter):
            return self.idx_by_name[book].verses[chapter - 1]
        else:
            raise IndexError("No chapter {0} in book {1}.".format(chapter,
                             book))

    def validate_cit(self, cit):
        if (not(isinstance(cit, BibleCit) or isinstance(cit, tuple)) or
                (type(cit) is tuple and len(cit) != 3 or
                    (type(cit[0]) is not str or
                     type(cit[1]) is not int or
                     type(cit[2]) is not int))):
            raise TypeError("Argument cit must be a BibleCit, or a "
                            "tuple of a str and two ints.")
        cit = BibleCit(*cit)
        verses = self.get_chapter_verses(cit.book, cit.chapter)
        if (cit.verse > verses):
            raise IndexError("No verse {0} in chapter {1} of book {2}"
                             .format(cit.verse, cit.chapter,
                                     self.get_book_name(cit.book)))
        else:
            return BibleCit(self.get_book_name(cit.book),
                            cit.chapter, cit.verse)

    def validate_range(self, start, end):
        try:
            start = self.validate_cit(start)
        except TypeError:
            raise TypeError("Argument start must be a BibleCit, or a "
                            "tuple of a str and two ints.")
        try:
            end = self.validate_cit(end)
        except TypeError:
            raise TypeError("Argument end must be a BibleCit, or a "
                            "tuple of a str and two ints.")
        if (start.book == end.book):
            return start.chapter < end.chapter or\
                   (start.chapter == end.chapter and start.verse < end.verse)
        else:
            return list(self.idx_by_name.keys()).index(start.book) <\
                   list(self.idx_by_name.keys()).index(end.book)

    def list_book_names(self):
        book_names = list(self.idx_by_name.keys())
        return book_names

    def list_book_filenames(self):
        return [self.idx_by_name[book].filename
                for book in self.idx_by_name.keys()]

    def get_book_abbrev(self, cit_book):
        book = self.get_book_name(cit_book)
        return self.idx_by_name[book[0]].abbrev


class TanachHdr(TanachXML):
    def __init__(self,
                 path=TANACH_PATH + "TanachHeader.xml"):
        TanachXML.__init__(self, path)

# end of file
