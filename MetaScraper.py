from flask import Flask, jsonify, request, render_template, url_for
import requests, random, string, base64, tldextract
from dblogic import *
from Crawler import *
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
    # Example data crawling
    post = getPost('pics', 20)
    video = getVideo('edm', 20)
    pdata = MetaScraper.get_preview(post, useragent=None)
    vdata = MetaScraper.get_preview(video, useragent=None)
    # Compacting Post Data
    title = pdata['pageOG:title']
    description = pdata['pageDescription']
    url = pdata['pageURL']
    img = pdata['pageOG:image']
    source = pdata['pageDomain']
    #Compacting Video Data
    video_title = vdata['pageOG:title']
    video_description = vdata['pageDescription']
    video_url = vdata['pageURL']
    video_video = vdata['pageOG:video']
    video_source = vdata['pageDomain']
    
    return render_template('index.html',
                           title=title, description=description, url=url, img=img, source=source,
                           video_title=video_title, video_description=video_description, video_url=video_url, video_source=video_source, video_video=video_video,
                           )



if __name__ == '__main__':
    app.run()