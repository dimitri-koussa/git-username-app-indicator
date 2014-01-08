#!/usr/bin/python

# based of indicator-cpuspeed.py (2012 Charl P. Botha)

from gi.repository import Gtk, GLib

import commands
import sys
import os

try: 
       from gi.repository import AppIndicator3 as AppIndicator  
except:  
       from gi.repository import AppIndicator

import re

class GitUsernameAppIndicator:
    def __init__(self):
        image_path = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Git-Icon-White.png"
        self.ind = AppIndicator.Indicator.new(
                            "git-username-app-indicator",
                            image_path,
                            AppIndicator.IndicatorCategory.APPLICATION_STATUS);
        self.ind.set_status (AppIndicator.IndicatorStatus.ACTIVE)

        self.menu = Gtk.Menu()

        item = Gtk.MenuItem()
        item.set_label("This menu item does nothing but is required")
        item.show()
        self.menu.append(item)

        self.menu.show()
        self.ind.set_menu(self.menu)

        self.update_git_su_status()
        GLib.timeout_add_seconds(2, self.handler_timeout)

    def get_git_su(self):
        return commands.getstatusoutput("git config user.name")[1];

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

    ind = GitUsernameAppIndicator()
    ind.main()
