#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Toolbars.py
# Gabriel, hice esto porque es un revoltijo abook.py :P
try:
	import gtk
	import sys
	from gettext import gettext as _
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
	
	from book import cBook
	from book import cPage
	from book import cOption
	from textbook import tutorial_book
	from textbook import empty_book
	from textbook import credits_book
	from Combo import Combo
	from ayuda import HelpButton as Ayudas
except ImportError:
	print 'NO SE ESTA EN SUGAR.. SALIENDO'
	sys.exit()
Fonts = Combo()
Fonts.set_items(["Purisa 8", "Purisa 12", "Purisa 24", "Monospace 8",
		 "Monospace 12", "Monospace 24", "Times New Roman 8",
		 "Times New Roman 12", "Times New Roman 24", "FreeSans 8",
		 "FreeSans 12", "FreeSans 24"])
Title_Tam = Combo()
Title_Tam.set_items(["Purisa 8", "Purisa 12", "Purisa 24", "Monospace 8",
		     "Monospace 12", "Monospace 24", "Times New Roman 8",
		     "Times New Roman 12", "Times New Roman 24", "FreeSans 8",
		     "FreeSans 12", "FreeSans 24"])
ColorLetra = ColorToolButton()
ColorTitle = ColorToolButton()
ColorFondo = ColorToolButton()
Col = gtk.gdk.Color('#ffffff')
ColorFondo.set_color(Col)
restart_button = ToolButton("home")
reading_button = ToolButton("read")
load_button = ToolButton("open-from-journal")
#credits = ToolButton("credits")
tutorial = ToolButton("tutorial")
tutorial.set_tooltip(_("Tutorial book"))
new_button = ToolButton("new")
book_button = ToolButton("edit-p")
page_button = ToolButton("edit-c")
check_button = ToolButton("broken")


def Color_Toolbar(toolbar):
	color_button = ToolbarButton(icon_name='color-preview')
	color_toolbar = gtk.Toolbar()
	ColorContentLabel = gtk.Label(_('Text color'))
	ColorFondoLabel   = gtk.Label(_('Page color'))
	ColorTitleLabel   = gtk.Label(_('Title color'))
	# Contenido del libro
	Item = gtk.ToolItem()
	Item.add(ColorContentLabel)
	Item.show()

	color_toolbar.insert(Item, -1)
	color_toolbar.insert(ColorLetra, -1)
	color_toolbar.insert(gtk.SeparatorToolItem(), -1)

	# Fondo # 
	Item = gtk.ToolItem()
	Item.add(ColorFondoLabel)
	Item.show()

	color_toolbar.insert(Item, -1)
	color_toolbar.insert(ColorFondo, -1)
	color_toolbar.insert(gtk.SeparatorToolItem(), -1)
	
	Item = gtk.ToolItem()
	Item.add(ColorTitleLabel)
	Item.show()
	color_toolbar.insert(Item, -1)
	color_toolbar.insert(ColorTitle, -1)

	color_button.props.page = color_toolbar
	color_toolbar.show_all()
	toolbar.toolbar.insert(color_button, -1)


def Text_Toolbar(toolbar):
	text_button = ToolbarButton(icon_name="format-text-size")
	text_toolbar = gtk.Toolbar()
	A = gtk.Label(_('Content:'))	
	B = gtk.Label(_('Title:'))
	Item = gtk.ToolItem()
	Item.add(A)
	Item.show()
	text_toolbar.insert(Item, -1)
	Item = gtk.ToolItem()
	Item.add(Fonts)
	Item.show()
	text_toolbar.insert(Item, -1)
	Fonts.show()
	A.show()
	Fonts.show()
	text_toolbar.insert(gtk.SeparatorToolItem(), -1)
	Item = gtk.ToolItem()
	Item.add(B)
	Item.show()
	text_toolbar.insert(Item, -1)
	Item = gtk.ToolItem()
	Item.add(Title_Tam)
	Item.show()
	Title_Tam.show()
	
	text_toolbar.insert(Item, -1)
	text_toolbar.show_all()
	text_button.props.page = text_toolbar
	toolbar.toolbar.insert(text_button, -1)


def Read_Toolbar(toolbar):	
	# read toolbar
	read_button = ToolbarButton(icon_name="read")
	read_toolbar = gtk.Toolbar()

	
	restart_button.set_tooltip(_("Start from the begining"))
	
	read_toolbar.insert(restart_button, -1)
	
	reading_button.set_tooltip(_("Read the book"))
	
	read_toolbar.insert(reading_button, -1)
	
	load_button.set_tooltip(_("Load book from Journal"))
	
	read_toolbar.insert(load_button, -1)
	read_button.props.page = read_toolbar
	read_toolbar.show_all()
	Sep = gtk.SeparatorToolItem()
	Sep.set_expand(False)
	Sep.set_draw(True)
	read_toolbar.insert(Sep, -1)
	Sep.show()
	
	#credits.set_tooltip(_("Credits"))

	#read_toolbar.insert(credits, -1)
	read_toolbar.insert(tutorial, -1)
	tutorial.show()
	#credits.show()
	toolbar.toolbar.insert(read_button, -1)


def Write_Toolbar(toolbar):
	# write toolbar
	write_button = ToolbarButton(icon_name="edit")
	write_toolbar = gtk.Toolbar()
	
	new_button.set_tooltip(_("New book"))
	
	write_toolbar.insert(new_button, -1)
	
	book_button.set_tooltip(_("Edit book properties"))
	
	write_toolbar.insert(book_button, -1)
	
	page_button.set_tooltip(_("Edit book contents"))
	
	write_toolbar.insert(page_button, -1)
	
	check_button.set_tooltip(_("Check book for missing parts"))
	
	write_toolbar.insert(check_button, -1)
	write_button.props.page = write_toolbar
	write_toolbar.show_all()
	toolbar.toolbar.insert(write_button, -1)

	
def Ayuda(toolbar):
	Boton_Ayuda = Ayudas()
	# Porfavor, traducir esto al ingles! #
	Boton_Ayuda.add_section(_("Creating a book"))
	Boton_Ayuda.add_paragraph(_("To create a new book, click on"),'edit')
	Boton_Ayuda.add_paragraph(_("Then click on"),'new')
	Boton_Ayuda.add_section(_("Editing a book"))
	Boton_Ayuda.add_paragraph(_("To edit the book, click on"),'edit')
	Boton_Ayuda.add_paragraph(_("Then click on"),'edit-c')
	Boton_Ayuda.add_section(_("Editing the book properties"))
	Boton_Ayuda.add_paragraph(_("To edit the book properties, click on"),'edit')
	Boton_Ayuda.add_paragraph(_("Then click on"),'edit-p')
	Boton_Ayuda.add_section(_("Reading a book"))
	Boton_Ayuda.add_paragraph(_("To read a book, click on"),'read')
	Boton_Ayuda.add_paragraph(_("If you want to go to the first page, click on"),'home')
	Boton_Ayuda.add_paragraph(_("If you want to load a book from the journal, click on"),'open-from-journal')
	Boton_Ayuda.add_section(_("Editing the text style"))
	Boton_Ayuda.add_paragraph(_("To change the font size, click on"),'format-text-size')
	Boton_Ayuda.add_paragraph(_("If you want to edit the font name, click on the text box (e.g., 'Purisa 8'); a font list will be displayed. Select one."))
	Boton_Ayuda.add_paragraph(_("If you want to change the color, click on"), 'color-preview')
	Boton_Ayuda.show()
	toolbar.toolbar.insert(Boton_Ayuda, -1)
