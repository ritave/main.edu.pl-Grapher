#!/usr/bin/env python
import sqlite3
import os

how_long = 25


class col:
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    end = '\033[0m'


def Bar(total, possible):
    if possible != 0:
        total = int(float(total) / float(possible) * how_long)
    else:
        total = how_long

    if total < (0.25 * how_long):
        color = col.red
    elif (total < (0.60 * how_long)):
        color = col.yellow
    elif (total == how_long):
        color = col.blue
    else:
        color = col.green

    return (color + '[' + ("=" * total) + (' ' * (how_long - total)) + ']' + col.end)

if not os.path.exists("cache.db"):
    print("Pierw wlacz download.py aby sciagnac twoje wyniki")
    exit()

conn = sqlite3.connect("cache.db")

at_id = "0"
while 1:
    title = conn.execute("SELECT * FROM main_cache WHERE id=?", [at_id]).fetchone()
    print(title[1] + "  " + Bar(title[2], title[3]))

    rows = conn.execute("SELECT * FROM main_cache WHERE parent=?", [at_id]).fetchall()

    how_many = len(rows)

    longest = 0
    names = []
    for i in range(how_many):
        temp = str(i + 1) + ". " + rows[i][1]
        longest = max(longest, len(temp))
        names += [temp]
    longest += 2

    for i in range(how_many):
        print('\t' + names[i].ljust(longest) + Bar(rows[i][2], rows[i][3]))
    print("\t0. Back")

    choice = -1
    while choice < 0 or choice > how_many:
        choice = int(input("Your choice: "))

    if choice == 0:
        at_id = str(title[4])
        if (at_id == "-1"):
            break
    else:
        at_id = str(rows[choice - 1][0])
    print('\n')

conn.close()
