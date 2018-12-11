# The Connect
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required, current_user, \
    login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, StringField, SubmitField, IntegerField, PasswordField, SelectField, DecimalField, HiddenField, \
    TextAreaField, validators
from wtforms.validators import DataRequired, NumberRange, EqualTo, Email
import pymysql
from flask_user import roles_required  # we will have three roles; admin, intern, sponsor
from forms import *
import sys
import random


class User(UserMixin):
    def __init__(self, UserID, email, password, role):
        self.id = UserID
        self.email = email
        self.pass_hash = generate_password_hash(password)
        print(self.pass_hash, file=sys.stderr)
        self.role = role

    def getID(self):
        return self.id

    def getEmail(self):
        return self.email

    def getRole(self):
        return self.role


app = Flask(__name__)
app.config['SECRET_KEY'] = 'TheConnect is the best string'  # various flask extensions need a "secret key"
bootstrap = Bootstrap(app)  # invokes bootstrap
moment = Moment(app)  # invokes bootstrap
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = pymysql.connect(host='35.231.51.121', user='root', password='connect1234', db='theConnect')
c = db.cursor()
user_db = {}

# user roles
def is_faculty():
    if current_user:
        if current_user.role == 'Faculty':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)


def is_sponsor():
    if current_user:
        if current_user.role == 'sponsor':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)


def is_student():
    if current_user:
        if current_user.role == 'student':
            return True
        else:
            return False
    else:
        print('User not authenticated.', file=sys.stderr)


# Login manager uses this function to manage user sessions.
# Function does a lookup by id and returns the User object if
# it exists, None otherwise.		
@login_manager.user_loader
def load_user(id):
    return user_db.get(id)


@app.route('/base')  # This is the base.html that every webpages uses.
def base():
    return render_template('base.html')


@app.route('/test')
def test():
    form = loginForm()
    return render_template('test.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    title = "404 - page not found"
    nav1 = "Home"
    logo_link = "/"
    return render_template('404.html', title=title, nav1=nav1, logo_link=logo_link), 404


@app.errorhandler(500)
def internal_server_error(e):
    title = "505 - internal server error"
    nav1 = "Home"
    logo_link = "/"
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def home():
	title = "TheConnect"
	logo_link = "/"

	if current_user.is_authenticated:
		if current_user.getRole == 'Sponsor':
			return redirect(url_for('sponsor_profile/%s'%(UserID)))
		elif current_user.getRole == 'Faculty':
			return redirect(url_for('admin_home/%s'%(UserID)))
		else:
			return redirect(url_for('intern_profile/%s'%(UserID)))
		
	form = loginForm()
	if form.validate_on_submit():
		UserID = form.UserID.data
		c.execute('SELECT * FROM User WHERE UserID = %s;' % (UserID))
		data = c.fetchall()

		for row in data:
			UserID,email,password,role = row[0],row[1],row[2],row[3]
			user = User(UserID,email,password,role)
			user_db[UserID] = user
			valid_password = check_password_hash(user.pass_hash, form.password.data)
			if user is None or not valid_password:
				print('Invalid username or password', file=sys.stderr)
				redirect(url_for('home'))
			else:
				login_user(user)
				if role == 'Sponsor':
					return redirect('sponsor/%s'%(UserID))
				elif role == 'Faculty':
					return redirect('admin_home/%s'%(UserID))
				else:
					return redirect('intern/%s'%(UserID))
	return render_template('landing.html', form=form, title=title, logo_link=logo_link)
	
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#profiles
@app.route('/intern/<UserID>')
@login_required
def intern_profile(UserID):
	title = "Profile"
	name = UserID
	logo_link = ('/edit_intern/%s' %(UserID))
	# profile_pic = "..\static\img\s_profile.png"  testing out profile pic
	c.execute('Select * from Student where UserID = %s' %(name))
	data = c.fetchall()

	for row in data:
		UserID = row[0]
		f_name = row[1]
		l_name = row[2]
		degree = row[6]
		gpa = row[7]
		email = row[4]
		phone = row[5]
		interest = row[12]
		bio = row[13]

	school = "Southern"
	profile_pic = "https://raw.githubusercontent.com/scsu-csc330-400/blu-test/help_jason/Static/\
	img/b.jpg?token=AoQ7TSJDqVpIdxBM_4hwk9J2QSluOd47ks5b7GhvwA%3D%3D"

	return render_template('intern_profile.html', profile_pic=profile_pic, logo_link=logo_link, first_name=f_name, last_name=l_name, \
                           degree=degree, school=school, gpa=gpa, email=email, phone=phone, interest=interest, \
                           bio=bio,)


@app.route('/sponsor/<UserID>')
@login_required
def sponsor_profile(UserID):
    title = "Profile"
    name = UserID
    # profile_pic = "..\static\img\s_profile.png"  testing out profile pic
    c.execute('Select * from Sponsor where UserID = %s' %(name))
    data = c.fetchall()

    for row in data:
        UserID = row[0]
        company = row[1]
        address = row[2]
        website = row[3]
        phone = row[4]
        zipcode = row[5]
        city = row[6]
        description = row[7]
        state = row[8]

    profile_pic = "https://raw.githubusercontent.com/scsu-csc330-400/blu-test/help_jason/Static/img/\
    b.jpg?token=AoQ7TSJDqVpIdxBM_4hwk9J2QSluOd47ks5b7GhvwA%3D%3D"

    return render_template('sponsor_profile.html', profile_pic=profile_pic, company=company, address=address, \
                           website=website, phone=phone, zipcode=zipcode, city=city, description=description, state=state)


@app.route('/admin_home', methods=['GET', 'POST'])  # doesnt work yet, needs to define the class.
@login_required
# @roles_required('admin')
def admin_home():
    c.execute('Select * from Internship WHERE approved = 0')
    approve_internship_data = c.fetchall()
    c.execute('Select * from Internship WHERE referral = 1')
    referral_requested_data = c.fetchall()
    c.execute('Select * from Student')
    intern_data = c.fetchall()
    c.execute('Select * from Sponsor')
    sponsor_data = c.fetchall()
    form_app = Approve()
    form_den = Deny()
    unq_id = 0
    if form_app.validate_on_submit():
        print("hiii")
        # c.execute('INSERT INTO User values("
    elif form_den.validate_on_submit():
        print("bye")
        # c.execute('INSERT INTO User values("

    return render_template('admin_home.html', approve_internship_data=approve_internship_data, form_app=form_app,
                           form_den=form_den, unq_id=unq_id, intern_data=intern_data, sponsor_data=sponsor_data,
                           referral_requested_data=referral_requested_data)


#create users
@app.route('/create_internship', methods=['GET', 'POST'])
# @login_required
# roles_required('admin','sponsor')
def create_internship():
	form = createInternship()
	title = "Internship"
	logo_link = "/"

	if form.validate_on_submit():
		
		company = company
		heading = heading
		body = body
		startDate = startDate
		endDate = endDate
		gpa = gpa
		pay = pay
		approved = 0
		referral = referral
		postID = str(random.randrange(100000,1000000)) 
		#postID needs loop to check for duplicates

		c.execute('INSERT INTO Internship values("%s","%s","%s","%s","%s","%s","%s","s","s")' % (company,heading,body,startDate,endDate,gpa,pay,approved, referral, postID))
		db.commit()
		return render_template('successful_internship.html', title=title, nav1=nav1, logo_link=logo_link)

	return render_template('create_internship.html', form=form, title=title, logo_link=logo_link)


@app.route('/create_sponsor', methods=['GET', 'POST'])
def create_sponsor():
    form = createSponsor()
    title = "Sponsor"
    logo_link = "/"

    if form.validate_on_submit():
        role = "Sponsor"
        sponsorID = form.sponsorID.data
        email = form.email.data
        password = form.password.data
        company = form.company.data
        website = form.website.data
        phone = form.phone.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        description = form.description.data

        c.execute('INSERT INTO User values("%s","%s","%s","%s")' % (sponsorID, email, password, role))
        c.execute('INSERT INTO Sponsor values("%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            sponsorID, company, address, website, phone, zipcode, city, description, state))

        db.commit()
        return redirect(url_for('home'))
    return render_template('create_sponsor.html', form=form, title=title, logo_link=logo_link)


@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
    form = createStudent()
    title = "Student"
    logo_link = "/"

    if form.validate_on_submit():
        role = "Student"
        studentID = form.studentID.data
        email = form.email.data
        password = form.password.data
        fname = form.fname.data
        lname = form.lname.data
        phone = form.phone.data
        address = form.address.data
        address2 = form.address2.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        major = form.major.data
        gpa = form.gpa.data

        c.execute('INSERT INTO User values("%s","%s","%s","%s")' % (studentID, email, password, role))
        c.execute('INSERT INTO Student values("%s","%s","%s","%s","%s","%s","%s",%s,"%s","%s","%s","%s")' % (
            studentID, fname, lname, address, email, phone, major, gpa, state, address2, city, zipcode))

        db.commit()
        return redirect(url_for('home'))

    return render_template('create_student.html', form=form, title=title, logo_link=logo_link)

#create ticket (probably get rid of)
@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    form = createTicket()
    title = "Report Error"
    logo_link = "/"
    if form.validate_on_submit():
        errType = form.errType.data
        email = form.email.data
        errDescription = form.errDescription.data
        c.execute('INSERT INTO Error values("%s","%s","%s","%s",)' % (errType, email, errDescription))
        db.commit()
        return render_template('landing.html', form=form, title=title, nav1=nav1, logo_link=logo_link)
    return render_template('create_ticket.html', form=form, title=title, logo_link=logo_link)

# resume
# resume_location = "..\static\img\s_resume.jpg"
# @app.route('/user_resume')
# def user_resume():
#    title = "Resume"
#    logo_link = "/"
#    resume_location = "..\static\img\s_resume.jpg"
#    return render_template('user_resume.html', title=title, resume=resume_location, logo_link=logo_link)

# @app.route('/user/<user>')
# def user_profile():
#     title = "Profile"
#     return render_template('sponsor_profile.html', title=title)

@app.route('/success')
def successful_internship():
    title = "Success"
    logo_link = "/"
    return render_template('successful_internship.html', title=title, logo_link=logo_link)


@app.route('/faq')
def faq():
    title = "FAQ"
    logo_link = "/"
    return render_template('faq.html', title=title, logo_link=logo_link)


@app.route('/about')
def about():
    title = "About"
    logo_link = "/"
    return render_template('about.html', title=title, logo_link=logo_link)


@app.route('/contact')
def contact():
    form = contactForm()
    title = "Contact"
    logo_link = "/"
    return render_template('contact.html', form=form, title=title, logo_link=logo_link)


@app.route('/help')
def help():
    title = "Help"
    logo_link = "/"
    return render_template('help.html', title=title, logo_link=logo_link)


@app.route('/notifications')
def notifications():
    title = "Notifications"
    return render_template('notifications.html', title=title)


@app.route('/user_resume')
def user_resume():
    title = "Resume"
    logo_link = "/"
    resume_location = "..\static\img\s_resume.jpg"
    return render_template('user_resume.html', title=title, resume=resume_location, logo_link=logo_link)


@app.route('/register')
def register():
    title = "Register"
    return render_template('register.html', title=title)


@app.route('/search')
def search():
    return render_template('search.html')

#view and search	
@app.route('/internships', methods=["GET","POST"])
#@login_required
def internships():
	title = "Opportunities"
	logo_link = "/intern/<UserID>"
	form = internshipSearch()
	#need to set approved to 1 once internships begin to be approved		
	c.execute('SELECT * FROM Internship')
	data = c.fetchall()
	
	if request.method == 'POST':
		return search_results(form)
	
		
	return render_template('internships.html',title=title, data=data, form=form, logo_link=logo_link)

@app.route('/students', methods=["GET","POST"])
#@login_required
def students():
	title = "Students"
	logo_link = "/"
	form = studentSearch()		
	c.execute('SELECT * FROM Student')
	data = c.fetchall()
	
	if request.method == 'POST':
		return search_results(form)
	
		 
	return render_template('internships.html',title=title, data=data, form=form, logo_link=logo_link)

@app.route('/results', methods=["GET","POST"])
#@login_required
def search_results(search):
#	title = "Opportunities"
	logo_link = "/"
	form = request.form
	search_string = request.form.get('search')
	category = request.form.get('select')

	sql = 'SELECT * FROM Internship WHERE {} LIKE "%{}%"' .format(category,search_string)

	c.execute(sql)
	data = c.fetchall()
	
	if not data:
		flash('No Results')
		return redirect(url_for('internships'))
	return render_template('internships.html', data=data, form=form, logo_link=logo_link)

#edit users	
@app.route('/edit_intern/<UserID>', methods=['GET','POST'])
def update_student(UserID):

	logo_link = ("/intern/%s" %(UserID))
	title = "Edit"
	
	c.execute('SELECT pass FROM User WHERE UserID = %s;' % (UserID))
	data = c.fetchall()
	
	pass_form = changePassword(request.form)
	for row in data:
		pass_form.password.data = row[0]
		pass_form.confirm.data = pass_form.password.data
		
	if request.method == "POST" and pass_form.validate():
		password = pass_form.password.data
		
		c.execute('UPDATE User SET pass=%s WHERE UserID=%s'%(password,UserID))
		db.commit()
		
	
	c.execute('SELECT * FROM Student WHERE UserID = %s;' %(UserID))
	data = c.fetchall()
	
	student_form = editStudent(request.form)
	
	for row in data:
	
		student_form.UserID.data = row[0]
		student_form.email.data = row[4]
		student_form.fname.data = row[1]
		student_form.lname.data = row[2]
		student_form.phone.data = row[5]
		student_form.address.data = row[3]
		student_form.address2.data = row[10]
		student_form.city.data = row[10]
		student_form.state.data = row[9]
		student_form.zipcode.data = row[11]
		student_form.major.data = row[6]
		student_form.gpa.data = row[7]
	
	if request.method == 'POST' and student_form.validate():
		
		UserID = student_form.UserID.data
		email = student_form.email.data
		fname = student_form.fname.data
		lname = student_form.lname.data
		phone = student_form.phone.data
		address = student_form.address.data
		address2 = student_form.address2.data
		city = student_form.city.data
		state = student_form.state.data
		zipcode = student_form.zipcode.data
		major = student_form.major.data
		gpa = student_form.gpa.data
		
		c.execute('UPDATE Student SET studentID=%s,email=%s,password=%s,fname=%s,lname=%s,phone=%s,address=%s,address2=%s,city=%s,state=%s,zipcode=%s,major=%s,gpa=%s WHERE UserID=%s' 
							%(UserID,email,fname,lname,phone,address,address2,city,state,zipcode,major,gpa))
		db.commit()
		
		return redirect(url_for('/intern/<UserID>'))
		
	

	return render_template('edit_student.html', form1=pass_form, form2=student_form, logo_link=logo_link)

@app.route('/edit_sponsor/<UserID>', methods=['GET','POST'])
def update_sponsor(UserID):

	title = "edit"
	logo_link = "/sponsor/<UserID>"
	
	c.execute('SELECT * FROM Sponsor WHERE UserID = %s;' % (UserID))
	data = c.fetchall()
	
	form = createSponsor(request.form)
	
	for row in data:
	
		form.company.data = row[4]
		form.address.data = row[2]
		form.website.data = row[1]
		form.phone.data = row[1]
		form.zipcode.data = row[5]
		form.city.data = row[10]
		form.description.data = row[3]
		form.state.data = row[5]
	
	if request.method == 'POST' and form.validate():
		
		sponsorID = form.sponsorID.data
		email = form.email.data
		password = form.password.data
		company = form.company.data
		website = form.website.data
		phone = form.phone.data
		address = form.address.data
		city = form.city.data
		state = form.state.data
		zipcode = form.zipcode.data
		description = form.description.data

		
		c.execute('UPDATE Sponsor SET company=%s,address=%s,website=%s,phone=%s,zipcode=%s,city=%s,description=%s,state=%s WHERE UserID=%s' 
							%(company, address, website, phone, zipcode, city, description, state, UserID))
		db.commit()
		
		return redirect(url_for('/sponsor/<UserID>'))
		
	

	return render_template('edit_info.html', form=form,title=title,logo_link=logo_link)

#edit internships, need internship primary key
@app.route('/edit_internship/<postID>', methods=['GET','POST'])
#@loginrequired
#roles_required(['admin','sponsor'])
def update_internship(postID):

	title = "edit"
	logo_link = "/sponsor/<UserID>"
	
	c.execute('SELECT * FROM Internship WHERE postID = %s;' % (postID))
	data = c.fetchall()
	
	form = createInternship(request.form)
	
	for row in data:
	
		form.company.data = row[0]
		form.heading.data = row[1]
		form.body.data = row[2]
		form.startDate.data = row[3]
		form.endDate.data = row[4]
		form.gpa.data = row[5]
		form.pay.data = row[6]
		form.referral.data = row[8]
	
	if request.method == 'POST' and form.validate():
		
		company = form.company.data
		heading = form.heading.data
		body = form.body.data
		startDate = form.startDate.data
		endDate = form.endDate.data
		gpa = form.gpa.data
		pay = form.pay.data
		referral = form.referral.data

		
		c.execute('UPDATE Internship SET company=%s,heading=%s,body=%s,startDate=%s,endDate=%s,gpa=%s,pay=%s,referral=%s WHERE UserID=%s' 
							%(company, heading, body, startDate, endDate, gpa, pay, referral))
		db.commit()
		
		return redirect(url_for('/sponsor/<UserID>'))
		
	

	return render_template('edit_internship.html', form=form,title=title,logo_link=logo_link)

	
if __name__ == '__main__':  # You can run the main.py and type "localhost:8080" in your
    app.run(host='0.0.0.0', port=8080, debug=True)  # broswer to test the main.py in your computer.
