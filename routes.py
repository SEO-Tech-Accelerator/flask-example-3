from flask import Flask, render_template, url_for, flash, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm
from os import path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a01ac6b99ff3af18854f2ee53b064b4b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
  
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page')

@app.route("/about")
def about():
    return render_template('about.html', subtitle='About Page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/captions")
def captions():
    FILE_NAME = "Becoming_Preface_shortened.wav"
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), FILE_NAME)
    def generate():
            with open(AUDIO_FILE, "rb") as fwav:
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")