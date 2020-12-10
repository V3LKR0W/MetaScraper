from flask import Flask, jsonify, request, render_template
import requests, random, string, base64, tldextract
from dblogic import *
from bs4 import BeautifulSoup as bs


app = Flask(__name__)

@app.errorhandler(404)
def fourofour(e):
    #TODO: Make 404 page
    return 'Endpoint not found.'

@app.errorhandler(500)
def serverError(e):
    #TODO: Make internal error page.
    return 'Looks like the server hit a bump.'

@app.errorhandler(405)
def methodNotAllowed(e):
    #TODO: Make method not allowed page.
    return 'Method not allowed.'


class MetaScraper():
    def __init__(self, url, useragent):
        self.url = url
        self.useragent = useragent
        
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
            Response = {}
            
            Response['pageURL'] = str(url)
            
            Response['pageDomain'] = tldextract.extract(str(url)).domain
            
            for v in soup.find_all('title'):
                Response['pageTitle'] = v.text  
                
            for v in soup.find_all('meta',{'name':'description'}):
                Response['pageDescription'] = v['content']
              
            for v in soup.find_all('meta',{'name':'theme-color'}):
                Response['themeColor'] = v['content']  
                    
            for v in soup.find_all('meta',{'property':'og:image'}):
                Response['pageOG:image'] = v['content']
                
            for v in soup.find_all('meta', {'property':'og:video:url'}):
                Response['pageOG:video'] = v['content']
                
            for v in soup.find_all('meta', {'property':'og:title'}):
                Response['pageOG:title'] = v['content']

        except Exception as e:
            return jsonify({'Error':'Could not establish a connection to target domain'})
        
        return Response


def createKey():
    s = string.ascii_letters
    key = ''.join(random.choice(s) for length in range(20))
    return key

@app.route('/keyGen', methods=['POST'])
def keyGen():
    if request.method == 'POST':
        encode = bytes(createKey(),'utf-8')
        keygen = base64.b64encode(encode, altchars=None).decode('utf-8')
        addKey(keygen)
        return jsonify({'API_KEY':str(keygen)})
    else:
        return render_template('keygen.html')



@app.route('/api/preview', methods=['POST'])
def preview():
    key = request.form.get('key')
    url = request.form.get('url')
   
   #Key Validation
   
    if checkKey(key) == None:
        return jsonify({"Error":"Incorrect Key"})
    
    #Param validation
    
    if key == None and url == None:
        return jsonify({"Error":"Incomplete request missing 'Url' and 'Key' parameter"})
    elif url == '':
        return jsonify({"Error":"Incomplete request missing Url parameter"})
    elif key == '':
        return jsonify({"Error":"Incomplete request missing Key parameter"})
    else:
       return MetaScraper.get_preview(url, useragent='MetaScraper/HTTP/RichEmbedPreview')



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()