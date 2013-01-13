#!/usr/bin/env python
from getpass import getpass
import sqlite3
import os
import os.path

import scrapper


def PrintOut(t, depth=0):
    print('\t'*depth + t.name + " - " + str(t.total) + "/" + str(t.possible))
    for x in t.data:
        PrintOut(x, depth + 1)


my_id = 0


def Insert(c, t, parent):
    global my_id
    c.execute("INSERT INTO main_cache VALUES(?, ?, ?, ?, ?)", (
        my_id,
        t.name,
        t.total,
        t.possible,
        parent
    ))
    this_id = my_id
    for i in t.data:
        my_id += 1
        Insert(c, i, this_id)


nick = input("Twoj nick: ")
password = getpass("Twoje haslo: ")

print("Loguje...")
cookie = scrapper.Login(nick, password)

print("Sciagam internety...")
tasks = scrapper.GetAll(cookie)
#PrintOut(tasks)

if os.path.isfile("cache.db"):
    print("Usuwam stary cache...")
    os.remove("cache.db")

print("Zapisuje do cache...")
conn = sqlite3.connect("cache.db")
c = conn.cursor()
c.execute("CREATE TABLE main_cache (id INTEGER, name STRING, total INTEGER, possible INTEGER, parent INTEGER);")
Insert(c, tasks, -1)
conn.commit()
c.close()

import show
