from flask import Flask, render_template, request, redirect, url_for, flash, session 
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash
import nltk


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)


app.app_context().push()


class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), nullable=False, unique=True)
	email = db.Column(db.String(100), nullable=False, unique=True)
	password = db.Column(db.String(100), nullable=False)
	text = db.relationship('Text', backref='user', lazy=True)



	def __str__(self):
		return f"{self.username}, {self.email}"



class Text(db.Model):
	text_id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.Text())
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)


	def __str__(self):
		return f"{self.text}"






@app.route('/')
def home():
	return render_template("home.html")



@app.route('/register', methods=['GET', 'POST'])
def register():
	users = User.query.all()
	if request.method == 'POST':
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
		confirm_password = request.form.get("confirm_password")
		for user in users:
			if user.username == username:
				flash("Username already exists")
			if user.email == email:
				flash("Email already exists")

		if password == confirm_password:
			hashed_password = generate_password_hash(password)
			user = User(username=username, email=email, password=hashed_password)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('login'))
			
	return render_template("register.html", title="Registration Page")




@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form.get("username")
		password = request.form.get("password")

		user = User.query.filter_by(username=username).first()

		if user and check_password_hash(user.password, password):
			session["user"] = user.username
			flash(f"Welcome {user.username}")
			return redirect(url_for('profile'))

	return render_template("login.html", title="Login Page")



@app.route('/logout')
def logout():
	if 'user' in session:
		session.pop('user', None)
		return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))




@app.route('/profile')
def profile():
	if 'user' in session:
		return render_template("profile.html")
	else:
		return redirect(url_for('login'))


words = []
sentences = []

@app.route('/words', methods=['GET', 'POST'])
def word():
	if request.method == 'POST':
		text = str(request.form.get('words'))
		words1 = nltk.word_tokenize(text)
		for word in words1:
			if word == '.':
				words1.remove(word)
		tagged = nltk.pos_tag(words1)
		words.append(tagged)
		return redirect(request.url)


	return render_template("words.html", title="Words Page", words=words)




@app.route('/sentences', methods=['GET', 'POST'])
def sentence():
	if request.method == 'POST':
		text = str(request.form.get('sentences'))
		sentences1 = nltk.sent_tokenize(text)
		sentences.append(sentences1)
		return redirect(request.url)
	return render_template("sentences.html", title="Sentences Page", sentences=sentences)




