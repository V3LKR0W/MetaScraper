from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import *
from keys import *
import requests, random, string, base64, tldextract
from dblogic import *
from Crawler import *
from bs4 import BeautifulSoup as bs

# Application initalization

app = Flask(__name__)
app.config['SECRET_KEY'] = flaskKeys['secret_key']

csrf = CSRFProtect(app)


# Application error handlers
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


# MetaScraper API

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
    
# Form inputs    
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    
class CreateAccount(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('retype_pw', message='Password must match')]) 
    retype_pw = PasswordField('Repeat password')
       
# Routes and Functions

def createKey():
    s = string.ascii_letters
    key = ''.join(random.choice(s) for length in range(20))
    return key

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        return 'success'
    else:
        return render_template('login.html', form=form)

@app.route('/create-account', methods=['GET', 'POST'])
def createAccount():
    form = CreateAccount()
    if request.method == 'POST' and form.validate_on_submit():
        return 'success'
    else:
        return render_template('createaccount.html', form=form)


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

@app.route('/SourceCode', methods=['GET'])
def sourceCode():
    return redirect('https://github.com/V3LKR0W/MetaScraper')

@app.route('/', methods=['GET'])
def index():
    # Example data crawling
    post = getPost('MadeMeSmile', 5)
    video = getVideo('pop music', 30)
    audio = getAudio()
    pdata = MetaScraper.get_preview(post, useragent=None)
    vdata = MetaScraper.get_preview(video, useragent=None)
    adata = MetaScraper.get_preview(audio, useragent=None)
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
    #Compacting Audio Data
    audio_title = adata['pageOG:title']
    audio_description = adata['pageDescription']
    audio_url = adata['pageURL']
    audio_audio = f'https://w.soundcloud.com/player/?url={ audio_url } '
    audio_source = adata['pageDomain']
    
    return render_template('index.html',
                           title=title, description=description, url=url, img=img, source=source,
                           video_title=video_title, video_description=video_description, video_url=video_url, video_source=video_source, video_video=video_video,
                           audio_title=audio_title, audio_description=audio_description, audio_source=audio_source, audio_audio=audio_audio, audio_url=audio_url,
                           )



if __name__ == '__main__':
    app.run(debug=True)