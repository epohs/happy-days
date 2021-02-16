from app import app, db, assets
from app.models import Entry
from flask import g
from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user
from sqlalchemy import func
from datetime import datetime, timedelta 
import math

@app.route('/dashboard')
def dashboard():
  
  if current_user.is_authenticated:
    
    g.user = current_user.get_id()
    
  else:
    
    return redirect(url_for('index'))


  day = func.strftime('%m/%d/%Y', Entry.created_on).label('day')
  avg = func.avg(Entry.val).label('avg')
  num_entries = func.count(Entry.id).label('num_entries')
  
  current_time = datetime.utcnow()
  thirty_days_ago = current_time - timedelta(days=30)
  days_ago = (func.julianday(current_time) - func.julianday(Entry.created_on)).label('days_ago')
  
  
  
  recent_entries = db.session.query(
    day,
    avg,
    Entry.created_on,
    days_ago,
    num_entries
  ).filter(Entry.created_on >= thirty_days_ago)\
    .filter_by(
      user_id = g.user,
      parent = 0,
      entry_type_id = 0
    ).order_by(day.desc()).group_by(day).all()




  # New entries object that has placeholders
  # for empty rows.
  entries_in_range = []

  # Loop through entire day range.
  # Search query result object.
  # If no entries found in that day
  # Add an emtpy flag.
  for day_ago in range(30 + 1): 
    
    # Filter SQLAlchemy Results Object to find
    # result matching the day_ago in our loop.
    # Convert KeyedTuple object using _asdict()
    day_in_range = [v._asdict() for v in recent_entries if math.floor(v.days_ago) == day_ago]
    
    if ( len(day_in_range) ):
      
      # Result matching day_ago found.
      # Append to our new list
      entries_in_range.append(day_in_range)
      
    else:
      
      # Result didn't match this day_ago.
      # Append our empty flag.
      entries_in_range.append([{'has_no_entry': True}])
  

  
  return render_template('dashboard.html', title='Dashboard', entries_by_day=entries_in_range)