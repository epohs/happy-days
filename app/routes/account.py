from config import AdminUser
from app import app, db
from app.models import User, Entry
from app.forms import LoginForm, ChangePassword
from sqlalchemy import or_, func
from werkzeug.security import generate_password_hash
from flask import render_template, flash, get_flashed_messages, url_for, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
import re


def login_check():
  
  # Make sure at least one user exists
  # If not, redirect to the setup page.
  try:
    
    user = User.query.one()
    
  except:
    
    return [False, 'setup']

    
  # If current user is logged in redirect to
  # the dashboard, otherwise to log in page. 
  if current_user.is_authenticated:
    
    return [True, 'dashboard']
    
  else:
    
    return [False, 'login']



    


def check_email_format(str):

  regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
  
  return re.search(regex, str)







@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    
    form.validate_on_submit()

    if request.method == 'POST':
        
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):

            flash('Invalid username or password')

        else:

            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))

    elif request.method == 'POST':

        flash('Something wasn’t right')


    return render_template('login.html', title='Sign In', form=form)


    
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))






@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
  
  num_entries = func.count(Entry.id).label('num_entries')
  day = func.strftime('%m/%d/%Y', Entry.created_on).label('day')
  
  # Get a count of all top level entries
  # by the current user, and the date of
  # the first entry.
  my_entries = db.session.query(
      num_entries,
      day
    ).filter_by(
        user_id = current_user.get_id(),
        parent_id = 0,
        entry_type = 0
      ).order_by(Entry.created_on.asc()).first()
      
  form = ChangePassword()
  
  # We validate the form and make sure it was
  # the change-password form that was submitted
  if form.validate_on_submit() and (request.form.get('form_id') == 'change-password'):
  
    current_user.password = generate_password_hash(
                          request.form.get('password'),
                          method='sha256'
                        )
                        
    db.session.commit()
    
    flash('Password updated')
  
  return render_template('account.html', title='Your Account', my_entries=my_entries, form=form)





@app.route('/setup')
def setup():
  
  modify_user = False
  update_confirmed = False
  user_modified = False
  warnings = 0
  
  # Check the validity of the Admin User in config file.
  if ( not AdminUser.USER or len(AdminUser.USER) < 5 ):
    
    flash('Username empty')
    valid_user = False
    warnings += 1
    
  else:
    
    valid_user = True


  if ( not AdminUser.PASS or len(AdminUser.PASS) < 6 ):
    
    flash('Password empty')
    valid_pass = False
    warnings += 1
    
  else:
    
    valid_pass = True


  if ( not AdminUser.EMAIL or not check_email_format(AdminUser.EMAIL) ):
    
    flash('Email empty')
    valid_email = False
    warnings += 1
    
  else:
    
    valid_email = True
    
  
    
  # If we have less than 3 error messages
  # the user format is okay.
  if ( warnings < 3 ):
    
    modify_user = True
    

    
  ## Here we go
  if ( modify_user and (request.args.get('modify_user') == 'yes') ):
    
    user = User.query.filter(
                          or_(
                            User.username == str(AdminUser.USER),
                            User.email == str(AdminUser.EMAIL)
                        )).first()

    # No matching user was found in the database
    # so we will insert a new user.
    if ( user is None and (warnings <= 0) ):
      
      newUser = User(username = AdminUser.USER,
                      email = AdminUser.EMAIL,
                      password = generate_password_hash(
                        AdminUser.PASS,
                        method='sha256'
                      )
                    )

      db.session.add(newUser)
      
      flash('New user added.')
      
    elif ( user is None and (warnings > 0) ):
      
      flash('Enter all Admin User data in config.py to add your first user.')
    
    # A user matching AdminUser in config.py was
    # found in the db, so we will update it.
    else:
      
      if valid_user:
  
        user.username = AdminUser.USER
      
      if valid_pass:
        user.password = generate_password_hash(
                            AdminUser.PASS,
                            method='sha256'
                          )

      if valid_email:
  
        user.email = AdminUser.EMAIL


      flash('User updated.') 
      
    db.session.commit()
    
    user_modified = True
  
  # No valid data in config.py means we don't
  # have enough info to update the database.
  elif( warnings >= 3 ):
    
    flash('Database will not be updated.')


  
  return render_template('setup.html', title='Setup', modify_user=modify_user, user_modified=user_modified)

    