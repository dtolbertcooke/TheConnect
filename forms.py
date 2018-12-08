#The Connect
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, \
    current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, StringField, SubmitField, IntegerField, PasswordField, \
SelectField, DecimalField, TextAreaField, DateField, validators, SelectMultipleField, FileField
import pymysql
from flask_user import roles_required   # we will have three roles; admin, intern, sponsor
import sys
from wtforms.validators import DataRequired, NumberRange, EqualTo, Email

#login
class loginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

#new internship
class createInternship(FlaskForm):

	company = StringField('Organization Name', validators=[DataRequired()])
	heading = StringField('Internship Title', validators=[DataRequired()])
	body = TextAreaField('Internship Description', validators=[DataRequired()])
	startDate = DateField('Start Date', format='%m-%d-%Y', validators=[DataRequired()])
	endDate = DateField('End Date', format='%m-%d-%Y')
	gpa = DecimalField('Minimum GPA',places =1,validators=[DataRequired()])
	pay = DecimalField('Pay Rate $',places=2)
	referral = SelectField('Public listing or by referral only ', choices=[('0', 'Public'), ('1', 'Referral')])
	submit = SubmitField('Submit')

#new sponsor
class createSponsor(FlaskForm):
    sponsorID = StringField('User ID', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    company = StringField('Organization Name', validators=[DataRequired()])
    website = StringField('Organization website', validators=[DataRequired()])
    phone = StringField('Organization Contact Phone', validators=[DataRequired()])
    address = StringField('Organization Address',validators=[DataRequired()])
    city = StringField('Organization City',validators=[DataRequired()])
    state = SelectField('Organization State',choices=[('ct', 'Connecticut'), ('ma', 'Massachussets'), ('ny', 'New York')])
    zipcode = StringField('Organization Zip' ,validators=[DataRequired()])
    description = TextAreaField('Organization description', validators=[DataRequired()])
    submit = SubmitField('Submit')

#new student
class createStudent(FlaskForm):
    studentID = StringField('Student ID', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    address2 = StringField('Address 2')
    city = StringField('City',validators=[DataRequired()])
    state = SelectField('State',choices=[('ct', 'Connecticut'), ('ma', 'Massachussets'), ('ny', 'New York')])
    zipcode = StringField('Zip' ,validators=[DataRequired()])
    major = StringField('Major',validators=[DataRequired()])
    gpa = DecimalField('GPA',places=1,validators=[DataRequired()])
    interest = StringField('Interests', validators=[DataRequired()])
    availability = SelectMultipleField('Availability', choices=[('M', 'Monday'), ('T', 'Tuesday'), ('W', 'Wednesday'), ('Th', 'Thursday'), ('F', 'Friday'), ('S', 'Saturday'), ('S', 'Sunday')])
    bio = TextAreaField('Biogrpahy', validators=[DataRequired()])
    submit = SubmitField('Submit')

#new admin
class createAdmin(FlaskForm):
	studentID = StringField('Student ID', validators=[DataRequired()])
	email = StringField('Email address', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	fname = StringField('First Name', validators=[DataRequired()])
	lname = StringField('Last Name', validators=[DataRequired()])
	phone = StringField('Phone', validators=[DataRequired()])
	address = StringField('Address',validators=[DataRequired()])
	address2 = StringField('Address 2')
	city = StringField('City',validators=[DataRequired()])
	state = SelectField('State',choices=[('ct', 'Connecticut'), ('ma', 'Massachussets'), ('ny', 'New York')])
	zipcode = StringField('Zip' ,validators=[DataRequired()])
	submit = SubmitField('Submit')

#error report
class createTicket(FlaskForm):
	errType = SelectField(u'Error Type', choices=[('', ''), ('', ''), ('', '')])
	email = StringField('Email address', validators=[DataRequired(), Email()])
	errDescription = TextAreaField('Error Description ' , validators=[DataRequired()])
	submit = SubmitField("Submit")

#Contact
class contactForm(FlaskForm):
	name = StringField("Name")
	email = StringField("Email")
	subject = StringField("Subject")
	message = TextAreaField("Message")
	submit = SubmitField("Send")


#Internship Search Form
class internshipSearch(FlaskForm):
	choices = [('Heading', 'Heading'),('Company', 'Company'),('startDate', 'startDate'),('endDate','endDate'),('GPA','GPA'),('Pay','Pay')]
	search = StringField("Search")
	select = SelectField("Search by",choices=choices)
	table = HiddenField('Internship')
	
class studentSearch(FlaskForm):
	choices = [('Heading', 'Heading'),('Company', 'Company'),('startDate', 'startDate'),('endDate','endDate'),('GPA','GPA'),('Pay','Pay')]
	search = StringField("Search")
	select = SelectField("Search by",choices=choices)
	table = HiddenField('Student')
	


#Profile Edit


#Internship Edit


#Internship Application


class Approve(FlaskForm):
    approve = SubmitField("Approve")

class Deny(FlaskForm):
    deny = SubmitField("Deny")
