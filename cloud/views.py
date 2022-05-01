from flask import session,Flask, render_template, redirect,request,url_for,jsonify
from werkzeug.utils import secure_filename
import os
import datetime
from database import db_session
import database as db
import random
import heartbeat

app = Flask(__name__)
app.secret_key = "12345"

@app.route("/")
def home():
    msg = request.args.get('msg')

    return render_template("index.html",msg=msg)

@app.route('/upload', methods=['POST'])
def handle_upload():
    if request.method == 'POST':
        userId = request.form['userId']
        file = request.files['file']
        tag = request.form['tag']
        state = request.form['state']
        public_beat = request.form['public_beat']
        filename = secure_filename(file.filename)
        print(filename)
        file_path = os.path.join(os.getcwd(),"static","uploads", filename)
        file.save(file_path)
     
        # print(eval(oiling)*200 + eval(wheel)*500 + eval(washing)*100 + eval(painting*400))


        status = db.save_file(userId,filename,tag,state,public_beat)
        return jsonify({'status':status})

    else:
        return ""

@app.route('/getUploads')
def getRequests():
    return jsonify(db.get_uploads())


@app.route('/getdata/<data>')
def getdata(data):
    
    user_id,_,fileName = data.split(',')
    print("**************\n",user_id,fileName,"\n**************")
    data = db.get_data(user_id,fileName)
    return jsonify({'public_beat':data.public_beat,'state':data.state})



@app.route('/getproof/')
def getfile():
    b = heartbeat.Heartbeat()

    challenge_text = request.args.get('challenge')
    user_id = request.args.get('userId')
    fileName = request.args.get('fileName')
    # print("*"*80)
    print(request.args.get('userId'))

    challenge_text = request.args.get('challenge')
    
    print("*"*80)
    print(challenge_text)
    print("*"*80)
    
    challenge = heartbeat.Swizzle.Challenge.fromdict(challenge_text)
    
    
    data = db.get_data(user_id,fileName)
    public_beat = heartbeat.Heartbeat.fromdict(data.public_beat).get_public()
    tag =heartbeat.Swizzle.Tag.fromdict(data.tag)
    state = heartbeat.Swizzle.State.fromdict(data.state)
    
    file_path = os.path.join(os.getcwd(),"static","uploads", fileName)
    with open(file_path,'rb') as f:
        proof = public_beat.prove(f,challenge,tag)

    
    
    # if data:

    # # file_path = os.path.join(os.getcwd(),"uploads", filename+'.enc')
    # return app.send_static_file(os.path.join("uploads", filename+'.enc'))

    # return open(file_path,'rb').read()
    return jsonify({'proof':proof.todict(),'public_beat':data.public_beat,'state':data.state})




@app.route('/admin/home')
def admin_home():
    if session['admin']:
        return redirect(url_for('service_register'))
    else:
        return redirect(url_for('home',msg='You are not logged in'))

@app.route('/admin/login',methods=['POST'])
def admin_login():

    username = request.form['username']
    password = request.form['password']

    if username == 'admin' and password == 'admin':
        session['admin'] = 'admin'
        return redirect(url_for('admin_home'))
    else:
        return redirect(url_for('home',msg="Wrong username/password"))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin')
    return redirect(url_for('home',msg="Successfully logged out"))



if __name__ == '__main__':
    app.run(debug = True,host="0.0.0.0",port=5000)


    
