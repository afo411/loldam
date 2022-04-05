from lib2to3.pgen2.literals import test
from riotwatcher import LolWatcher
from datetime import datetime, timedelta
import time
import threading
from socket import *
import socket
import sys
from flask import Flask, render_template, redirect, request, url_for
app = Flask(__name__)






@app.route('/', methods=['GET', 'POST'])
def index(nickname=None):
    return render_template('index.html' , nickname=nickname)

@app.route('/stop' ,methods=['POST'])
def stop():
    print('종료되었습니다')
    global a
    a = 1000
    return render_template('index.html')


@app.route('/<nickname>')
def inputtext(nickname=None ,timestart=None, time30s = None, time60s = None):
    lol_watcher = LolWatcher('RGAPI-af146936-2b3e-4d71-8923-af5eec7b009f')
    my_region = 'kr'
    inputName = nickname
    me = lol_watcher.summoner.by_name(my_region, inputName)
    spectator = None

    def loltime30():
        time30s = '30초가 경과하였습니다'
        print(time30s)
        timer.cancel()
        timer2 = threading.Timer(30, loltime60)
        timer2.start()

    def loltime60():
        time60s = "1분이 경과하였습니다"
        print(time60s)
    global a
    a = 0
    while a < 200:
        print('[*] Checking...', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print(a)
        a = a + 5
        
        try:
            spectator = lol_watcher.spectator.by_summoner(my_region, me['id'])

            start_time = datetime.fromtimestamp(spectator['gameStartTime'] / 1000)

            if datetime.now() - start_time < timedelta(minutes=5):
                timestart = '게임이 시작 되었습니다'
                print(timestart)
                timer = threading.Timer(30, loltime30)
                timer.start()
                break


        except:
            pass

        time.sleep(5)

    return render_template('index.html', nickname=nickname, timestart = timestart , time30s = time30s, time60s = time60s)

@app.route('/load',methods=['POST'])
def calculate(nickname=None):

    if request.method == 'POST':
        inputName = request.form['nickname']

    else:
        inputName = None

    return redirect(url_for('inputtext', nickname=inputName))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


