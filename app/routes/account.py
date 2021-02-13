from config import AdminUser
from app import app, db
from app.models import User
from app.forms import LoginForm
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash
from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user, login_user, logout_user
import re


def login_check():
  
  # Make sure at least one user exists
  # If not, redirect to the setup page.
  try:
    
    user = User.query.one()
    
  except NoResultFound as e:
    
    return [False, 'setup']

    
  # If current user is logged in redirect to
  # the dashboard, otherwise log in. 
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

    if request.method == 'POST' and form.validate_on_submit():
        
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
def logout():
    logout_user()
    return redirect(url_for('index'))




@app.route('/setup')
def setup():
  
  modify_user = True
  update_confirmed = False
  #user_modified = True if (request.args['user_modified'] == 'true') else False
  user_modified = False
  bullets = []
  
  # Check the validity of the Admin User in config file.
  if ( not AdminUser.USER or len(AdminUser.USER) < 5 ):
    
    bullets.append( {'text': 'Username required'} )
    
  if ( not AdminUser.PASS or len(AdminUser.PASS) < 6 ):
    
    bullets.append( {'text': 'Password required'} )
    
  if ( not AdminUser.EMAIL or not check_email_format(AdminUser.EMAIL) ):
    
    bullets.append( {'text': 'Email required'} )
    
  
  # If we don't have any warning bullets
  # the user format is okay.
  if ( len(bullets) <= 0 ):
    
    modify_user = True
    

  ## Here we go
  if ( modify_user and (request.args.get('modify_user') == 'yes') ):
    
    user = User.query.filter_by(username=AdminUser.USER).first()

    if ( user is None ):
      
      newUser = User(username = AdminUser.USER,
                      email = AdminUser.EMAIL,
                      password = generate_password_hash(
                        AdminUser.PASS,
                        method='sha256'
                      )
                    )

      db.session.add(newUser)
      
    else:
      
      user.email = AdminUser.EMAIL
      user.password = generate_password_hash(
                          AdminUser.PASS,
                          method='sha256'
                        )
      
    db.session.commit()
    
    user_modified = True


  
  return render_template('setup.html', title='Setup', bullets=bullets, modify_user=True, user_modified=user_modified)

    