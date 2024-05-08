from flask import Flask, render_template, request, redirect, url_for, session 



app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')


@app.route('/')
def home():
	return render_template("home.html")



@app.route('/register', methods=['GET', 'POST'])
def register():
	return render_template("register.html", title="Registration Page")




@app.route('/login', methods=['GET', 'POST'])
def login():
	return render_template("login.html", title="Login Page")



@app.route('/logout')
def logout():
	pass





@app.route('/words', methods=['GET', 'POST'])
def words():
	return render_template("words.html", title="Words Page")




@app.route('/sentences', methods=['GET', 'POST'])
def sentences():
	return render_template("sentences.html", title="Sentences Page")




