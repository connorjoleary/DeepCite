from bs4 import BeautifulSoup
# from selenium import webdriver
import requests
import re

#TODO This should handle multiple links in one citation or no links, right now it sends the first link
def wiki(url, parent):
    """ If the url is a cite_note and the parent is wikipedia, then link to where the citenote links to
    """
    url = url.replace("note","ref")
    if url.startswith("#cite_ref"):

        #Request wiki page and parse it
        html = requests.get(parent)
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
            try:
                target_link = links[linkdict[link] + 1]
            except IndexError:
                return
            if '#cite' not in target_link:
                if target_link[:6] == "/wiki/":
                    target_link = "https://en.wikipedia.org" + target_link
                return target_link

    elif url[:6] == "/wiki/":
        return "https://en.wikipedia.org" + url
    
    return url
