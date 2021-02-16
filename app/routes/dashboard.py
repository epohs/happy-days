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
  # last_month = filter(Entry.created_on >= thirty_days_ago)
  
  # current_time = datetime.datetime.utcnow()
  # ten_weeks_ago = current_time - datetime.timedelta(weeks=10)
  # WHERE date BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime');
  # .filter(User.birthday <= '1988-01-17').filter(User.birthday >= '1985-01-17')
  
  recent_entries = db.session.query(
    day,
    avg,
    Entry.created_on,
    days_ago,
    num_entries
  ).filter(Entry.created_on >= thirty_days_ago).\
    filter_by(
      user_id = g.user,
      parent = 0,
      entry_type_id = 0
    ).order_by(day.desc()).group_by(day).all()
    
  
  #entries_map = [x for x in recent_entries if math.floor(x.days_ago) == 2]

  
  #flash( team_map )
  
  # Add emtpy flag
  # for entry in recent_entries: 
  for day_ago in reversed(range(30 + 1)): 
    #date = entry.__dict__['days_ago']
    #i.__dict__['date_modified'] = date.replace('/', '-')
    
    if ( not len([x for x in recent_entries if math.floor(x.days_ago) == day_ago]) ):
      
      flash('Nothing {} days ago'.format(day_ago))
  
  
  return render_template('dashboard.html', title='Dashboard', recent_entries=recent_entries)