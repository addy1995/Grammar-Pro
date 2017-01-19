from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)


textGearsKey = '' #Add TextGear Key here
wordsApiMashapeKey = '' #Add WordApiMashape Key here


@app.route('/grammarly', methods={'GET', 'POST'})
def grammarly():
    if request.method == "POST":
        ans = get_corr(request.form["text_input"])
        print(request.form["text_input"])
        return render_template("grammarly.html", ans=ans,text=request.form["text_input"])

    return render_template("grammarly.html")


@app.route('/words',methods={'GET', 'POST'})
def words():
    if request.method == "POST":
        typ=request.form['type']
        word = request.form["text_input"]
        if typ=='Word':
            ans = get_word(word)
        elif typ=='Definition':
            ans = get_def(word)
            pass
        elif typ=='Synonyms':
            ans = get_syn(word)
            pass
        elif typ=='Antonyms':
            ans = get_ant(word)
            pass
        if type(ans) is str:
            return render_template("words.html", ans=ans.capitalize(), word=None, type=typ)
        if ans[0] != None:
            word = ans[0]
        ans = ans[1:]
        return render_template("words.html", ans=ans, word=word.capitalize(), type=typ)

    return render_template("words.html",ans=None)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/home')
def _home():
    return render_template("home.html")


def get_corr(text):
    text = ' '.join(text.split())
    text = text.replace(' ', '+')
    url = "https://api.textgears.com/check.php?text=" + text + "&key="+ textGearsKey
    code = requests.get(url).text
    a = open("temp.txt" , 'r')
    # code = a.read()
    result = json.loads(code)
    a.close()
    if result['result'] and list(result.keys()).count('errors')!=0:
        return show_corr(result['errors'])
    elif list(result.keys()).count('error_code')!=0:
        return show_error(result['error_code'], result['description'])
    return ''


def show_corr(sugges):
    newlist=[]
    for item in sugges:
        list=[]
        list.append(item['bad'])
        for better in item['better']:
            list.append(better)
        newlist.append(list)
    return newlist
    pass


def show_error(error_code, desc):

    return str(error_code)+str(desc)
    pass


def get_word(word):
    url='https://wordsapiv1.p.mashape.com/words/'+word

    code = requests.get(url, headers={
                            "X-Mashape-Key": wordsApiMashapeKey,
                               "Accept": "application/json"
                           }).text

    a = open("temp.txt", 'r')
    #code = a.read()
    result = json.loads(code)
    print(result)
    if list(result.keys()).count('success') == 1:
        return result['message']

    a.close()
    new=[]
    if list(result.keys()).count('word')==1:
        new.append(result['word'])
    else:
        new.append(None)

    if list(result.keys()).count('pronunciation') == 1:
        new.append(result['pronunciation'])
    else:
        new.append(None)

    new.append(result['results'])
    return new


def get_def(word):
    url = 'https://wordsapiv1.p.mashape.com/words/' + word+ '/definitions'
    code = requests.get(url, headers={
                            "X-Mashape-Key": wordsApiMashapeKey,
                               "Accept": "application/json"
                           }).text
    result = json.loads(code)
    if list(result.keys()).count('success') == 1:
        return result['message']
    new = []
    if list(result.keys()).count('word') == 1:
        new.append(result['word'])
    else:
        new.append(None)
    new.append(result['definitions'])
    return new


def get_syn(word):
    url = 'https://wordsapiv1.p.mashape.com/words/' + word + '/synonyms'
    code = requests.get(url, headers={
        "X-Mashape-Key": wordsApiMashapeKey,
        "Accept": "application/json"
    }).text
    result = json.loads(code)
    if list(result.keys()).count('success') == 1:
        return result['message']
    new = []
    if list(result.keys()).count('word') == 1:
        new.append(result['word'])
    else:
        new.append(None)
    new.append(result['synonyms'])
    return new

def get_ant(word):
    url = 'https://wordsapiv1.p.mashape.com/words/' + word + '/antonyms'
    code = requests.get(url, headers={
        "X-Mashape-Key": wordsApiMashapeKey,
        "Accept": "application/json"
    }).text
    result = json.loads(code)
    if list(result.keys()).count('success') == 1:
        return result['message']
    new = []
    if list(result.keys()).count('word') == 1:
        new.append(result['word'])
    else:
        new.append(None)
    new.append(result['antonyms'])
    return new

if __name__ == '__main__':
    app.run()
