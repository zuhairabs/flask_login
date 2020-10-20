#!/usr/bin/python

# -*- coding: utf-8 -*-

#__copyright__ = 'Zuhair Abbas'

from flask import Flask, render_template, redirect, url_for, request
from flask import session, abort, flash, jsonify
import pymysql
import os
import flask

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

app.debug = True

app.secret_key = os.urandom(12)

def get_db():
    db = pymysql.connect(host='localhost', user='root', passwd='',
                         db='flask_api', charset='utf8mb4')
    return db

@app.route('/')
def base():
    return render_template('home.html')

# SignUp
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if 'email' in request.form \
                and 'password' in request.form:
            name = request.form.get('name')
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')
            confirmpassword = request.form.get('confirm')
            db = get_db()
            c = db.cursor()
            c.execute('select email from testApi where email = %s', email)
            account = c.fetchone()
            if account:
              flash('Email already exists please try again with another email!')
              return redirect(url_for('base'))
            else:
              if password == confirmpassword:
                c.execute('insert into testApi (name, email, username, password ) values (%s, %s, %s, md5(%s))', (name, email, username, password ))
                db.commit()
                flash('Registered Successfully')
                c.close()
                db.close()
                return redirect(url_for('base'))
              else:
                flash('Passwords do not match!')
                return redirect(url_for('base'))
        else:
            flash("Please enter all the details.")
            return redirect(url_for('base'))
    else:
        return redirect(url_for('base'))

# Login
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form \
            and 'password' in request.form:
        try:
            username = request.form['username']
            password = request.form['password']
            db = get_db()
            c = db.cursor()
            c.execute('SELECT id, name, email, username, password from testApi WHERE username = %s and password = md5(%s)', (username, password))
            account = c.fetchone()

            if account is not None:
                session['logged_in'] = True
                session['id'] = account[0]
                session['name'] = account[1]
                session['email'] = account[2]
                session['username'] = account[3]

                db.commit()
                c.close()
                db.close()
                flash('Logged In Successfully')
                print(session)
                return redirect(url_for('base'))
            else:
                flash('Invalid credentials. Please try again.')
                return redirect(url_for('base'))
        except Exception as e:
            print(e)
        flash('An error occured. Please try again.')
        return redirect(url_for('base'))
    else:
        return redirect(url_for('base'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logged Out Successfully')
    return redirect(url_for('base'))

'''
                        ERROR HANDLING
'''
@app.errorhandler(403)
def access_forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500



'''
                        APP RUNNER
'''
if __name__ == '__main__':
    app.run()  # host='0.0.0.0', port=5000
