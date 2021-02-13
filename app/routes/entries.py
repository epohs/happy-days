from app import app, db
from app.forms import NewEntry
from app.models import Entry
from flask import g
from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user
from datetime import datetime

@app.route('/new', methods=['GET', 'POST'])
def new_entry():
  
  if current_user.is_authenticated:
    
    g.user = current_user.get_id()
    
  else:
    
    return redirect(url_for('index'))
    
  
  form = NewEntry()
  
  if request.method == 'POST' and form.validate_on_submit():
    
    overall = request.form['overall']
    
    newEntry = Entry(
                  val = overall,
                  user_id = g.user
                )
  
    db.session.add(newEntry)
    
    db.session.commit()
    
    flash('New entry added.')
    
    return redirect(url_for('dashboard'))
    
  elif request.method == 'POST':

    flash('Something wasn’t right')
    
    
  
  now = datetime.now() # current date and time
  date_time = now.strftime("%A, %b. %d %Y")
  
  return render_template('entry/new.html', title='New entry - {}'.format(date_time), form=form)