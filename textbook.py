#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gettext import gettext as _
from book import cBook
from book import cPage
from book import cOption


def tutorial_book():

    mybook = cBook(_("How to use Adventure Book"))
    mybook.set_license(_("CC-BY"))

    p1 = cPage(_("What are Adventure Books?"))
    mybook.add_page(p1)
    p1.set_text(_("""Adventure Books are books that allow the reader to
choose between different alternatives. Every page in an Adventure Book
offers several options and depending on your choice the story follows
in different directions.

You can read an existing Adventure Book and if you want you can modify
it and distribute among your friends. Or you can create a new Adventure
Book from scratch."""))

    p2 = cPage(_("How can I read an Adventure Book?"))
    mybook.add_page(p2)
    p2.set_text(_("""To read an Adventure Book, first load it from the
journal. A cover page with the title and author are displayed. You can 
press the 'Start reading' button to go to the first page.

Every page has a text and one or more buttons with different choices.
When you press a button, you go to the page corresponding to that option.
If you want, you can go back to the first page with the button 'Start from
the beginning'."""))

    p3 = cPage(_("How can I create an Adventure Book?"))
    mybook.add_page(p3)
    p3.set_text(_("""Adventure Books can be created with the 'New book'
button. Introduce the title, your name, and choose a license. (A license
is a legal term that declares if you want your book to be copied
and shared; please read more about licenses in the Creative Commons web
page.)

Press the 'Edit book contents' button to enter the text of your book. You
have to create the pages for your book; for every page you have to add a
title and a text, and then create as many options as choices you want to
give the reader in that particular page. For every option, you have to
define to which page the story is going to jump. Please give every page
a different title so you won't get confused. If you want the story to
jump to a page you haven't created yet, don't worry, you can define it
later."""))

    p4 = cPage(_("How can I modify an Adventure Book?"))
    mybook.add_page(p4)
    p4.set_text(_("""All Adventure Books can be modified. You simply select
the 'Edit book contents' button and you can edit and modify all the pages in
the book. After you're done, it's good to use the 'Check book for missing parts'
button to verify that your book is correct; if there is an error it will show
you where the problem is so you can correct it."""))

    p5 = cPage(_("Credits"))
    mybook.add_page(p5)
    p5.set_text(_("""Authors:
Gabriel Eirea <geirea@gmail.com>
Ignacio Rodriguez <nachoel01@gmail.com>
Thanks to: Flavio Danesse <fdanesse@gmail.com>

¡Thanks for using this program! :)
 
To continue create an empty book!"""))

    o1 = cOption(_("How to read"),p2)
    o2 = cOption(_("How to create"), p3)
    o3 = cOption(_("How to modify"), p4)
    o4 = cOption(_("Credits"), p5)
    p1.add_option(o1)
    p1.add_option(o2)
    p1.add_option(o3)
    p1.add_option(o4)

    o4 = cOption(_("Return"), p1)
    p2.add_option(o4)
    p3.add_option(o4)
    p4.add_option(o4)
    p5.add_option(o4)

    return mybook


def empty_book():

    mybook = cBook(_("Title"))
    mybook.set_license(_("CC-BY"))

    p1 = cPage(_("First page"))
    op = cOption(_("Return"), mybook)
    p1.add_option(op)
    mybook.add_page(p1)

    return mybook


def credits_book():

    mybook = cBook(_("Credits"))
    p1 = cPage(_("Credits"))
    p1.set_text(_("""Authors:
Gabriel Eirea <geirea@gmail.com>
Ignacio Rodriguez <nachoel01@gmail.com>
Thanks to: Flavio Danesse <fdanesse@gmail.com>

¡Thanks for use this program! :)
 
To continue create a empty book!"""))
    mybook.add_page(p1)
    return mybook


def print_text_book(mybook):

    print "TITLE: " + mybook.get_title()
    print "AUTHOR: " + mybook.get_author()
    print "LICENSE: " + mybook.get_license()
    print

    for p in mybook.get_pages():
        print "PAGE: " + p.get_title()
        print p.get_text()
        for o in p.get_options():
            print "-> " + o.get_text()
        print


if __name__ == "__main__":

    mybook = tutorial_book()
    print_text_book(mybook)






