from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from math import ceil


def wikiRequest(query: str = None):
    # https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard
    webpage = urlopen('https://fr.wikipedia.org/wiki/%s' % (query if query else 'Sp%C3%A9cial:Page_au_hasard')).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    return soup


def getPageTitle(wikiRequest: BeautifulSoup):
    title = wikiRequest.find('title').getText()
    title = title.split('—')[0].strip()
    return title


def getHyperLinks(page: BeautifulSoup):
    return page.findAll('a', attrs={'href': re.compile("^/wiki/[^:]+$"), 'title': re.compile("[\S\s]+[\S]+.*(?<!c])$")})


def pagination(lists, page, maxItems):
    return {
        "items": lists[slice(maxItems * (page - 1), page * maxItems)],
        "lastItem": lists[len(lists) - 1],
        "prev": False if page == 1 else True,
        "next": False if (page * maxItems) >= len(lists) else True,
        "page": page,
        "maxPage": ceil(len(lists) / maxItems)
    }
