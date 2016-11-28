# -*- coding: utf-8 -*-
"""
Created on Fri May 22 15:38:13 2015

@author: rakitin
"""

from collections import OrderedDict, Counter
from xml.etree import ElementTree as ET
import shelve

from .tanachconstants import *
from .tanachXML import *

__all__ = ['TanachBooks']


class TanachBooks:
    def __init__(self,
                 books=None,
                 root=TANACH_PATH,
                 ext=".xml"):
        with shelve.open('tanachshelf') as tanachshelf:
            if ('idx' in tanachshelf):
                self.idx = tanachshelf['idx']
            else:
                self.idx = TanachIdx()
                tanachshelf['idx'] = self.idx
        if (isinstance(books, list)):
            book_names = [self.idx.get_book_name(book) for
                          book in self.books]
            file_names = [self.idx.idx_by_name[book].filename
                          for book in self.book_names]
        elif (books is None):
            book_names = self.idx.list_book_names()
            file_names = self.idx.list_book_filenames()
        else:
            raise ValueError("Argument 'books' must be None or a list of "
                             "strings.")
        paths = ["".join([root, file_name, ext]) for
                 file_name in file_names]
#        self.trees = OrderedDict((name, TanachXML(path)) for name, path in
#                                 zip(book_names, paths))
        self.trees = OrderedDict()
        with shelve.open('tanachshelf') as tanachshelf:
            for name, path in zip(book_names, paths):
                if name in tanachshelf:
                    self.trees[name] = tanachshelf[name]
                else:
                    self.trees[name] = TanachXML(path)
                    tanachshelf[name] = self.trees[name]

    def print_all(self):
        print("The following books are available:\n")
        for node in self.trees.values():
            print("\n{}".format(node))

    def check_book_list(self, books):
        if (books is None):
            books = self.idx.list_book_names()
        else:
            try:
                books = [self.idx.get_book_name(book) for book in books]
            except ValueError:
                raise ValueError("Argument 'books' must be None or a list of "
                                 "strings.")
        return books

    def get_tanach_nodes(self, books=None):
        books = self.check_book_list(books)
        root = ET.Element("tanach_nodes")
        root.extend([node.tanach_node for book, node in self.trees.items()
                     if book in books])
        return root

    def iter_tanach_nodes(self, books=None):
        books = self.check_book_list(books)
        for book, node in self.trees.items():
            if (book in books):
                yield(node.tanach_node)

    def get_header_nodes(self, books=None):
        books = self.check_book_list(books)
        root = ET.Element("teiHeader_nodes")
        root.extend([node.teiHeader_node for book, node in self.trees.items()
                     if book in books])
        return root

    def iter_header_nodes(self, books=None):
        books = self.check_book_list(books)
        for book, node in self.trees.items():
            if (book in books):
                yield(node.teiHeader_node)

    def get_nodes_in_range(self, start=TORAH_START, end=TORAH_END,
                           variant="all"):
        start = self.idx.validate_cit(start)
        end = self.idx.validate_cit(end)
        if not self.idx.validate_range(start, end):
            raise ValueError("Argument start = {0} and end {0} are not a "
                             "valid range.".format(start, end))
        if (variant in VERSE_TAGS):
            tags = VERSE_TAGS[variant]
        elif (isinstance(variant, list) and
              set(variant).issubset(VERSE_TAGS["all"])):
            tags = variant
        else:
            raise ValueError("Argument 'variant' must be a list with all "
                             "elements in {0}.".format(VERSE_TAGS["all"]))
        book_names = list(self.trees.keys())
        start_book_idx = book_names.index(start.book)
        end_book_idx = book_names.index(end.book)
        books = book_names[start_book_idx:(end_book_idx + 1)]
        root = ET.Element("range_nodes")
        for b in self.iter_tanach_nodes(books):
            book = ET.SubElement(root, b.find(".//name").text, b.attrib)
            book.text = b.text
            for c in b.iter('c'):
                if (not((b.find(".//name").text == start.book) and
                        int(c.get("n")) < start.chapter or
                        (b.find(".//name").text == end.book and
                        int(c.get("n")) > end.chapter))):
                    chapter = ET.SubElement(book, c.tag, c.attrib)
                    chapter.text = c.text
                    for v in c.iter("v"):
                        if (not((b.find(".//name").text == start.book and
                                int(c.get("n")) == start.chapter and
                                int(v.get("n")) < start.verse) or
                                (b.find(".//name").text == end.book and
                                 int(c.get("n")) == end.chapter and
                                 int(v.get("n")) > end.verse))):
                            verse = ET.SubElement(chapter, v.tag, v.attrib)
                            verse.attrib = v.attrib
                            verse.text = v.text
                            for w in v:
                                if (w.tag in tags):
                                    word = ET.SubElement(verse, w.tag,
                                                         w.attrib)
                                    word.text = w.text
        return root

    def get_str_in_range(self, start=TORAH_START, end=TORAH_END,
                         variant="ketiv", xpath=".//v/*",
                         letters=ALL_TANACH_CHARS):
        root = self.get_nodes_in_range(start, end, variant)
        if (not set(VERSE_TAGS[variant]).issubset(VERSE_TAGS["words"])):
            raise ValueError("Acceptable variants include 'w', 'k', and 'q' "
                             "tags only.")
        if (not set(letters).issubset(ALL_TANACH_CHARS)):
            raise ValueError("Argument 'letters' must be a subset of {0}."
                             .format(ALL_TANACH_CHARS))
        s = ''.join([n.text for n in root.iterfind(xpath)])
        t = str.maketrans({c: None for c in
                           set(ALL_TANACH_CHARS) - set(letters)})
        return s.translate(t)

    def count_str_in_range(self, start=TORAH_START, end=TORAH_END,
                           variant="ketiv", xpath=".//v/*",
                           letters=ALL_TANACH_CHARS):
        s = self.get_str_in_range(start, end, variant, xpath, letters)
        return Counter(s)

    def gematria(self, text):
        if (not set(text).issubset(HEBREW_LETTERS)):
            raise ValueError("Gematria only defined for the set of Hebrew "
                             "letters: {0}.".format(HEBREW_LETTERS))
        return sum([GEMATRIA[l] for l in text])

    def gematria_in_range(self, variant, start=TORAH_START, end=TORAH_END):
        if (variant not in ["ketiv", "qere"]):
            raise ValueError("Acceptable variants are 'ketiv' or 'qere' only.")
        cnt = self.count_str_in_range(start, end, variant=variant,
                                      letters=HEBREW_LETTERS)
        return sum([GEMATRIA[l]*cnt[l] for l in cnt.keys()])

    def count_nodes(self, nodes, xpath=".//v/*"):
        cnt = Counter(n.tag for n in nodes.iterfind(xpath))
        return cnt

    def count_nodes_in_range(self, start=TORAH_START, end=TORAH_END,
                             variant="all", xpath=".//v/*"):
        root = self.get_nodes_in_range(start, end, variant)
        return self.count_nodes(root, xpath)

# end of file
