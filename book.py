#!/usr/bin/env python
# -*- coding: utf-8 -*-
# book.py

# Copyright 2012 Gabriel Eirea 
# geirea@gmail.com

# Copyright 2012 Ignacio Rodríguez
# nachoel01@gmail.com

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import random

class cBook(object):

    def __init__(self, title, author = '', book_license=''):
        self._title = title
        self._author = author
        self._license = book_license
        self._pages = []
        self._pageids = set()

    def set_title(self, text):
        self._title = text

    def get_title(self):
        return self._title

    def set_author(self, text):
        self._author = text

    def get_author(self):
        return self._author

    def set_license(self, text):
        self._license = text

    def get_license(self):
        return self._license

    def add_page(self, page):
        self._pages.append(page)
#        while page.get_id() in self._pageids:
#            page.set_id()
        self._pageids.add(page.get_id())

    def get_pages(self):
        return self._pages

    def remove_page(self, page):
        self._pages.remove(page)
        self._pageids.remove(page.get_id())


class cPage(object):

    def __init__(self, title, text = ''):
        self._title = title
        self._text = text
        self._options = []
        self.set_id()

    def set_title(self, text):
        self._title = text

    def get_title(self):
        return self._title

    def set_id(self):
        self._id = random.randrange(100000)

    def get_id(self):
        return self._id

    def set_text(self, text):
        self._text = text

    def get_text(self):
        return self._text

    def add_option(self, option):
        self._options.append(option)

    def get_options(self):
        return self._options

    def remove_option(self, option):
        self._options.remove(option)


class cOption(object):

    def __init__(self, text, page):
        self._text = text
        self._page = page

    def set_text(self, text):
        self._text = text

    def get_text(self):
        return self._text

    def set_page(self, page):
        self._page = page

    def get_page(self):
        return self._page

