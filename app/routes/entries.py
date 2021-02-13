from app import app, db
from app.forms import NewEntry
from app.models import Entry
from flask import render_template, flash, url_for, redirect, request

@app.route('/new')
def new_entry():
  
  form = NewEntry()
  
  return render_template('entry/new.html', title='New entry', form=form)