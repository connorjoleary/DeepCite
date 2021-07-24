from bs4 import BeautifulSoup
# from selenium import webdriver
import requests
import re


def wiki(url, parent):
    session = requests.Session()
    if url[:10] =="#cite_note":
        url = url.replace("note","ref")

        html = session.post(parent)
        bsObj = BeautifulSoup(html.text, "html.parser")
        findReferences = bsObj.find('ol', {'class': 'references'})
        href = BeautifulSoup(str(findReferences), "html.parser")
        links = [a["href"] for a in href.find_all("a", href=True)]

        linkdict = {}
        for i,link in enumerate(links):
            linkdict[link] = i

        url_match = url.split('-')[-1]
        cand_link = [link for link in links if ('_' + url_match + '-') in link or url == link ]
        for link in cand_link:
            target_link = links[linkdict[link] + 1]
            if '#cite' not in target_link:
                if target_link[:6] == "/wiki/":
                    target_link = "https://en.wikipedia.org" + target_link
                return target_link
