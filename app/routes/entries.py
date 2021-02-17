from app import app, db
from app.forms import NewEntry
from app.models import Entry
from flask import g
from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user
from sqlalchemy import extract, or_
from sqlalchemy.dialects import sqlite
from datetime import datetime




@app.route('/new', methods=['GET', 'POST'])
def new_entry():
  
  if current_user.is_authenticated:
    
    g.user = current_user.get_id()
    
  else:
    
    return redirect(url_for('index'))
    
  
  form = NewEntry()
  
  if request.method == 'POST' and form.validate_on_submit():
    
    overall = request.form.get('overall', type=float)
    outlook = request.form.get('outlook', type=float)
    energy = request.form.get('energy', type=float)
    focus = request.form.get('focus', type=float)
    
    newEntry = Entry(
                  val = overall,
                  user_id = g.user
                )
  
    db.session.add(newEntry)
    
    db.session.commit()


    # Add the extra entry attributes if they
    # were filled out.
    if newEntry.id is not None:
      
      if outlook is not None and outlook > 0:
        
        newOutlook = Entry(
                        val = outlook,
                        entry_type = 1,
                        parent_id = newEntry.id,
                        user_id = g.user
                      )
        
        db.session.add(newOutlook)
      
      if energy is not None and energy > 0:
        
        newEnergy = Entry(
                        val = energy,
                        entry_type = 2,
                        parent_id = newEntry.id,
                        user_id = g.user
                      )
        
        db.session.add(newEnergy)

      if focus is not None and focus > 0:
        
        newFocus = Entry(
                        val = focus,
                        entry_type = 3,
                        parent_id = newEntry.id,
                        user_id = g.user
                      )
        
        db.session.add(newFocus)
      
      db.session.commit()
    
    flash('New entry added.')
    
    return redirect(url_for('dashboard'))
    
  elif request.method == 'POST':

    flash('Something wasn’t right')
    
    
  
  now = datetime.now() # current date and time
  date_time = now.strftime("%A, %b. %d %Y")
  
  return render_template('entry/new.html', title='New entry', subhead=format(date_time), form=form)







@app.route('/entry/by/date/<date_str>')
def entry_by_date(date_str):

  try:

    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

    valid_date = True

  except ValueError:

    valid_date = False

    flash('{} is not valid date in the format YYYY-MM-DD'.format(date_str))


  if ( valid_date ):

    present = datetime.now().date()

    if ( date_obj <= present ):

      
      parent_entries = db.session.query(Entry)\
                      .with_entities(Entry.id)\
                      .filter(
                        Entry.parent_id == 0,
                        extract('day', Entry.created_on) == date_obj.day
                      )
                      
      grouped_entries = db.session.query(Entry)\
                      .filter(
                        or_(
                          Entry.id.in_(parent_entries),
                          Entry.parent_id.in_(parent_entries),
                        )
                      )
                      
      entries = grouped_entries.all()

                      
      flash( [{i:v for i, v in r.__dict__.items() if i in r.__table__.columns.keys()} for r in grouped_entries] )
      
      flash( str( grouped_entries.statement.compile(dialect=sqlite.dialect()) ) )

    else:

      entries = False

      flash('date must be in the past')



  return render_template('entry/list.html', title='Entry by date', date_target=date_str, entries=entries)



