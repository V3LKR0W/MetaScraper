import requests
from bs4 import BeautifulSoup as bs



class MetaScraper():
    def __init__(self, url, useragent):
        self.url = url
        self.useragent = useragent
        
    def get_preview(url, useragent):
        if useragent == None or '':
            usr_agent = {
                'User-Agent':'HTTP/MetaCrawler/DEFAULT'
            }
        else:
            usr_agent = {
                'User-Agent':str(useragent)
            }
        raw = requests.get(url, headers=usr_agent).text
        soup = bs(raw, 'lxml')
        for v in soup.find_all('meta',{'name':'description'}):
            Response = {
                'preview_description':str(v['content'])
            }
            print(Response)



#MetaScraper.get_preview('https://reddit.com', useragent=None)

