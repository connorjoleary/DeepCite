from bs4 import BeautifulSoup
import requests
import re

def wiki(url, parent):
    session = requests.Session()
    if url[:10] == "#cite_note":
        url = url.replace("note","ref")
        html = session.post(parent)
        bsObj = BeautifulSoup(html.text, "html.parser")
        findReferences = bsObj.find('ol', {'class': 'references'})
        href = BeautifulSoup(str(findReferences), "html.parser")
        links = [a["href"] for a in href.find_all("a", href=True)]
        print(links)
        start = len(links)
        end = 0
        for i,link in enumerate(links):
            if link == url or url[: -2] in link:
                start = i
            if i > start and link[:9] == "#cite_ref":
                end = i
                break
        corrlinks = links[start + 1 : end]
        print(corrlinks)
        for corrlink in corrlinks:
            if corrlink[:6] == "/wiki/":
                corrlink = "https://en.wikipedia.org" + corrlink
        return corrlinks
    else:
        return ["https://en.wikipedia.org" + url]


if '__main__':
    wiki("#cite_note-Burke,_pp._205–214-3", "https://en.wikipedia.org/wiki/Albert_G%C3%B6ring")