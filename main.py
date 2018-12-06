#! /usr/bin/python

from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.secret_key = 'dumbkey'
app.config['SESSION_TYPE'] = 'memcached' 
socketio = SocketIO(app)
imgurl = "https://i.guim.co.uk/img/static/sys-images/Guardian/Pix/pictures/2015/5/1/1430492654253/240db3a1-e137-4d5e-aff0-0a58b34ca6c3-1020x729.jpeg?width=700&quality=85&auto=format&fit=max&s=1ed5cdce54406c97915ce4aab23a4ec0"

def get_all_chat():
    '''Get all of the messages'''
    f = open("chat.txt", "r")
    if f.mode == 'r':
    	messages = f.read()
    return str(messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
    	#set the username for the session
        session['username'] = request.form['username']
        return redirect(url_for('sessions'))
    else:
        return render_template('login.html', error=error)

#start chatroom at chatroom.html with username from login
@app.route('/')
def sessions():
    try:
        username = session['username']
        return render_template('chatroom.html', user=username, GET_image=imgurl) 
    except:
        return redirect(url_for('login'))

def messageReceived(methods=['GET', 'POST']):
    print('message received')
	
#on message	
@socketio.on('my event')
def handle_event(json, methods=['GET', 'POST']):
    print('received event: ' + str(json))
    print type(json)

    #input cases
    if json['message'] == '/help':
        print('worked')
    elif json['message'] == '/chat':
        messages = get_all_chat()
        #I'm not really sure what to do with this yet, but
        #it should only display on the user who typed /chat
        #Is this a server thing or a client thing?
    else:
    	#add messages to log
    	f= open("chat.txt","a+")
    	f.write(str(json['user_name']) + ": " + str(json['message']) + "\r\n")
    	f.close()
    #send to clients
    socketio.emit('response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9020, debug=True)
