from flask import Flask,render_template,request,redirect,url_for,session
from analyser import main
app = Flask(__name__)
app.secret_key = '12345'

@app.route('/',methods=['GET','POST'])
def home():
	if request.method == 'GET':
		return render_template("index.html")
	else:
		url = request.form['url']
		print(url)
		results = main(url)
		print(results)
		return render_template('index.html',results=results,url=url,title_length=len(results['title'][0].title_text),desc_length=len(results['desc'].description_text))



if __name__ == '__main__':
	app.run(debug=True)