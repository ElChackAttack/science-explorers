from flask import Flask, flash, render_template, request, session, url_for, redirect
import pymysql.cursors

#to deal with date searches
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import *

#to display charts
# import matplotlib.pyplot as plt
# from matplotlib import *

#to hash passwords
import hashlib

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
#connect to our specific database using appropriate user, password, and db
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='Science_Explorers_LMS',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

"""
GENERAL METHODS
"""
@app.route("/")
def default():
    return render_template("mainpage.html")

"""
LOGIN METHODS
"""
@app.route("/login_form", methods=["GET","POST"])
def login_form(message=None):
	return render_template("login_form.html",error = message)

@app.route("/login_method", methods=["GET","POST"])
def login_method():
	username = request.form['username']
	password = request.form['password']
	print('fetching username = {},password = {}'.format(username,password))
	try:
		query = """SELECT username, password FROM users WHERE username='{}' AND password='{}'""".format(username,password)
		print(query)
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		data = cursor.fetchall()
		print('data >>> ',data)
		cursor.close()
		print(len(data))
		print("SESSION",session)
		if len(data) != 0:
			print(session)
			if not bool(dict):
				login_successful = False
			else:
				session['username']= username
				login_successful = True
			return render_template("user_homepage.html",username=username,login_successful=login_successful)
		else:
			message = "Incorrect username/password combination"
			return login_form(message)
	except:
		message = "There was an unexpected error"
		login_form(message)


"""
LOGOUT METHODS
"""

@app.route("/logout",methods=["GET","POST"])
def logout():
	print(session)
	session.pop('username')
	return redirect(url_for('default'))

# @app.route("/user_homepage.html", methods=["GET,'POST"])
# def user_homepage

"""
REGISTRATION METHODS
"""
@app.route("/registration_form", methods=["GET","POST"])
def registration_form(message=None):
	return render_template("registration_form.html",error = message)

@app.route("/registration_method", methods=["GET","POST"])
def registration_method():
	print('entered registration_method successfully')
	# error = False
	username = request.form['username']
	password = request.form['password']
	print('fetching information correctly: ',username,password)
	# Remember to hash the passwords using MD5 preferably
	try:
		query = """SELECT username FROM users WHERE username='{}'""".format(username)		
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		data = cursor.fetchall()
		cursor.close()
		if len(data) != 0:
			print('len(data)!= 0')
			message = '>>> \nThe username already exists in the database \n>>>'
			return registration_form(message)
		else:
			query = """ INSERT INTO users VALUES ('{}','{}') """.format(username,password)
			cursor = conn.cursor()
			cursor.execute(query)
			conn.commit()
			cursor.close()
			message = '>>> \nYou have registered successfully \n>>>'
			return login_form(message)
	except:
		message = "There was an unexpected error"
		registration_form(message)

"""
USER METHODS 
"""
@app.route("/library",methods=["GET","POST"])
def library(display=None):
	try:
		print(session['username'])
	except:
		error = "Oops you are not logged in. Please log in first."
		return login_form(error)
	query = """ SELECT DISTINCT genre FROM Books """
	cursor = conn.cursor()
	cursor.execute(query)
	conn.commit()
	data = cursor.fetchall()
	cursor.close()
	try:
		book_name = request.form['book_to_search']
		print(book_name)
		query = """ SELECT Name FROM Books WHERE Name='{}' """.format(book_name)
		cursor = conn.cursor()
		cursor.execute(query)
		conn.commit()
		book_searched = cursor.fetchall()
		cursor.close()
		print(book_searched)
		if len(book_searched) == 0:
			book_searched = None
	except:
		book_searched = None
	return render_template("/library.html",y=data,display=display,book_searched=book_searched)

@app.route("/user_homepage",methods=["GET","POST"])
def user_homepage():
	return render_template("user_homepage.html",username=session['username'])


@app.route("/display_genre",methods=["GET","POST"])
def display_genre():
	genre=request.form['book_genre']
	query = """ SELECT name FROM Books WHERE genre='{}'""".format(genre)
	cursor = conn.cursor()
	cursor.execute(query)
	conn.commit()
	data = cursor.fetchall()
	cursor.close()
	genre=data
	print (genre)
	return library(genre)

@app.route("/book_reader",methods=["GET","POST"])
def book_reader():
	book_name = request.form['book_to_read']
	print('book reader book_name >>> ',book_name)
	return render_template("/book_reader.html",book_name = book_name)

# @app.route("/library_search",methods=["GET","POST"])
# def library_search():
# 	book_name = request.form['book_to_search']
# 	query = """ SELECT Name FROM Books WHERE Name='{}' """
# 	cursor = conn.cursor()
# 	cursor.execute(query)
# 	conn.commit()
# 	data = cursor.fetchall()
# 	cursor.close()
# 	if (data):
# 		return render_template("/library.html",book_cover=data)

"""
ADMIN METHODS
"""
@app.route("/add_book")
def add_book():
	print(session)
	return render_template("/add_book.html")
"""

"""

"""
Debug Mode
"""
app.secret_key = 'some key that you will never guess'
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
