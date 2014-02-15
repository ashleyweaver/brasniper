from flask import Flask, flash
from pymongo import MongoClient
from secrets import MONGO_USER, MONGO_PASS, MONGO_URL, MONGO_PORT
from wtforms import Form, TextField, validators

app = Flask(__name__)
app.config.from_object(__name__)

client = MongoClient(MONGO_URL, MONGO_PORT)
client.BraSniper.authenticate(MONGO_USER, MONGO_PASS)
db = client.BraSniper

class RegistrationForm(Form):
	email = TextField('Email Address', [validators.Length(min=6, max=35)])
	sizes = TextField('Bra Sizes, separated by commas')

class UnregistrationForm(Form):
	email = TextField('Email Address', [validators.Length(min=6, max=35)])
	accept_unsubscribe = BooleanField('Are you sure you want to unsubscribe?', [validators.Required()])

@app.route('/', methods=['GET', 'POST'])
def subscribe():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		delimiters = " ", ","
	 	regexPattern = '|'.join(map(re.escape, delimiters))
		userSizes = re.split(regexPattern, title) 
        db.users.insert({email: form.email.data, sizes: userSizes, sent: []}
        flash('Thanks for subscribing!')
    return render_template('subscribe.html', form=form)

@app.route('/unsubscribe', methods=['GET', 'POST'])
def unsubscribe():
	form = UnregistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		db.users.remove({email: form.email.data})
		flash('You have successfully unsubscribed.')
	return render_template('unsubscribe.html', form=form)

if __name__ == '__main__':
	app.run()