# The Connect
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, request
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
	def __init__(self, id, email, password, role):
		self.id = id
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
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db = pymysql.connect(host='35.231.51.121', user='root', password='connect1234', db='theConnect')
c = db.cursor()


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
	c.execute('SELECT * FROM User WHERE UserID = %s;' %(id))
	data = c.fetchall()

	for row in data:
		UserID, email, password, role = row[0], row[1], row[2], row[3]
		user = User(UserID, email, password, role)
	return user


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
	form = loginForm()

	if current_user.is_authenticated:
		user = current_user
		if user.getRole() == 'Sponsor':
			return redirect('sponsor/%s'%(user.getID()))
		elif user.getRole() == 'Faculty':
			return redirect('admin_home')
		else:
			return redirect("intern/%s"%(user.getID()))

	if form.validate_on_submit():
		UserID = form.UserID.data
		c.execute('SELECT * FROM User WHERE UserID = %s;' %(UserID))
		data = c.fetchall()

		for row in data:
			UserID,email,password,role = row[0],row[1],row[2],row[3]
			user = User(UserID,email,password,role)

			valid_password = check_password_hash(user.pass_hash, form.password.data)
			if user is None or not valid_password:
				print('Invalid username or password', file=sys.stderr)
				redirect(url_for('home'))
			else:
				login_user(user)
				if role == 'Sponsor':
					return redirect('sponsor/%s'%(UserID))
				elif role == 'Faculty':
					return redirect('admin_home')
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
	logo_link = "/"
	edit = ("/edit_profile/intern/%s" %(UserID))
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
		biography = row[13]
		availability = row[14]

	school = "Southern"
	profile_pic = "https://raw.githubusercontent.com/scsu-csc330-400/blu-test/help_jason/Static/\
	img/b.jpg?token=AoQ7TSJDqVpIdxBM_4hwk9J2QSluOd47ks5b7GhvwA%3D%3D"
	biography = biography

	return render_template('intern_profile.html',UserID=UserID, profile_pic=profile_pic, logo_link=logo_link, edit=edit,
						   first_name=f_name, last_name=l_name, degree=degree, school=school, gpa=gpa, email=email,
						   phone=phone, interest=interest, biography=biography,availability=availability)


@app.route('/sponsor/<UserID>')
@login_required
def sponsor_profile(UserID):
	title = "Profile"
	name = UserID
	edit = ("/edit_profile/sponsor/%s" %(UserID))

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

	c.execute('Select postID, heading, startDate, endDate from Internship where company like "%s"' %(company))
	data2 = c.fetchall()

	if len(data2)==0:
		postID = 0
		heading=''
		startDate=''
		endDate=''
	elif len(data2)>=1:
		for row2 in data2:
			postID = row2[0]
			heading = row2[1]
			startDate = row2[2]
			endDate = row2[3]

	c.execute('SELECT * FROM Applicants')
	data3 = c.fetchall()

	if len(data3)==0:
		fName = 'First'
		lName = 'Last'
		startDate='01/01/18'
		endDate='12/31/18'
	elif len(data3)>=1:
		for row3 in data3:
			fName = row3[1]
			lName = row3[2]
			degree = row3[3]
			gpa = row3[4]
			phone1 = row3[5]


	

	profile_pic = "https://raw.githubusercontent.com/scsu-csc330-400/blu-test/help_jason/Static/img/\
	b.jpg?token=AoQ7TSJDqVpIdxBM_4hwk9J2QSluOd47ks5b7GhvwA%3D%3D"

	return render_template('sponsor_profile.html', UserID=UserID, profile_pic=profile_pic, company=company, address=address,
						   website=website, phone=phone, zipcode=zipcode, city=city, description=description,
						   state=state, edit=edit, data2=data2, postID=postID, heading=heading, startDate=startDate,
						   endDate=endDate, fName=fName, lName=lName, degree=degree, gpa=gpa, phone1=phone1, data3=data3)

@app.route('/edit_profile/intern/<UserID>', methods=['GET', 'POST'])
@login_required
# @roles_required('admin','intern')
def edit_profile_intern(UserID):
	form = editInternProfileForm()
	title = 'Edit Profile'
	logo_link = "/"
	id = UserID


	if form.validate_on_submit():
		degree = form.degree.data
		gpa = form.gpa.data
		phone = form.phone.data
		interest = form.interest.data
		availability = form.availability.data
		bio = form.bio.data
		c.execute('UPDATE Student SET major = "%s", GPA = "%s", phone = "%s", \
		interest = "%s", availability = "%s", biography = "%s" WHERE UserID = "%s"' \
		% (degree, gpa, phone, interest, availability, bio, id))
		db.commit()
		flash('Your changes have been saved.')
		return redirect('intern/%s'%(UserID))

	elif request.method == 'GET':
		c.execute('Select * from Student where UserID = %s' %(id))
		data = c.fetchall()

		for row in data:
			degree = row[6]
			gpa = row[7]
			phone = row[5]
			interest = row[12]
			availability = row[14]
			bio = row[13]
		form.degree.data = degree
		form.gpa.data = gpa
		form.phone.data = phone
		form.interest.data = interest
		form.availability.data = availability
		form.bio.data = bio
	return render_template('edit_profile_intern.html', form=form, title=title, logo_link=logo_link)

@app.route('/edit_profile/sponsor/<UserID>', methods=['GET', 'POST'])
@login_required
def edit_profile_sponsor(UserID):
	form = editSponsorProfileForm()
	title = 'Edit Profile'
	logo_link = "/"
	id = UserID


	if form.validate_on_submit():
		company = form.company.data
		website = form.website.data
		phone = form.phone.data
		address = form.address.data
		city = form.city.data
		state = form.state.data
		zipcode = form.zipcode.data
		description = form.description.data
		c.execute('UPDATE Sponsor SET company = "%s", website = "%s", phone = "%s", \
		address = "%s", city = "%s", state = "%s", zipcode = "%s", description = "%s" \
		WHERE UserID = "%s"' % (company, website, phone, address, city, state, zipcode, description, id))
		db.commit()
		flash('Your changes have been saved.')
		return redirect('sponsor/%s'%(UserID))

	elif request.method == 'GET':
		c.execute('Select * from Sponsor where UserID = %s' %(id))
		data = c.fetchall()

		for row in data:
			company = row[1]
			website = row[3]
			phone = row[4]
			address = row[2]
			city = row[6]
			state = row[8]
			zipcode = row[5]
			description = row[7]
		form.company.data = company
		form.website.data = website
		form.phone.data = phone
		form.address.data = address
		form.city.data = city
		form.state.data = state
		form.zipcode.data = zipcode
		form.description.data = description
	return render_template('edit_profile_sponsor.html', form=form, title=title, logo_link=logo_link)

@app.route('/admin_home', methods=['GET', 'POST'])  # doesnt work yet, needs to define the class.
@login_required
# @roles_required('admin')
def admin_home():
	unq_id = 0
	c.execute('Select * from Internship WHERE approved = 0')
	approve_internship_data = c.fetchall()
	c.execute('Select * from Internship WHERE referral = 1')
	referral_requested_data = c.fetchall()
	c.execute('Select * from Internship')
	internship_data = c.fetchall()
	c.execute('Select * from Student WHERE approved = 0')
	intern_data = c.fetchall()
	c.execute('Select * from Sponsor')
	all_sponsor_data = c.fetchall()
	c.execute('Select * from Sponsor WHERE approved = 0')
	sponsor_data = c.fetchall()
	c.execute('Select * from ContactRequest')
	contact_data = c.fetchall()
	c.execute('Select * from Error')
	ticket_data = c.fetchall()
	c.execute('Select * from Student WHERE GPA >= 3.8 and suggestion = 0')
	top_student_data = c.fetchall()

	form_app = Approve()
	form_den = Deny()
	form_view = View()
	form_delete = Delete()

	return render_template('admin_home.html', approve_internship_data=approve_internship_data, form_app=form_app,
						   form_den=form_den, unq_id=unq_id, intern_data=intern_data, sponsor_data=sponsor_data,
						   contact_data=contact_data, ticket_data=ticket_data, referral_requested_data=referral_requested_data,
						   internship_data = internship_data, form_view=form_view,form_delete=form_delete,
						   all_sponsor_data=all_sponsor_data, top_student_data=top_student_data)


#create users
@app.route('/create_internship', methods=['GET', 'POST'])
#@login_required
def create_internship():
	form = createInternship()
	title = "Internship"
	logo_link = "/"
	name = current_user.getID()
	c.execute('Select company from Sponsor where UserID = %s' %(name))
	data = c.fetchall()
	for row in data:
                company = row[0]

	if form.validate_on_submit():
		#company = form.company.data
		heading = form.heading.data
		body = form.body.data
		startDate = form.startDate.data
		endDate = form.endDate.data
		gpa = form.gpa.data
		pay = form.pay.data
		approved = 0
		referral = form.referral.data
		postID = str(random.randrange(100000,1000000))

		c.execute('INSERT INTO Internship values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %(company,heading,body,startDate,endDate,gpa,pay,approved,referral,postID))
		db.commit()
		return redirect(url_for('home'))
	return render_template('create_internship.html', form=form, title=title, logo_link=logo_link)

@app.route('/create_sponsor', methods=['GET', 'POST'])
def create_sponsor():
	form = createSponsor()
	title = "Sponsor"
	logo_link = "/"

	if form.validate_on_submit():
		role = "Sponsor"
		UserID = str(random.randrange(100000,1000000))
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
		approved = 0
		c.execute('INSERT INTO User values("%s","%s","%s","%s")' % (UserID, email, password, role))
		c.execute('INSERT INTO Sponsor values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
				  %(UserID, company, address, website, phone, zipcode, city, description, state,approved))

		db.commit()
		login_user(User(UserID, email, password, role))
		return redirect('sponsor/%s'%(UserID))
	return render_template('create_sponsor.html', form=form, title=title, logo_link=logo_link)


@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
	form = createStudent()
	title = "Student"
	logo_link = "/"

	if form.validate_on_submit():
		role = "Student"
		UserID = str(random.randrange(100000,1000000))
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
		interest = form.interest.data
		biography = form.biography.data
		availability = form.availability.data
		approved = 0
		suggestion = 0

		c.execute('INSERT INTO User values("%s","%s","%s","%s")' % (UserID, email, password, role))
		c.execute('INSERT INTO Student values("%s","%s","%s","%s","%s","%s","%s",%s,"%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
			UserID, fname, lname, address, email, phone, major, gpa, state, address2, city, zipcode, interest, biography, availability, approved, suggestion))

		db.commit()
		login_user(User(UserID,email,password,role))
		return redirect('intern/%s'%(UserID))

	return render_template('create_student.html', form=form, title=title, logo_link=logo_link)


@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
	form = createTicket()
	title = "Report Error"
	logo_link = "/"
	if form.validate_on_submit():
		errType = form.errType.data
		email = form.email.data
		errDescription = form.errDescription.data
		c.execute('INSERT INTO Error values("%s","%s","%s")' %(errType, email, errDescription))
		db.commit()
		return redirect(url_for('home'))
	return render_template('create_ticket.html', form=form, title=title, logo_link=logo_link)



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


@app.route('/contact', methods=['GET', 'POST'])
def contact():
	form = contactForm()
	title = "Contact"
	logo_link = "/"
	if form.validate_on_submit():
		name = form.name.data
		email = form.email.data
		subject = form.subject.data
		message = form.message.data
		c.execute('INSERT INTO ContactRequest values("%s","%s","%s","%s")' % (name, email, subject, message))
		db.commit()
		return redirect(url_for('home'))
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
#@login_required
def user_resume():
	title = "Resume"
	logo_link = "/"
	resume_location = "..\static\img\s_resume.jpg"
	return render_template('user_resume.html', title=title, resume=resume_location, logo_link=logo_link)

#view and search
@app.route('/internships', methods=["GET","POST"])
#@login_required
# @roles_required('admin')
def internships():
	title = "Opportunities"
	logo_link = "/"
	form = internshipSearch()
	#need to set approved to 1 once internships begin to be approved
	c.execute('SELECT * FROM Internship')
	data = c.fetchall()

	if request.method == 'POST':
		return search_results(form)


	return render_template('internships.html',title=title, data=data, form=form, logo_link=logo_link)

@app.route('/students', methods=["GET","POST"])
#@login_required
# @roles_required('admin')
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
#@login.required
def search_results(search):
#	title = "Opportunities"
	logo_link = "/"
	form = internshipSearch()
	search_string = request.form.get('search')
	category = request.form.get('select')
	sql = 'SELECT * FROM Internship WHERE {} LIKE "%{}%"'.format(category,search_string)
	c.execute(sql)
	data = c.fetchall()
	if not data:
		flash('No Results')
		return redirect(url_for('internships'))
	return render_template('internships.html', data=data, form=form, logo_link=logo_link)

@app.route('/view_internship/<postID>', methods=["GET","POST"])
#login.required
def viewInternship(postID):
	logo_link = "/"
	sql = ('SELECT * FROM Internship WHERE postID = %s' %(postID))
	c.execute(sql)
	data = c.fetchall()

	for row in data:
		company = row[0]
		title = row[1]
		body= row[2]
		start = row[3]
		end = row[4]
		gpa = row[5]
		pay = row[6]
		post = postID

		
	return render_template('view_internship.html', data=data, logo_link=logo_link, company=company, title=title,
						   body=body, start=start, end=end, gpa=gpa, pay=pay, post=post)

@app.route('/submit_application', methods=["GET","POST"])
#login.required
def submitApplication():
	user = current_user.getID()
	sql = ('SELECT * FROM Student WHERE UserID=%s' %(user))
	c.execute(sql)
	student_data = c.fetchall()
	
	applicationID = str(random.randrange(100000,1000000))
	for row in student_data:
		f_name = row[1]
		l_name = row[2]
		degree = row[6]
		gpa = row[7]
		phone = row[5]
		interest = row[12]
		availability = row[14]
		bio = row[13]
		postID = "2509"


	sql = ('INSERT INTO Applicants values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %(applicationID, f_name, l_name, degree, gpa, phone, interest, availability, bio, postID))
	c.execute(sql)
	db.commit()

	return render_template('internships.html', user=user, id=id, data=data, form=form, logo_link=logo_link)

app.route('/approve/', methods=['GET', 'POST'])
def approve():
    cursor = db.cursor()
    approval_list = request.get_json()
    UID = str(approval_list[0])
    value_from_AdminHome = int(approval_list[1])
    approved = 1
    denied = 3
    print(approval_list)
    print(UID)
    print(value_from_AdminHome)
    if request.method == "POST":
        # neg float to pos float is tr range (not used, but for reference)
        # 1-999 is approval range for students
        # 1000-99900 is approval range for sponsor 100000
        # 100000-9990000 is approval range for sponsor
        # -1-(-999) is denial range for students
        # -1000-(-99900) is denial range for sponsor 100000

        # approve student-------------
        if 1 <= value_from_AdminHome <= 999:
            sql_approve1 = "UPDATE Student SET approved=%s WHERE UserID=%s"
            cursor.execute(sql_approve1, (approved, UID))
            db.commit()
            cursor.close()

            # approve sponsor-------------
        elif 1000 <= value_from_AdminHome <= 99900:
            sql_approve2 = "UPDATE Sponsor SET approved=%s WHERE UserID=%s"
            cursor.execute(sql_approve2, (approved, UID))
            db.commit()
            cursor.close()

            # Approve internship----------------
        elif 100000 <= value_from_AdminHome <= 9990000:
            sql_approve3 = "UPDATE Internship SET approved=%s WHERE postID=%s"
            cursor.execute(sql_approve3, (approved, UID))
            db.commit()
            cursor.close()

        elif 10000000 <= value_from_AdminHome <= 999000000:
            sql_approve4 = "UPDATE Student SET suggestion=%s WHERE UserID=%s"
            cursor.execute(sql_approve4, (approved, UID))
            db.commit()
            cursor.close()

        # denied student------------------------
        elif -1 >= value_from_AdminHome >= -999:
            sql_denied1 = "UPDATE Student SET approved=%s WHERE UserID=%s"
            cursor.execute(sql_denied1, (denied, UID))
            db.commit()
            cursor.close()
            print("Denied sucker")

            # denied sponsor------------------------
        elif -1000 >= value_from_AdminHome >= -99900:
            sql_denied2 = "UPDATE Sponsor SET approved=%s WHERE UserID=%s"
            cursor.execute(sql_denied2, (denied, UID))
            db.commit()
            cursor.close()
            print("Denied sucker")

            # denied internship------------------------
        elif -100000 >= value_from_AdminHome >= -9990000:
            sql_denied3 = "UPDATE Internship SET approved=%s WHERE postID=%s"
            cursor.execute(sql_denied3, (denied, UID))
            db.commit()
            cursor.close()
            print("Denied sucker")

    return 'hi'


@app.route('/recommendation')
def recommendation():
    c.execute('Select * from Student WHERE suggestion = 1')
    intern_data = c.fetchall()

    return render_template('recommendation.html', intern_data=intern_data)


@app.route('/reco/', methods=['GET', 'POST'])
def reco():
    cursor = db.cursor()
    clear_value = 1
    print("dndsidjf")
    if request.method == "POST":
        sql_approve1 = "UPDATE Student SET suggestion=0 WHERE suggestion=%s"
        cursor.execute(sql_approve1, (clear_value))
        db.commit()
        cursor.close()
        print("we did it")
    return 'hi'

if __name__ == '__main__':  # You can run the main.py and type "localhost:8080" in your
	app.run(host='0.0.0.0', port=8080, debug=True)  # broswer to test the main.py in your computer.
