from flask import session,Flask, render_template, redirect,request,url_for,jsonify
import datetime
from database import db_session
import database as db
import random
import requests
import hashlib
import time
import heartbeat

app = Flask(__name__)
app.secret_key = "12345"

@app.route("/")
def home():
    msg = request.args.get('msg')

    return render_template("index.html",msg=msg)

@app.route('/audit', methods=['POST'])
def service_register():
    if request.method == 'POST':
        userId = request.form['userId']
               
        fileName = request.form['fileName']
        status = db.saveRequest(userId,fileName)
        return jsonify(status)

@app.route('/register/<fileName>')
def register(fileName):
    return jsonify(db.registerForVerification(1,fileName))

@app.route("/verify/<data>")
def verfiy(data):
    print(data)
    r = requests.get("http://0.0.0.0:5000/getdata/"+data)
    userId,audit_id,fileName = data.split(',')
    #r = requests.get("http://0.0.0.0:5000/getdata/",data={'userId':userId,'fileName':fileName})
    d = r.json()
    


    b = heartbeat.Heartbeat()
    beat = heartbeat.Heartbeat.fromdict(d['public_beat'])
    beat = beat.get_public()
    print(d)
    state = heartbeat.Swizzle.State.fromdict(d['state'])
    challenge = beat.gen_challenge(state)
    print(challenge.todict())

    t1 = time.time()
    r = requests.get("http://0.0.0.0:5000/getproof/",
                     params = {'challenge':challenge.todict(),'userId':userId,'auditId':audit_id,'fileName':fileName})


    # r = requests.get("http://0.0.0.0:5000/static/uploads/"+fileName+".enc")
 
    d = r.json()
    proof = heartbeat.Swizzle.Proof.fromdict(d['proof'])
    verification_status = True
    if (beat.verify(proof,challenge,state)):
        is_valid = True
        print('file is stored by the server')
        
    else:
        print('file proof invalid')
        is_valid = False

    db.updateAuditRequest(fileName,is_valid,True)

    r = requests.get("http://0.0.0.0:5566/updateStatus/",
                     params = {'userId':userId,'status':'success' if is_valid else 'failure','fileName':fileName})

    return jsonify({'status':'success' if is_valid else 'failure'})
        
  

    t2 = time.time()
    # print("Blocks: ",fileSize," time taken to  is: ",t2-t1)
    # db.updateAuditRequest(fileName)


    # return jsonify({'status':k==new_key})

@app.route('/getUploads')
def getRequests():
    return jsonify(db.get_uploads())


@app.route('/admin/home')
def admin_home():
    if session['admin']:
        audit_requests,table=db.getRequests()

        return render_template("home.html",audit_requests=audit_requests,table = table,getattr=getattr)
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
    app.run(debug = True,host="0.0.0.0",port=5555)


    
