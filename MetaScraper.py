from flask import Flask
import requests
from bs4 import BeautifulSoup as bs


app = Flask(__name__)


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
            return Response


@app.route('/', methods=['GET'])
def index():
    return 'Nothing at the moment.'


@app.route('/preview/<url>', methods=['GET'])
def preview(url):
    return MetaScraper.get_preview(f'https://{url}', useragent=None)



if __name__ == '__main__':
    app.run()