import json
import requests
from bs4 import BeautifulSoup
from wiki_scraper import wiki

def lambda_handler(event, context):
    ref2text = {}
    website = event['website']

    # is wikipedia link
    if self.parent != None and  "https://en.wikipedia.org" in self.parent.href:
        citation = wiki(self.href, self.parent.href)
        if citation == None:
            self.href = self.parent.href + self.href
            self.score = self.parent.score
            return ""
        else:
            self.href = citation
    # not wikipedia link
    else:
        # no errors
        if not self.excep_handle(): # why does this only run if not in wikipedia?
            self.score = self.parent.score
            return 

    user_agent = {'User-agent': 'Mozilla/5.0'}
    try:
        response = requests.get(, headers=user_agent, timeout=30)
    # url is trash
    except Exception as e:
        # faulty input
        if self.parent == None:
            return error.URLError('Unable to reach URL: ' + html_link(self.href))
        # create leaf
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    static = soup.findAll('p')
    print(static)

    # Exception that the child of one claim has no valid sentences, then add its parent to the leaf list.
    if len(text_raw) < 6:
        # Terminate the scraper and parse the parent node to the leaf list
        # unable to obtain infomation from website
        if self.parent == None and 'reddit.com' not in self.href:
            return error.EmptyWebsite('Unable to obtain infomation from the website.' + \
                        new_indention(html_link(self.href) + ' could contain the following errors: Error404, Error403, Error500, or content of site cannot be obtained.'))
        return

    for unit in text_raw:
        if len(unit.findAll('a')) > 0:
            for ref in unit.findAll('a'):
                try:
                    if ref['href'] != self.href:
                        ref2text[unit.text] = ref['href'] # doesn't this just take the last link in a piece of text?
                except KeyError:
                    continue
        else:
            ref2text[unit.text] = ""

    # If the claim is on reddit, the title and link of the posts are not in p tags. To get around this we read its json
    if 'reddit.com' in self.href:
        try:
            response = requests.get(self.href+'.json', headers=user_agent)
            page_info = json.loads(response.text)
        except Exception as e:
            page_info = {}
        if type(page_info) == list:
            page_info = page_info[0]

        if page_info.get('kind') == 'Listing':
            posts = page_info['data']['children']
            for post in posts:
                if post.get('kind') == 't3':
                    post = post.get('data', {})
                    if 'url' in post and 'title' in post:
                        if post['url']!= self.href:
                            ref2text[post['title']] = post['url']

    return ref2text
