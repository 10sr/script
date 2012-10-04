#!/usr/bin/env python3

import os
from types import MethodType
try :
    import shoutcast as sc
except ImportError :
    sc = None
# try :
#     from mpg123 import MPG123, MPG123A
# except ImportError :
#     MPG123 = None
#     MPG123A = None
try :
    from mplayc import MPLAYC, MPLAYCA
except ImportError :
    MPLAYCA = None

class Controller() :
    player = None

    status = ""

    def __init__(self) :
        if MPLAYC :
            self.player = MPLAYC()

    def cmd(self, args) :
        print(args[0])
        f = getattr(self, args[0], None)
        if isinstance(f, MethodType) \
                and args[0] != "cmd" \
                and args[0] != "__init__" :
            f(args)
        else :
            self.status = "%s: Command not found." % args[0]

    def ls(self, args) :
        def not_hidden(f) :
            return not f.startswith(".")

        lst = os.listdir()
        self.status = "\n".join(filter(not_hidden, lst))

    def cd(self, args) :
        try :
            if args == "" :
                args = os.path.expanduser("~/")
            os.chdir(args[1])
            self.status = args[1]
        except OSError :
            self.status = "OSERROR"

    def add(self, args) :
        self.player.add(args[1:])
        self.status = "Added :\n" + "\n".join(args[1:])

    def new(self, args) :
        self.player.new(args[1:])
        self.status = "New playlist :\n" + "\n".join(args[1:])

    def play(self, args) :
        self.player.play(args[1:])
        self.status = "Player terminated."

    def set(self, args) :
        d = {}
        for p in args[1:] :
            d[p] = True
        self.player.set(**d)
        self.status = "Property " + " ".join(args[1:]) + " is set."

    def list(self, args) :
        self.status = "Playlist :\n" + "\n".join(self.player.plist)

    def shoutcast(self, args) :
        m = sc.get_media_from_words(" ".join(args))
        if m :
            self.play(m)
            self.status = "Player terminated."
        else :
            self.status = "Url not found."

    def help(self, args) :
        self.status = "Available commands are :\n"

class ControllerA(Controller) :
    def __init__(self, pipepath, pidfile) :
        if MPLAYCA :
            self.player = MPLAYCA(pipepath, pidfile)

    def play(self, args) :
        self.player.play(args[1:])
        self.status = self.player.status

    def volumeup(self, args) :
        self.player.volume(1)

    def volumedown(self, args) :
        self.player.volume(-1)

    def stop(self, args) :
        self.player.stop()
        self.status = self.player.status

    def pp(self, args) :
        self.player.playpause()
        self.status = self.player.status