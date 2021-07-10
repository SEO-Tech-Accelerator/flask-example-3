from flask import Flask, render_template, url_for, flash, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm
from analyze_audio import printWAV, getDuration
import time, random, threading
from turbo_flask import Turbo

app = Flask(__name__)
interval=10
FILE_NAME = "Becoming_Preface_shortened.wav"
turbo = Turbo(app)

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

@app.before_first_request
def before_first_request():
    #resetting time stamp file to 0
    file = open("pos.txt","w") 
    file.write(str(0))
    file.close()
    #starting thread that will time updates
    threading.Thread(target=update_captions).start()
    
@app.context_processor
def inject_load():
    # getting previous time stamp
    file = open("pos.txt","r")
    pos = int(file.read())
    file.close()
    print(pos)
    # writing next time stamp
    file = open("pos.txt","w")
    file.write(str(pos+interval))
    file.close()
    #returning captions
    return {'caption':printWAV(FILE_NAME, pos=pos, clip=interval)}
    
def update_captions():
    with app.app_context():
        while True:
            # timing thread waiting for the interval
            time.sleep(interval)
            # forcefully updating captionsPane with caption
            turbo.push(turbo.replace(render_template('captionsPane.html'), 'load'))
    
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
    TITLE = "Becoming"
    return render_template('captions.html', songName=TITLE, file=FILE_NAME)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")