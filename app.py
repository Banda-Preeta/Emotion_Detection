from flask import Flask, render_template, request, redirect, url_for, session,Response
import cv2
#from tensorflow.keras.utils import img_to_array
import tensorflow as tf
#from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
#from keras.models import load_model
import numpy as np
from keras.models import model_from_json
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from camera import Video
import json


application = Flask(__name__)
application.secret_key = 'Your Secrete key'
application.config['MYSQL_HOST'] = ''
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = 'Your password'
application.config['MYSQL_DB'] = 'userlogin'
mysql = MySQL(application)  
@application.route('/')
@application.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
  
@application.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
@application.route('/login1')
def login1():
    return render_template('login.html')
  
@application.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

#application.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1


@application.route('/index')
def index():
    return render_template('index.html')
@application.route('/home1')
def home1():
    return render_template('home.html')
@application.route('/about')
def about():
    return render_template('about.html')
@application.route('/team')
def team():
    return render_template('team.html')

def load():
    json_file = open('fold6.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    emotion_classifier = model_from_json(loaded_model_json)
    # load weights into new model
    emotion_classifier.load_weights("fold1.h5")
    return emotion_classifier

@application.route('/after', methods=['GET', 'POST'])
def after():
    imge = request.files['file1']
    imge.save('static/file.jpg')

    op = {0: "angry", 1: "confident", 2: "confused", 3: "contempt", 4: "crying", 5: "disgust", 6: "fear", 7: "happy",
          8: "neutral", 9: "sad", 10: "shy", 11: "sleepy", 12: "surprised"}

    path = "static/file.jpg"
    img = tf.keras.preprocessing.image.load_img(path, target_size=(48, 48))

    i = tf.keras.preprocessing.image.img_to_array(img) / 255
    input_arr = np.array([i])
    input_arr.shape
    
    emotion_classifier=load()
    pred = np.argmax(emotion_classifier.predict(input_arr))
    final_prediction = {op[pred]}
    return render_template('index.html', data=final_prediction)

@application.route('/index2')
def index2():
    return render_template('index2.html')
def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame +
        b'\r\n\r\n')
@application.route('/video')
def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__== "__main__":
    jsn={"detected": False, "pred": {"angry": 0, "confident": 0, "confused": 0, "contempt": 0, "crying": 0, "disgust": 0, "fear": 0, "happy": 0, "neutral": 0, "sad": 0, "shy": 0, "sleepy": 0, "surprised": 0}}
    with open('static/result/result.json', 'w') as f:
        json.dump(jsn, f)
if __name__ == "__main__":
    application.run(debug=True)