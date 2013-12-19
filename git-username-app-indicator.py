#!/usr/bin/python

# based of indicator-cpuspeed.py (2012 Charl P. Botha)

from gi.repository import Gtk, GLib

import commands
import sys
import os
import pygtk
pygtk.require('2.0')

try: 
       from gi.repository import AppIndicator3 as AppIndicator  
except:  
       from gi.repository import AppIndicator

import re

class IndicatorCPUSpeed:
    def __init__(self):
        image_path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Git-Icon-White.png"
        self.ind = AppIndicator.Indicator.new(
                            "indicator-cpuspeed", 
                            image_path,
                            AppIndicator.IndicatorCategory.APPLICATION_STATUS);
        self.ind.set_status (AppIndicator.IndicatorStatus.ACTIVE)

        self.menu = Gtk.Menu()

        item = Gtk.MenuItem()
        item.set_label("Enter git su...")
        item.connect("activate", self.pop_up_text_entry)
        item.show()
        self.menu.append(item)

        self.menu.append(Gtk.SeparatorMenuItem())

        item = Gtk.MenuItem()
        item.set_label("Yesterday's developers")
        item.connect("activate", self.pop_up_text_entry)
        item.show()
        self.menu.append(item)

        self.menu.show()
        self.ind.set_menu(self.menu)

        self.update_git_su_status()
        GLib.timeout_add_seconds(2, self.handler_timeout)

    def get_git_su(self):
        return commands.getstatusoutput("git config user.name")[1];

    def handler_menu_exit(self, evt):
        Gtk.main_quit()

    def handle_text_entry(self):
        text = entry.get_text()
        print('text: ' + text)

    def pop_up_text_entry(self, evt):
        window = Gtk.Window(Gtk.WINDOW_TOPLEVEL)
        window.set_size_request(200, 100)
        window.set_title("GTK Entry")
        window.connect("delete_event", lambda w,e: Gtk.main_quit())

        vbox = Gtk.VBox(False, 0)
        window.add(vbox)
        vbox.show()

        entry = Gtk.Entry()
        entry.set_max_length(50)
        entry.connect("activate", self.handle_text_entry, entry)
        entry.set_text("hello")
        entry.insert_text(" world", len(entry.get_text()))
        entry.select_region(0, len(entry.get_text()))
        vbox.pack_start(entry, True, True, 0)
        entry.show()

    def handler_timeout(self):
        self.update_git_su_status()
        return True

    def update_git_su_status(self):
        self.ind.set_label(' ' + self.get_git_su(), "40 character limit .....................")

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    ind = IndicatorCPUSpeed()
    ind.main()
