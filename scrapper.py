import urllib.request
import urllib.parse
from bs4 import BeautifulSoup


class Task:
    def __init__(self):
        self.data = []
        self.total = 0
        self.possible = 0
        self.name = ""
    data = []
    total = 0
    possible = 0
    name = ""


def Login(login, password):
    form_data = [
        ("auth", "1"),
        ("login", login),
        ("pass", password)
    ]
    login_data = urllib.parse.urlencode(form_data)

    request = urllib.request.Request("http://main.edu.pl/pl/login",
        login_data.encode("utf-8"),
        {
            "User-Agent": "Robot, source at: http://github.com/ritave/main.edu.pl-Grapher/"
        })

    login_form = urllib.request.urlopen(request)

    return login_form.info()["Set-Cookie"]


def GetContestList():
    request = urllib.request.Request("http://main.edu.pl/pl/archive",
        headers={
            "User-Agent": "Robot, source at: http://github.com/ritave/main.edu.pl-Grapher/"
        })
    out = urllib.request.urlopen(request)

    soup = BeautifulSoup(out)
    contests = soup.find_all(**{"class": "level2"})

    out = []

    for line in contests:
        out += [(line.string, line.get("href"))]

    return out


def GetCategories(link):
    link = "http://main.edu.pl/pl/" + link
    request = urllib.request.Request(link,
        headers={
            "User-Agent": "Robot, source at: http://github.com/ritave/main.edu.pl-Grapher/"
        })
    out = urllib.request.urlopen(request)

    soup = BeautifulSoup(out)
    body = soup.find(id="body")
    cats = body("a")

    out = []

    for line in cats:
        href = line.get("href")
        if href[:7] != "http://":
            out += [(line.string, href)]

    return out


def GetTasks(link, cookie):
    link = "http://main.edu.pl/pl/" + link
    request = urllib.request.Request(link,
        headers={
            "User-Agent": "Robot, source at: http://github.com/ritave/main.edu.pl-Grapher/",
            "Cookie": cookie
        })
    out = urllib.request.urlopen(request)

    soup = BeautifulSoup(out)

    total_sum = 0
    possible_sum = 0
    out = []

    row = soup("tr")
    for i in row:
        coll = i("td")
        temp = Task()
        it = coll[0]("a")
        for j in it:
            temp.name = j.string.strip()

        if temp.name != "":
            num = coll[2].string.strip()
            num = num.partition("/")
            temp.total = int(num[0][1:])
            temp.possible = int(num[2][:-1])

            # Normalize
            temp.total = int(temp.total / temp.possible * 100.0)
            temp.possible = 100

            total_sum += temp.total
            possible_sum += temp.possible

            out += [temp]

    temp = Task()
    temp.total = total_sum
    temp.possible = possible_sum
    temp.data = out
    return temp


def GetAll(cookie):
    stuff = Task()
    stuff.name = "Wszystko"

    contests = GetContestList()

    categories = []
    for c in contests:
        temp = Task()
        temp.name = c[0]

        cats = GetCategories(c[1])
        for i in cats:
            tasks = GetTasks(i[1], cookie)
            tasks.name = i[0]

            temp.data += [tasks]
            temp.total += tasks.total
            temp.possible += tasks.possible

        categories += [(c[0], cats)]

        stuff.data += [temp]
        stuff.total += temp.total
        stuff.possible += temp.possible

    return stuff
