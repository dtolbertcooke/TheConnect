# The Connect
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required, current_user, \
    login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import Form, StringField, SubmitField, IntegerField, PasswordField, SelectField, DecimalField, \
    TextAreaField, validators, FileField
from wtforms.validators import DataRequired, NumberRange, EqualTo, Email
import pymysql
from flask_user import roles_required  # we will have three roles; admin, intern, sponsor
#from flask_table import Table, Col
from forms import *
import sys
import random


class User(UserMixin):
    def __init__(self, userID, email, password, role):
        self.id = userID
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
def is_admin():
    if current_user:
        if current_user.role == 'admin':
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
		email = form.email.data
		c.execute('SELECT * FROM User WHERE UserID = %s;' % (email))
		data = c.fetchall()

		for row in data:
			userID,email,password,role = row[0],row[1],row[2],row[3]
			user = User(userID,email,password,role)
			user_db[userID] = user
			valid_password = check_password_hash(user.pass_hash, form.password.data)
			if user is None or not valid_password:
				print('Invalid username or password', file=sys.stderr)
				redirect(url_for('home'))
			else:
				login_user(user)
				if role == 'Sponsor':
					return redirect('sponsor/%s'%(userID))
				elif role == 'Faculty':
					return redirect('admin_home/%s'%(userID))
				else:
					return redirect('intern/%s'%(userID))
	return render_template('landing.html', form=form, title=title, logo_link=logo_link)


@app.route('/intern/<UserID>')
@login_required
def intern_profile(UserID):
    title = "Profile"
    name = UserID
    # profile_pic = "..\static\img\s_profile.png"  testing out profile pic
    c.execute('Select * from Student where UserID = %s' % (name))
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

    return render_template('intern_profile.html', profile_pic=profile_pic, first_name=f_name, last_name=l_name, \
                           degree=degree, school=school, gpa=gpa, email=email, phone=phone, interest=interest, \
                           bio=bio)


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

@app.route('/admin_home/', methods=['GET', 'POST'])
def admin_home():
    c.execute('Select * from Internship WHERE approved = 0')
    approve_internship_data = c.fetchall()
    c.execute('Select * from Internship WHERE referral = 1')
    referral_requested_data = c.fetchall()
    c.execute('Select * from Student WHERE approved = 0')
    intern_data = c.fetchall()
    c.execute('Select * from Sponsor WHERE approved = 0')
    sponsor_data = c.fetchall()

    return render_template('admin_home.html', approve_internship_data=approve_internship_data
                           , intern_data=intern_data, sponsor_data=sponsor_data,
                           referral_requested_data=referral_requested_data)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/create_internship', methods=['GET', 'POST'])
def create_internship():
    form = createInternship()
    title = "Internship"
    logo_link = "/"

    if form.validate_on_submit():
        company = form.company.data
        heading = form.heading.data
        body = form.body.data
        startDate = form.startData.data
        endDate = form.endDate.data
        gpa = form.gpa.data
        pay = form.pay.data
        approved = 0
        referral = form.referral.data
        postID = str(random.randrange(100000,1000000))

        c.execute('INSERT INTO Internship values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            company, heading, body, startDate, endDate, gpa, pay, approved, referral, postID))

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
        interest = form.interest.data
        availability = form.availability.data
        bio = form.bio.data

        c.execute('INSERT INTO User values("%s","%s","%s","%s")' % (studentID, email, password, role))
        c.execute('INSERT INTO Student values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
            studentID, fname, lname, address, email, phone, major, gpa, state, address2, city, zipcode, interest, bio))

        db.commit()
        return redirect(url_for('home'))

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
        c.execute('INSERT INTO Error values("%s","%s","%s","%s",)' % (errType, email, errDescription))
        db.commit()
        return render_template('landing.html', form=form, title=title, nav1=nav1, logo_link=logo_link)
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

@app.route('/internships', methods=["GET","POST"])
@login_required
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
@login_required
def students():
	title = "Students"
	logoLink = "/"
	form = studentSearch()
	#need to set approved to 1 once internships begin to be approved		
	c.execute('SELECT * FROM Student')
	data = c.fetchall()
	
	if request.method == 'POST':
		return search_results(form)
	
		
	return render_template('internships.html',title=title, data=data, form=form, logo_link=logo_link)

@app.route('/results', methods=["GET","POST"])
@login_required
def search_results(search):
#	title = "Opportunities"
	logoLink = "/"
	form = request.form
	search_string = request.form.get('search')
	category = request.form.get('select')
	table = request.form.get('table')
	sql = 'SELECT * FROM Internship WHERE {} LIKE "%{}%"'.format(category,search_string)
	c.execute(sql)
	data = c.fetchall()
	if not data:
		flash('No Results')
		return redirect(url_for('internships'))
	return render_template('internships.html', data=data, form=form, logo_link=logo_link)
		


@app.route('/approve/', methods=['GET', 'POST'])
def approve():
    cursor = db.cursor()
    approval_list = request.get_json()
    UID = str(approval_list[0])
    value_from_AdminHome = int(approval_list[1])
    print(value_from_AdminHome)
    print(UID)
    approved = 1
    denied = 3
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


if __name__ == '__main__':  # You can run the main.py and type "localhost:8080" in your
    app.run(host='0.0.0.0', port=8080, debug=True)  # broswer to test the main.py in your computer.
