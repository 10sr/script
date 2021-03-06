#!/usr/bin/env python3

program = "leafpad"
notepath = "~/dbx/note/note2"
#program = "open"

import os
import subprocess as sp
import sys
import fileinput
import datetime

notepath = os.path.expanduser(notepath)
trash = ".trash"

def print_list(func):
    flist = [f for f in os.listdir(notepath) \
                 if f != trash and not f.startswith(".") and \
                 not f.endswith(".html")]
    for i, f in enumerate(flist):
        i += 1
        print("%2d : %s" % (i, f))
    if func:
        ask_open(flist, func)

def ask_open(flist, func):
    s = input("Input num: ")
    if s == "":
        exit()
    else:
        func(flist[int(s) - 1])

def edit_file(filename):
    os.chdir(notepath)
    os.access(filename, os.F_OK) or os.mknod(filename, 0o644)
    if sys.platform == "darwin":
        sp.call(["open", "-e", filename])
    else:
        sp.call([program, filename])

def cat_file(filename):
    print("** %s **********" % filename)
    for l in fileinput.input(os.path.join(notepath, filename)):
        print(l, end = "")
    print("")
    print("*" * (14 + len(filename)))

def remove_file(filename):
    cat_file(filename)
    time = datetime.datetime.today().strftime("%Y-%m-%dT%H-%M-%S")
    s = input("Really remove %s? [y/N]: " % filename)
    if s == "y":
        os.rename(os.path.join(notepath, filename),
                  os.path.join(notepath, trash, filename + "." + time))

def print_help():
    b = os.path.basename(sys.argv[0])
    print("Usage: %s [e|c|rm] [file]" % b, file=sys.stderr)
    print("       %s l" % b, file=sys.stderr)
    exit(1)

def main(argv):
    if(len(argv) == 3):
        if(argv[1] == "e"):
            edit_file(argv[2])
        elif(argv[1] == "c"):
            cat_file(argv[2])
        elif(argv[1] == "rm"):
            remove_file(argv[2])
        else:
            print_help()
    elif(len(argv) == 2):
        if(argv[1] == "e"):
            print_list(edit_file)
        elif(argv[1] == "c"):
            print_list(cat_file)
        elif(argv[1] == "rm"):
            print_list(remove_file)
        elif(argv[1] == "l"):
            print_list(None)
        else:
            print_help()
    else:
        print_list(None)

if __name__ == "__main__":
    os.access(os.path.join(notepath, trash), os.W_OK) or \
        os.makedirs(os.path.join(notepath, trash), 0o755)

    main(sys.argv)
