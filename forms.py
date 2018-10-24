from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired

class loginForm(FlaskForm):
        username = StringField('Username:',validators=[DataRequired()])
        password = StringField('Password:', validators=[DataRequired()])
        submit = SubmitField('Submit')
'''       
class createInternship(FlaskForm):
	email = StringField('Email address', validators=[DataRequired()])
	address = StringField('Address: ',validators=[DataRequired()])
	address2 = StringField('Address 2: ',validators=[DataRequired()])
	city = StringField('City: ',validators=[DataRequired()])
	state = SelectField('State',choices=[('ct', 'Connecticut'), ('ma', 'Massachussets'), ('ny', 'New York')])
	zipcode = StringField('Zip' ,validators=[DataRequired()]) 
	major = StringField('Desired Major: ',validators=[DataRequired()])
	gpa = DecimalField('Minimum GPA: ',places =1,validators=[DataRequired()])
	pay = DecimalField('Pay Rate : $',places=2)
	description = TextAreaField('Internship description', validators=[DataRequired()])
	submit = SubmitField('Submit')'''

'''	
class createSponsor(FlaskForm):
	email = StringField('Email address ', validators=[DataRequired()])
	#emailConfirm = EmailField('Re-enter Email address ', [validators.DataRequired(),validators.Equalto('confirm ') ,validators.Email()])
	password = PasswordField('Password ', [validators.DataRequired(),validators.EqualTo('confirm ', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	address = Stringfield('Address: ',validators=[DataRequired()])
	address2 = StringField('Address 2: ',validators=[DataRequired()])
	city = StringField('City: ',validators=[DataRequired()])
	state = SelectField('State',choices=[('ct', 'Connecticut'), ('ma', 'Massachussets'), ('ny', 'New York')])
	zipcode = StringField('Zip' ,validators=[DataRequired()])
	description = TextAreaField('Organization description', validators=[DataRequired()])
	submit = SubmitField('Submit')'''

'''
class createStudent(FlaskForm):
	studentID = StringField('Student ID', validators=[DataRequired()])
	email = StringField('Email address ', validators=[DataRequired()])
	#emailConfirm = EmailField('Re-enter Email address ', [validators.DataRequired(),validators.Equalto('confirm ') ,validators.Email()])
	password = PasswordField('Password ', [validators.DataRequired(),validators.EqualTo('confirm ', message='Passwords must match')])
	confirm = PasswordField('Repeat Password')
	address = Stringfield('Address: ',validators=[DataRequired()])
	address2 = StringField('Address 2: ',validators=[DataRequired()])
	city = StringField('City: ',validators=[DataRequired()])
	state = SelectField('State ',choices=[('ct', 'Connecticut'), ('ma', 'Massachussets'), ('ny', 'New York')])
	zipcode = StringField('Zip ' ,validators=[DataRequired()])
	major = StringField('Major ',validators=[DataRequired()])
	gpa = DecimalField('GPA ',places=1,validators=[DataRequired()])
	submit = SubmitField('Submit')'''

'''	
class createTicket(FlaskForm):
	errType = SelectField(u'Error Type', choices=[('', ''), ('', ''), ('', '')])
	email = EmailField('Email address ', [validators.DataRequired(), validators.Email()])
	errDescription = TextAreaField('Error Description ' , validators=[DataRequired()])
	
'''
