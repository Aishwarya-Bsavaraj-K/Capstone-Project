from flask import Flask,session,request,redirect,jsonify,render_template,url_for
import requests
import heartbeat
from werkzeug.utils import secure_filename
import database as db
import os 

app = Flask(__name__)
app.secret_key = "12345"


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET',"POST"])
def upload_file():
    print(request.method)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print("%%%%%%%%%%%%%%%%%%%")
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print("$$$$$$$$$$$$$$$$$$$$$$")            
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(os.getcwd(),"uploads", filename)
            file.save(file_path)
            
            
            status = HLA_and_upload(file_path,filename)
            return redirect(url_for('home',msg=status['status']))
            # obj = file.read()

def HLA_and_upload(file_path,filename):
    # file = self.input_file_path
    # print("file is ",file)
    # # post_params = {'parameters': params}
    with open(file_path,'rb') as f:
        beat = heartbeat.Heartbeat()
        public_beat = beat.get_public()
        (tag,state) = public_beat.encode(f)
        
    #db.save_data(session['user']['id'],filename,beat.todict())

    with open(file_path,'rb') as f:      
        files = {'file': f}  
        url = "http://0.0.0.0:5000/upload"
        d = {'userId':session['user']['id'],
                                'fileName':os.path.basename(file_path),
                                 'public_beat':public_beat.todict(),
                                 'tag':tag.todict(),
                                 'state':state.todict()
                                }
        print(d)
        r = requests.post(url, data=d, files=files)

        # if status_code == 200:
        status = db.save_data(session['user']['id'],filename,beat.todict())
    return status

        # self.table_appender(self.stack.tableWidget,'1',os.path.basename(self.input_file_path),'True','True')
        # self.showMessage("Success")

		# file.?close() # close the BytesIO object

@app.route("/verify/")
def send_for_verification():
    filename = request.args.get('data')
    if db.isVerified(session['user']['id'],filename):
        db.updateStatus(session['user']['id'],filename,is_valid=False,is_verified=False)
            
        beat = db.get_data(session['user']['id'],filename)
        print('*'*10,filename)
        r =requests.post("http://0.0.0.0:5555/audit",data={'userId':session['user']['id'],
                                                
                                                            'fileName':os.path.basename(filename)})
        print(r.status_code)
        return redirect(url_for('home',msg="success"))
    return redirect(url_for('home',msg="file already submitted for verification"))
    
    #  r = requests.get(url)


@app.route('/updateStatus/')
def updateStatus():
    userId = request.args.get("userId")

    filename = request.args.get("fileName")
    status = request.args.get("status")
    print(userId,filename,status)
    is_valid = True if status == "success" else False
    status = db.updateStatus(userId,filename,is_valid,True)
    return jsonify({'status':status})
    
    


@app.route("/")
def home():
    
    msg = request.args.get('msg')
    if 'user' in session:
        # return render_template("home.html")
        audit_requests,table=db.getRequests(session['user']['id'])        
        return render_template("home.html",audit_requests=audit_requests,table = table,getattr=getattr)
    

    return render_template("index.html",msg=msg)

@app.route('/user/home')
def user_home():
    if session['user']:
        audit_requests,table=db.getRequests()

        return render_template("home.html",audit_requests=audit_requests,table = table,getattr=getattr)
    else:
        return redirect(url_for('home',msg='You are not logged in'))




@app.route('/user/login',methods=['POST'])
def user_login():

    username = request.form['username']
    password = request.form['password']
    user = db.verify_user(username,password)

    if user:
        session['user'] = {'name':user.name,"id":user.id}
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home',msg="Wrong username/password"))


@app.route('/user/register',methods=['POST'])
def user_register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    status = db.register_user(name,email,password)
    return redirect(url_for('home',msg=status['status']))


@app.route('/user/logout')
def user_logout():
    session.pop('user')
    return redirect(url_for('home',msg="Successfully logged out"))

app.run(debug=True,port=5566,host='0.0.0.0')
