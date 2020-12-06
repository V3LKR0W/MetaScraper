from flask import Flask, jsonify, request
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
        try:
            raw = requests.get(url, headers=usr_agent).text
            soup = bs(raw, 'lxml')
            Response = {
                'pageURL': '',
                'pageTitle': '',
                'pageDescription': '',
                'pageOG:image': '',
            }
            
            Response['pageURL'] = str(url)
            
            for v in soup.find_all('title'):
                if v.text == '':
                    Response['pageTitle'] = 'N/A'
                else:
                    Response['pageTitle'] = v.text  
                
            for v in soup.find_all('meta',{'name':'description'}):
                if v.content == '':
                    Response['pageDescription'] = 'N/A'
                else:
                    Response['pageDescription'] = v['content']
                    
            for v in soup.find_all('meta',{'property':'og:image'}):
                if v.content == '':
                    Response['pageOG:image'] = 'N/A'
                else:
                    Response['pageOG:image'] = v['content']
                
                
        except Exception:
            return jsonify({'Error':'Could not establish a connection to target domain'})
        
        return Response


@app.route('/', methods=['GET'])
def index():
    return 'Nothing at the moment.'


@app.route('/preview', methods=['GET'])
def preview():
    url = request.args.get('url')
    if url == '':
        return jsonify({'Error':'No target specified'})
    else:
        return MetaScraper.get_preview(url, useragent=None)



if __name__ == '__main__':
    app.run()