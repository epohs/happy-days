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
                        entry_type_id = 1,
                        parent = newEntry.id,
                        user_id = g.user
                      )
        
        db.session.add(newOutlook)
      
      if energy is not None and energy > 0:
        
        newEnergy = Entry(
                        val = energy,
                        entry_type_id = 2,
                        parent = newEntry.id,
                        user_id = g.user
                      )
        
        db.session.add(newEnergy)

      if focus is not None and focus > 0:
        
        newFocus = Entry(
                        val = focus,
                        entry_type_id = 3,
                        parent = newEntry.id,
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
  
  return render_template('entry/new.html', title='New entry - {}'.format(date_time), form=form)