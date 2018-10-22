from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, SelectField
from wtforms.validators import DataRequired, NumberRange
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TheConnect is the best string'    #various flask extensions need a "secret key"

bootstrap = Bootstrap(app)                                    #invokes bootstrap
moment = Moment(app)                                          #invokes bootstrap

@app.route('/base')                                           #This is the base.html that every webpages uses.
def base():
    return render_template('base.html')


@app.route('/test')
def test():
    return render_template('test.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/admin/home')
def admin_home():
    return render_template('admin_home.html')


@app.route('/admin/login')
def admin_login():
    return render_template('admin_login.html')


@app.route('/create/internship')
def create_internship():
    return render_template('create_internship.html')


@app.route('/create/sponsor')
def create_sponsor():
    return render_template('create_sponsor.html')


@app.route('/create/student')
def create_student():
    return render_template('create_student.html')


@app.route('/create/ticket')
def create_ticket():
    return render_template('create_ticket.html')


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/notifications')
def notifications():
    return render_template('notifications.html')


@app.route('/sponsor/profile')
def sponsor_profile():
    return render_template('sponsor_profile.html')


if __name__ == '__main__':                                   #You can run the main.py and type "localhost:8080" in your
    app.run(host='0.0.0.0', port=8080, debug=True)           #broswer to test the main.py in your computer.