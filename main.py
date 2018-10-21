from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, SelectField
from wtforms.validators import DataRequired, NumberRange
import pymysql


@app.route('/')
def connectHome():
    return render_template('landing.html')
	

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')
