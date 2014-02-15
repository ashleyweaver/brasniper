from flask import Flask, flash, redirect, render_template, request, url_for
from pymongo import MongoClient
from secrets import MONGO_USER, MONGO_PASS, MONGO_URL, MONGO_PORT, SECRET_KEY
from wtforms import Form, TextField, BooleanField, validators
import re

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = SECRET_KEY

client = MongoClient(MONGO_URL, MONGO_PORT)
client.BraSniper.authenticate(MONGO_USER, MONGO_PASS)
db = client.BraSniper

class RegistrationForm(Form):
	email = TextField('Email Address', [validators.Length(min=6, max=35)])
	sizes = TextField('Bra Sizes, separated by spaces (no punctuation)')

class UnregistrationForm(Form):
	email = TextField('Email Address', [validators.Length(min=6, max=35)])
	accept_unsubscribe = BooleanField('Are you sure you want to unsubscribe?', [validators.Required()])

@app.route('/', methods=['GET', 'POST'])
def subscribe():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		if db.users.find({'email': form.email.data}):
			flash('You have already subscribed!')
			flash('Unsubscribe first if you want to update your sizes.')
			return redirect(url_for('unsubscribe'))
		userSizes = form.sizes.data.split()
		db.users.insert({'email': form.email.data, 'sizes': userSizes, 'sent': []})
		flash('Thanks for subscribing!')
		return redirect(url_for('subscribe'))
	return render_template('subscribe.html', form=form)

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
	form = UnregistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		db.users.remove({'email': form.email.data})
		flash('You have successfully unsubscribed.')
		return redirect(url_for('subscribe'))
	return render_template('unsubscribe.html', form=form)

@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run(debug = True)