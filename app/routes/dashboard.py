from app import app, db, assets
from app.models import Entry
from flask import g
from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user
from sqlalchemy import func

@app.route('/dashboard')
def dashboard():
  
  if current_user.is_authenticated:
    
    g.user = current_user.get_id()
    
  else:
    
    return redirect(url_for('index'))


  day = func.strftime('%m/%d/%Y', Entry.created_on).label('day')
  avg = func.avg(Entry.val).label('avg')
  num_entries = func.count(Entry.id).label('num_entries')
  
  recent_entries = db.session.query(
    day,
    avg,
    Entry.created_on,
    num_entries
  ).filter_by(
      user_id = g.user,
      parent = 0,
      entry_type_id = 0
    ).order_by(day.desc()).group_by(day).limit(30)
  
  
  return render_template('dashboard.html', title='Dashboard', recent_entries=recent_entries)