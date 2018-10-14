import flask from flask, render_template
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
