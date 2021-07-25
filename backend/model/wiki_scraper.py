from bs4 import BeautifulSoup
# from selenium import webdriver
import requests
import re

#TODO This could be better, but right now it isn't broken so...
def wiki(url, parent):
    """ If the url is a cite_note and the parent is wikipedia, then link to where the citenote links to
    """
    session = requests.Session()
    if url[:10] =="#cite_note":
        url = url.replace("note","ref")

        #Request wiki page and parse it
        html = session.post(parent)
        bsObj = BeautifulSoup(html.text, "html.parser")
        findReferences = bsObj.find('ol', {'class': 'references'})
        href = BeautifulSoup(str(findReferences), "html.parser")

        # Find all links in the page
        links = [a["href"] for a in href.find_all("a", href=True)]

        # Make a dict with the key as the link and the value as num
        linkdict = {}
        for i,link in enumerate(links):
            linkdict[link] = i
        # Get the number at the end of the cite_note
        url_match = url.split('-')[-1]

        # Only include the links with the cite_note number
        cand_link = [link for link in links if ('_' + url_match + '-') in link or url == link ]

        for link in cand_link:
            target_link = links[linkdict[link] + 1]
            if '#cite' not in target_link:
                if target_link[:6] == "/wiki/":
                    target_link = "https://en.wikipedia.org" + target_link
                return target_link
