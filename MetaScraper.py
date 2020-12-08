from flask import Flask, jsonify, request, render_template
import requests, base64, random, string
from bs4 import BeautifulSoup as bs


app = Flask(__name__)


class MetaScraper():
    def __init__(self, url, useragent):
        self.url = url
        self.useragent = useragent
        
    error = {
        'Missing'
    }
    def get_preview(url, useragent):
        if useragent == None or '':
            usr_agent = {
                'User-Agent':'HTTP/MetaScraper/DEFAULT'
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
                'themeColor': '',
                'pageOG:image': '',
                'pageOG:video': '',
            }
            
            Response['pageURL'] = str(url)
            
            for v in soup.find_all('title'):
                if v.text == '':
                    Response['pageTitle'] = error[0]
                else:
                    Response['pageTitle'] = v.text  
                
            for v in soup.find_all('meta',{'name':'description'}):
                if v.content == '':
                    Response['pageDescription'] = error[0]
                else:
                    Response['pageDescription'] = v['content']
              
            for v in soup.find_all('meta',{'name':'theme-color'}):
                if v.content == '':
                    Response['themeColor'] = error[0]
                else:
                    Response['themeColor'] = v['content']  
                    
            for v in soup.find_all('meta',{'property':'og:image'}):
                if v.content == '':
                    Response['pageOG:image'] = error[0]
                else:
                    Response['pageOG:image'] = v['content']
                
            for v in soup.find_all('meta', {'property':'og:video:url'}):
                if v.content == '':
                    Response['pageOG:video'] = error[0]
                else:
                    Response['pageOG:video'] = v['content']
                
        except Exception as e:
            return jsonify({'Error':'Could not establish a connection to target domain'})
        
        return Response


def createKey():
    s = string.ascii_letters
    key = ''.join(random.choice(s) for length in range(20))
    return key


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/keyGen', methods=['POST', 'GET'])
def keyGen():
    if request.method == 'POST':
        encode = bytes(createKey(), 'utf-8')
        keygen = base64.b64encode(encode, altchars=None)
        return jsonify({'API_KEY':str(keygen)})
    else:
        return render_template('keygen.html')



@app.route('/preview', methods=['GET'])
def preview():
    url = request.args.get('url')
    if url == '':
        return jsonify({'Error':'No target specified'})
    else:
        return MetaScraper.get_preview(url, useragent='MetaScraper/PagePreviewer')



if __name__ == '__main__':
    app.run()