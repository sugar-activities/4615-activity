#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Combo.py
# Extraido de CeibalNotifica
# Flavio Danesse <fdanesse@gmail.com>
import gtk
import gobject
class Combo(gtk.ComboBox):
    __gsignals__ = {"change_selection": (gobject.SIGNAL_RUN_FIRST,
    gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}
    def __init__(self):
        gtk.ComboBox.__init__(self, gtk.ListStore(str))
        cell = gtk.CellRendererText()
        self.pack_start(cell, True)
        self.add_attribute(cell, 'text', 0)
        self.show_all()
        self.connect("changed", self.emit_selection)

    def set_items(self, items):
        self.get_model().clear()

        for item in items:
            self.append_text(str(item))
        self.set_active(0)

    def emit_selection(self, widget):
        indice = widget.get_active()
        if indice < 0: return
        iter = widget.get_model().get_iter(indice)
        value = widget.get_model().get_value(iter, 0)
        self.emit("change_selection", value)

    def get_value_select(self):
        indice = self.get_active()
        if indice < 0: return None
        iter = self.get_model().get_iter(indice)
        value = self.get_model().get_value(iter, 0)
        return value
