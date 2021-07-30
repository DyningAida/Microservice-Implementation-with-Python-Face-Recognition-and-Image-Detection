from flask import Flask, render_template, url_for, redirect, session, request
from authlib.integrations.flask_client import OAuth
import pymysql, config, numpy as np
import cv2, time, os
from PIL import Image

app = Flask(__name__)

oauth = OAuth(app)
app.secret_key = 'percobaanuasai'
app.config.from_object('config')

def db_connect():
    return pymysql.connect(host='localhost', user='root', password='', database='simak_mst_mhs', port=3306)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display')
def display():
    if 'username' in session:
        db = db_connect()
        sql = f"select *from simak_mst_mahasiswa where MhswID='{session['username']}'"
        with db:
            cur = db.cursor()
            cur.execute(sql)
            data = cur.fetchall()
            return render_template ('profil.html', data = data)
    camera = 0
    video = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
    faceDetection = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('dataset/training.xml')
    a = 0
    while True:
        a = a+1
        check, frame = video.read()
        abu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        wajah = faceDetection.detectMultiScale(abu,1.3,5)
        for(x,y,w,h) in wajah:
            #cv2.imwrite('dataset/user.'+str(id)+'.'+str(a)+'.jpg',abu[y:y+h,x:x+w])
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            id, conf = recognizer.predict(abu[y:y+h,x:x+w])
            if id > 0:
                cv2.putText(frame,str(id),(x+40,y-10),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,0))
            else:
                cv2.putText(frame,'tidak dikenali',(x+40,y-10),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,0))
        cv2.imshow("Face Recognition", frame)
        key = cv2.waitKey(1)
        if key==ord('a'):
            break
            #if (a>29):
            #   break
    video.release()
    cv2.destroyAllWindows()
    db = db_connect()
    sql = f"select *from simak_mst_mahasiswa where MhswID='{id}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        data = cur.fetchall()
    return render_template('profil.html', data=data)

@app.route('/register',methods=['GET','POST'])
def register():
    if 'username' in session:
        return render_template('profil.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')

def verifikasi_username_password(username, password):
    db = db_connect()
    sql = f"select * from simak_mst_mahasiswa where Login={username} and password = SUBSTRING(MD5(MD5('{password}')), 1, 10)"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        if cur.fetchone():
            return True
        return False

@app.route('/login', methods=['POST'])
def login_auth():
    username = request.form['username']
    password = request.form['password']
    if verifikasi_username_password(username, password):
        session['username'] = username
        camera = 0
        video = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
        faceDetection = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        a = 0
        id = username
        #nama = input('masukkan nama : Dyning Aida Batrishya')
        while True:
            a = a+1
            check, frame = video.read()
            abu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            wajah = faceDetection.detectMultiScale(abu,1.3,5)
            for(x,y,w,h) in wajah:
                cv2.imwrite('dataset/mhs_'+str(id)+'_'+str(a)+'.jpg',abu[y:y+h,x:x+w])
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                #cv2.putText(frame,"mahasiswa",(x+40,y-10),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,0))
            cv2.imshow("Face Recognition", frame)
            if (a>29):
                break
        video.release()
        cv2.destroyAllWindows()
        return redirect('/display')
    else:
        return 'login gagal'

@app.route('/cek_gambar',methods=['POST','GET'])
def cek_gambar():
    if request.method == 'POST':
        filestr = request.files['image']
        #convert string data to numpy array
        npimg = np.fromfile(filestr, np.uint8)
        # convert numpy array to image
        img = cv2.imdecode(npimg, cv2.IMREAD_GRAYSCALE)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('dataset/training.xml')
        faceDetection = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        wajah = faceDetection.detectMultiScale(img,1.3,5)
        for(x,y,w,h) in wajah:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            id, conf = recognizer.predict(img[y:y+h,x:x+w])
            if id > 0:
                return render_template('result.html', id=id)
                #cv2.imshow('img', img)
            else:
                return str(id)
        # cv2.imshow('img', img)
        # cv2.waitKey()
        # cv2.destroyAllWindows()   
    return render_template('cek_gambar.html')

if __name__ == "__main__":
   app.run(debug=True)