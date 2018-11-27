#! /usr/bin/python

from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = 'dumbkey'
app.config['SESSION_TYPE'] = 'memcached' 
socketio = SocketIO(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('sessions'))
    else:
        return render_template('login.html', error=error)

@app.route('/')
def sessions():
    username = session['username']
    return render_template('chatroom.html', user=username)

def messageReceived(methods=['GET', 'POST']):
    print('message received')

@socketio.on('my event')
def handle_event(json, methods=['GET', 'POST']):
    print('received event: ' + str(json))
    print type(json)
    if json['message'] == 'help':
        print('worked')
    socketio.emit('response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9020, debug=True)
