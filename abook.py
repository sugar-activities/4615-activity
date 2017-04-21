#!/usr/bin/env python
# -*- coding: utf-8 -*-
# abook.py

# Copyright 2012 Gabriel Eirea 
# Copyright 2012 Ignacio Rodríguez

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

# Contact information:

# Gabriel Eirea geirea@gmail.com
# ceibalJAM! ceibaljam.org

# Ignacio Rodríguez  nachoel01@gmail.com
# ceibalJAM! ceibaljam.org

import json

from gettext import gettext as _
import gtk

from sugar import profile
from sugar import mime
from sugar.activity import activity
from sugar.activity.widgets import StopButton
from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import ToolbarButton
from sugar.graphics.icon import Icon
from sugar.graphics.colorbutton import ColorToolButton
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.objectchooser import ObjectChooser
from sugar.graphics.alert import Alert, NotifyAlert
import pango
from ayuda import HelpButton as Ayuda
from book import cBook
from book import cPage
from book import cOption
from textbook import tutorial_book
from textbook import empty_book
from textbook import credits_book
from Toolbars import Text_Toolbar
from Toolbars import Write_Toolbar
from Toolbars import Read_Toolbar
from Toolbars import Color_Toolbar
from Toolbars import Ayuda
import Toolbars
EventBox = gtk.EventBox()

class AdventureBookActivity(activity.Activity):

    def __init__(self, handle):
	activity.Activity.__init__(self, handle, True)
	toolbarbox = ToolbarBox()
	self._main_view = gtk.VBox()

	EventBox.add(self._main_view)
## CONNECTS ##
	Toolbars.restart_button.connect("clicked", self._restart_button_cb)
	Toolbars.reading_button.connect("clicked", self._read_button_cb)
	Toolbars.load_button.connect("clicked", self._load_button_cb)
	#Toolbars.credits.connect("clicked", self.Credits)
	Toolbars.new_button.connect("clicked", self._new_button_cb)
	Toolbars.book_button.connect("clicked", self._edit_book_button_cb, Toolbars.ColorLetra.get_color())
	Toolbars.page_button.connect("clicked", self._edit_page_button_cb, EventBox)
	Toolbars.check_button.connect("clicked", self._check_button_cb, Toolbars.ColorLetra.get_color())
	Toolbars.ColorLetra.set_title(_('Select color for font and go to home page'))
	Toolbars.ColorLetra.connect('notify::color', self.Home)	
	Toolbars.ColorFondo.set_title(_('Select color for page and go to home page'))
	Toolbars.ColorFondo.connect('notify::color', self.Home)	
	Toolbars.Fonts.connect('change_selection', self.Home)
	Toolbars.Title_Tam.connect('change_selection', self.Home)
	Toolbars.ColorTitle.set_title(_('Select color for title and go to home page'))
	Toolbars.ColorTitle.connect('notify::color', self.Home)
	Toolbars.tutorial.connect("clicked", self.Tutorial)
# FIN DE CONNECTS #

	# The Activity Button:
	activity_button = ActivityToolbarButton(self)

    # Insert the Activity Toolbar Button in the toolbarbox
	toolbarbox.toolbar.insert(activity_button, 0)
	toolbarbox.toolbar.insert(gtk.SeparatorToolItem(), -1)
	Read_Toolbar(toolbarbox)
	Write_Toolbar(toolbarbox)
	Text_Toolbar(toolbarbox)
	Color_Toolbar(toolbarbox)

	Separador = gtk.SeparatorToolItem()
	Separador.props.draw = False
	Separador.set_expand(True)
	toolbarbox.toolbar.insert(Separador, -1)
	Ayuda(toolbarbox)
	# Stop button
	stopbtn = StopButton(self)
	toolbarbox.toolbar.insert(stopbtn, -1)

	# Set toolbar box
	self.set_toolbar_box(toolbarbox)

	# Define main view as a vbox container

	EventBox.modify_bg(gtk.STATE_NORMAL, Toolbars.ColorFondo.get_color())
	self.set_canvas(EventBox)
	
	# Empty Book
	self._book = empty_book()
	self._start_book(Toolbars.ColorLetra.get_color())

    def Home(self, widget, pspec):
	self._restart_button_cb(None)
	EventBox.modify_bg(gtk.STATE_NORMAL, Toolbars.ColorFondo.get_color())
    def _clean_main_view(self):

        for w in self._main_view.get_children():
            self._main_view.remove(w)


    def _start_book(self, Color):
	Tam = pango.FontDescription(Toolbars.Fonts.get_active_text())
	Title = pango.FontDescription(Toolbars.Title_Tam.get_active_text())
	Color_ts = Toolbars.ColorTitle.get_color()
	self._clean_main_view()
        title_label = gtk.Label(self._book.get_title())
        title_label.modify_fg(gtk.STATE_NORMAL, Color_ts)
	title_label.modify_font(Title)
	title_label.show()
        author_label = gtk.Label(self._book.get_author())
        author_label.modify_fg(gtk.STATE_NORMAL, Color)
	author_label.show()
	author_label.modify_font(Tam)
        license_label = gtk.Label(self._book.get_license())
        license_label.modify_fg(gtk.STATE_NORMAL, Color)
	license_label.show()
	license_label.modify_font(Tam)
        start_button = gtk.Button(_("Start reading"))
        start_button.connect('clicked', self._start_button_cb)
        
        self._main_view.pack_start(title_label)
        self._main_view.pack_start(author_label)
        self._main_view.pack_start(license_label)
        self._main_view.pack_start(start_button)

        self.show_all()

        self._current_page = self._book.get_pages()[0]


    def _start_button_cb(self, widget):

        self._current_page = self._book.get_pages()[0]
        self._show_page(Toolbars.ColorLetra.get_color())


    def _restart_button_cb(self, widget):

        self._start_book(Toolbars.ColorLetra.get_color())


    def _read_button_cb(self, widget):

        self._show_page(Toolbars.ColorLetra.get_color())


    def _show_page(self, Color):
        self._clean_main_view()
	Tam = pango.FontDescription(Toolbars.Fonts.get_active_text())
	Title = pango.FontDescription(Toolbars.Title_Tam.get_active_text())
	Color_ts = Toolbars.ColorTitle.get_color()
	print Tam
        title_label = gtk.Label(self._current_page.get_title())
        title_label.modify_fg(gtk.STATE_NORMAL, Color_ts)
	title_label.show()
	title_label.modify_font(Title)
        
        text_label = gtk.Label(self._current_page.get_text())
        text_label.modify_fg(gtk.STATE_NORMAL, Color)
	text_label.show()
	text_label.modify_font(Tam)
        
        self._main_view.pack_start(title_label)
        self._main_view.pack_start(text_label)

        for o in self._current_page.get_options():
            o_button = gtk.Button(o.get_text())
            o_button.connect('clicked', self._option_button_cb, o)
            self._main_view.pack_start(o_button)

        self.show_all()


    def _option_button_cb(self, widget, option):
        self._current_page = option.get_page()
        self._show_page(Toolbars.ColorLetra.get_color())
    def _load_button_cb(self, widget):

        chooser = ObjectChooser(parent=self)
        result = chooser.run()
        if result == gtk.RESPONSE_ACCEPT:
        	try:
	    		jobject = chooser.get_selected_object()
            		_file_path = str(jobject.get_file_path())
            		self.read_file(_file_path)
			alerta = NotifyAlert(10)
			alerta.props.title = _('Good!')
			alerta.props.msg = _('Book loaded')
			alerta.connect('response', lambda w, i: self.remove_alert(w))
			self.add_alert(alerta)
        	except IOError:
			alerta = NotifyAlert(10)
			alerta.props.title = 'Error'
			alerta.props.msg = _('Error in load book')
			alerta.connect('response', lambda w, i: self.remove_alert(w))
			self.add_alert(alerta)
	else:
            return


    def _new_button_cb(self, widget):

        self._book = empty_book()
        self._start_book(Toolbars.ColorLetra.get_color())
	EventBox.modify_bg(gtk.STATE_NORMAL, Toolbars.ColorFondo.get_color())

#        self._start_button_cb(widget)


    def Credits(self, widget):
	self._book = tutorial_book() #credits_book()
        self._start_book(Toolbars.ColorLetra.get_color())
	EventBox.modify_bg(gtk.STATE_NORMAL, Toolbars.ColorFondo.get_color())


    def Tutorial(self, widget):
	self._book = tutorial_book()
	self._start_book(Toolbars.ColorLetra.get_color())
	EventBox.modify_bg(gtk.STATE_NORMAL, Toolbars.ColorFondo.get_color())


    def _edit_book_button_cb(self, widget, Color):
	Tam = pango.FontDescription('8')
	Col = gtk.gdk.Color('#ff0000')
	EventBox.modify_bg(gtk.STATE_NORMAL, Col)

        self._clean_main_view()

        header_label = gtk.Label(_("Edit book properties"))
	header_label.modify_font(Tam)
        header_label.modify_fg(gtk.STATE_NORMAL, Color)
        self._main_view.pack_start(header_label)
        
        title_hbox = gtk.HBox()
        title_label = gtk.Label(_("Book title"))
	title_label.modify_font(Tam)
        title_label.modify_fg(gtk.STATE_NORMAL, Color)
        
        title_hbox.pack_start(title_label)
        title_entry = gtk.Entry()
        title_entry.set_text(self._book.get_title())
        title_entry.connect("changed", self._title_changed_cb)
        title_hbox.pack_start(title_entry)
        self._main_view.pack_start(title_hbox)

        author_hbox = gtk.HBox()
        author_label = gtk.Label(_("Book author"))
	author_label.modify_font(Tam)
        author_label.modify_fg(gtk.STATE_NORMAL, Color)
        author_hbox.pack_start(author_label)
        author_entry = gtk.Entry()
        author_entry.set_text(self._book.get_author())
        author_entry.connect("changed", self._author_changed_cb)
        author_hbox.pack_start(author_entry)
        self._main_view.pack_start(author_hbox)

        license_hbox = gtk.HBox()
        license_label = gtk.Label(_("Book license"))
	license_label.modify_font(Tam)
        license_label.modify_fg(gtk.STATE_NORMAL, Color)
        license_hbox.pack_start(license_label)
        license_combo = gtk.combo_box_new_text()
        license_combo.append_text(_("CC-BY"))
        license_combo.append_text(_("CC-BY-SA"))
        license_combo.append_text(_("CC-BY-NC"))
        license_combo.append_text(_("CC-BY-NC-SA"))
        license_combo.append_text(_("Copyright"))
        license_tree_model = license_combo.get_model()
        # next loop is to set the right entry in the combo
        for i in license_tree_model:
            license_combo.set_active_iter(i.iter)
            if self._book.get_license() == license_combo.get_active_text():
                break
        license_combo.connect("changed", self._license_changed_cb)
        license_hbox.pack_start(license_combo)
        self._main_view.pack_start(license_hbox)

        self.show_all()


    def _title_changed_cb(self, w):
	EventBox.modify_bg(gtk.STATE_NORMAL, Toolbars.ColorFondo.get_color())
        self._book.set_title(w.get_text())


    def _author_changed_cb(self, w):
	EventBox.modify_bg(gtk.STATE_NORMAL, Toolbars.ColorFondo.get_color())
        self._book.set_author(w.get_text())


    def _license_changed_cb(self, w):
	EventBox.modify_bg(gtk.STATE_NORMAL, Toolbars.ColorFondo.get_color())
        self._book.set_license(w.get_active_text())


    def _edit_page_button_cb(self, widget,Caja):
        self._clean_main_view()
        page_hbox = gtk.HBox()
        list_vbox = gtk.VBox()
        page_vbox = gtk.VBox()
        page_list_model = gtk.ListStore(str)
        Col =  gtk.gdk.Color("#FF0000")
        Caja.modify_bg(gtk.STATE_NORMAL, Col)
        for p in self._book.get_pages():
            page_list_model.append([p.get_title()])
        page_list_view = gtk.TreeView(model=page_list_model)
        page_list_view.get_selection().set_mode(gtk.SELECTION_SINGLE)
        page_list_view.connect("cursor-changed", 
                               self._page_selected_for_edition_cb,
                               page_vbox, Toolbars.ColorLetra.get_color())
        page_list_view.set_cursor(0) # need to change to point to page
        page_list_column = gtk.TreeViewColumn(_("Book pages"))
        page_list_view.append_column(page_list_column)
        page_list_cell = gtk.CellRendererText()
        page_list_column.pack_start(page_list_cell)
        page_list_column.add_attribute(page_list_cell, 'text', 0)

        add_page_button = gtk.Button(_("Add page"))
        add_page_button.connect("clicked", self._add_page_button_cb,
                                page_list_model, page_list_view)
        remove_page_button = gtk.Button(_("Remove page"))
        remove_page_button.connect("clicked", self._remove_page_button_cb,
                                page_list_model, page_list_view)

        list_vbox.pack_start(page_list_view)
        list_vbox.pack_start(add_page_button)
        list_vbox.pack_start(remove_page_button)

        page_hbox.pack_start(list_vbox)
        page_hbox.pack_start(page_vbox)

        self._main_view.pack_start(page_hbox)

        self.show_all()


    def _add_page_button_cb(self, w, page_list_model, page_list_view):

        new_page = cPage(_("New page"))
        self._book.add_page(new_page)
        page_list_model.append([new_page.get_title()])
        # TODO: seleccionar nueva pagina
        page_list_view.set_cursor(-1)


    def _remove_page_button_cb(self, w, page_list_model, page_list_view):

        selection = page_list_view.get_selection()
        treemodel, treeiter = selection.get_selected()
        page_title = treemodel.get_value(treeiter, 0)
        # next loop is to retrieve page from title
        selected_page = None
        for p in self._book.get_pages():
            if p.get_title() == page_title:
                selected_page = p
                break
        if selected_page == None:
            print "ERROR: couldn't find page " + page_title

        # before remove, check that no option points to it!!!!!!!!
        pointed_to = False
        for p in self._book.get_pages():
            for o in p.get_options():
                if o.get_page() == selected_page:
                    pointed_to = True
        if pointed_to:
            # error: can't remove
            print "Can't remove"
            return
        
        # ... and add confirmation?

        self._book.remove_page(selected_page)
        page_list_model.remove(treeiter)
        # TODO: seleccionar nueva pagina
        page_list_view.set_cursor(0)


    def _page_selected_for_edition_cb(self, w, page_vbox, Color):
	Tam = pango.FontDescription('10')

        for ch in page_vbox.get_children():
            page_vbox.remove(ch)

        selection = w.get_selection()
        treemodel, treeiter = selection.get_selected()
        page_title = treemodel.get_value(treeiter, 0)
        # next loop is to retrieve page from title
        selected_page = None
        for p in self._book.get_pages():
            if p.get_title() == page_title:
                selected_page = p
                break

        if selected_page == None:
            print "ERROR: couldn't find page " + page_title

        title_hbox = gtk.HBox()
        title_label = gtk.Label(_("Page title"))
	title_label.modify_font(Tam)
        title_label.modify_fg(gtk.STATE_NORMAL, Color)
        title_hbox.pack_start(title_label)
        title_entry = gtk.Entry()
        title_entry.set_text(selected_page.get_title())
        title_entry.connect("changed", self._page_title_changed_cb, 
                            p, treemodel, treeiter)
        title_hbox.pack_start(title_entry)
        page_vbox.pack_start(title_hbox)

        text_hbox = gtk.HBox()
        text_label = gtk.Label(_("Page text"))
	text_label.modify_font(Tam)
        text_label.modify_fg(gtk.STATE_NORMAL, Color)
        text_hbox.pack_start(text_label)
        text_entry = gtk.TextBuffer()
        text_entry_view = gtk.TextView(text_entry)
        text_entry.set_text(selected_page.get_text())
        text_entry.connect("changed", self._page_text_changed_cb, 
                            selected_page, treemodel, treeiter)
        text_hbox.pack_start(text_entry_view)
        page_vbox.pack_start(text_hbox)

        options_vbox =gtk.VBox()
        option_label = gtk.Label(_("Options"))
	option_label.modify_font(Tam)
        option_label.modify_fg(gtk.STATE_NORMAL, Color)
        options_vbox.pack_start(option_label)
        page_options = selected_page.get_options()
        for o in page_options:
            option_hbox = gtk.HBox()
            remove_button = gtk.Button(_("Remove"))
            remove_button.connect("clicked", self._remove_option_button_cb,
                                  selected_page, o, option_hbox)
            option_hbox.pack_start(remove_button)
            option_entry = gtk.Entry()
            option_entry.set_text(o.get_text())
            option_entry.connect("changed", self._option_text_changed_cb,
                                 o)
            option_hbox.pack_start(option_entry)
            page_dest_combo = gtk.combo_box_new_text()
            for p in self._book.get_pages():
                page_dest_combo.append_text(p.get_title())
            page_dest_tree_model = page_dest_combo.get_model()
            # next loop is to set the right entry in the combo
            for i in page_dest_tree_model:
                page_dest_combo.set_active_iter(i.iter)
                if o.get_page().get_title() == \
                        page_dest_combo.get_active_text():
                    break
            page_dest_combo.connect("changed", self._page_dest_changed_cb,
                                    o)
            option_hbox.pack_start(page_dest_combo)
            options_vbox.pack_start(option_hbox)

        option_hbox = gtk.HBox()
        add_button = gtk.Button(_("Add option"))
        add_button.connect("clicked", self._add_option_button_cb,
                           selected_page, option_hbox, options_vbox)
        option_hbox.pack_start(add_button)
        options_vbox.pack_start(option_hbox)

        page_vbox.pack_start(options_vbox)

        page_vbox.show_all()


    def _page_title_changed_cb(self, w, p, treemodel, treeiter):
	print w
        p.set_title(w.get_text(w.get_start_iter(),w.get_end_iter()))
        treemodel.set_value(treeiter, 0, w.get_text(w.get_start_iter(),w.get_end_iter()))


    def _page_text_changed_cb(self, w, p, treemodel, treeiter):
	print w
        p.set_text(w.get_text(w.get_start_iter(),w.get_end_iter()))


    def _option_text_changed_cb(self, w, option):

        option.set_text(w.get_text())


    def _remove_option_button_cb(self, w, page, option, option_hbox):

        page.remove_option(option)
        option_hbox.get_parent().remove(option_hbox)


    def _add_option_button_cb(self, w, page, option_hbox, options_vbox):
	Tam = pango.FontDescription('10')

        w.get_parent().remove(w)

        new_option = cOption(_("Text"), self._book.get_pages()[0])
        page.add_option(new_option)

        remove_button = gtk.Button(_("Remove"))
        remove_button.connect("clicked", self._remove_option_button_cb,
                              page, new_option, option_hbox)
        option_hbox.pack_start(remove_button)
        option_entry = gtk.Entry()
        option_entry.set_text(new_option.get_text())
        option_entry.connect("changed", self._option_text_changed_cb,
                             new_option)
        option_hbox.pack_start(option_entry)
        page_dest_combo = gtk.combo_box_new_text()
        for p in self._book.get_pages():
            page_dest_combo.append_text(p.get_title())
        page_dest_tree_model = page_dest_combo.get_model()
        # next loop is to set the right entry in the combo
        for i in page_dest_tree_model:
            page_dest_combo.set_active_iter(i.iter)
            if new_option.get_page().get_title() == \
                    page_dest_combo.get_active_text():
                break
        page_dest_combo.connect("changed", self._page_dest_changed_cb,
                                new_option)
        option_hbox.pack_start(page_dest_combo)
        option_hbox.show_all()

        option_new_hbox = gtk.HBox()
        add_button = gtk.Button(_("Add option"))
        add_button.connect("clicked", self._add_option_button_cb,
                           page, option_new_hbox, options_vbox)
        option_new_hbox.pack_start(add_button)
        options_vbox.pack_start(option_new_hbox)
        options_vbox.show_all()


    def _page_dest_changed_cb(self, w, option):

        for p in self._book.get_pages():
            if p.get_title() == w.get_active_text():
                option.set_page(p)
                break


    def _check_button_cb(self, widget, Color):
	Tam = pango.FontDescription('10')

        self._clean_main_view()
        # check that all pages are referenced
        everything_ok = True
        for p1 in self._book.get_pages():
            pointed_to = False
            for p in self._book.get_pages():
                for o in p.get_options():
                    if o.get_page() == p1:
                        pointed_to = True
            if not pointed_to:
                print "Page "+ p1.get_title() + " not referenced"
                msg_label = gtk.Label("Error: Page '"+ p1.get_title() + 
                                      "' not referenced from any other page")
                msg_label.modify_fg(gtk.STATE_NORMAL, Color)
		msg_label.modify_font(Tam)
                self._main_view.pack_start(msg_label)
                everything_ok = False
        # check that all pages have different names
        for p1 in self._book.get_pages():
            for p in self._book.get_pages():
                if p1.get_title() == p.get_title() and p1 != p:
                    msg_label = gtk.Label("Error: Page title '"+ p1.get_title() + 
                                          "' is not unique")
                    msg_label.modify_fg(gtk.STATE_NORMAL, Color)
		    msg_label.modify_font(Tam)
                    self._main_view.pack_start(msg_label)
                    everything_ok = False

        if everything_ok:
            msg_label = gtk.Label(_("Everything is OK"))
	    msg_label.modify_font(Tam)
            msg_label.modify_fg(gtk.STATE_NORMAL, Color)
            self._main_view.pack_start(msg_label)
      
        self._main_view.show_all()


    def write_file(self, file_path):

        jfile = open(file_path, "w")

        pages_props = []
        for p in self._book.get_pages():
            options_props = []
            for o in p.get_options():
                options_props.append({'text': o.get_text(),
                                      'page': o.get_page().get_title()})
            pages_props.append({'title': p.get_title(),
                                'text': p.get_text(),
                                'options': options_props})
        book_props = {'title': self._book.get_title(),
                      'author': self._book.get_author(),
                      'license': self._book.get_license(),
                      'pages': pages_props}

        try:
            json.dump(book_props, jfile)
        finally:
            jfile.close()


    def read_file(self, file_path):

        jfile = open(file_path, "r")

        try:
            book_props = json.load(jfile)
        finally:
            jfile.close()

        self._book = cBook(book_props['title'])
        self._book.set_author(book_props['author'])
        self._book.set_license(book_props['license'])
        page_list = book_props['pages']
        for p in page_list:
            page_props = cPage(p['title'])
            page_props.set_text(p['text'])
            self._book.add_page(page_props)
        for p in page_list:
            for o in p['options']:
                page_dest = None
                page_orig = None
                for pp in self._book.get_pages():
                    if pp.get_title() == o['page']:
                        page_dest = pp
                    if pp.get_title() == p['title']:
                        page_orig = pp
                if page_dest == None or page_orig == None:
                    print(_("Error while loading file"))
                option_props = cOption(o['text'], page_dest)
                page_orig.add_option(option_props)

        self._start_book(Toolbars.ColorLetra.get_color())


