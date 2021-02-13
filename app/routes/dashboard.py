from app import app
from app.models import Entry
from flask import g
from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user

@app.route('/dashboard')
def dashboard():
  
  if current_user.is_authenticated:
    
    g.user = current_user.get_id()
    
  else:
    
    return redirect(url_for('index'))
  
  recent_entries = Entry.query.filter_by(user_id=g.user).order_by(Entry.created_on.desc()).limit(30)
  
  
  return render_template('dashboard.html', title='Dashboard', recent_entries=recent_entries)