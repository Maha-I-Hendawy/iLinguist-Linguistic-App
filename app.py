from flask import Flask, render_template, request, redirect, url_for, session 
import nltk


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




