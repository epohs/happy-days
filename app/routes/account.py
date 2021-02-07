from config import AdminUser
from app import app
from app.models import User
from app.forms import LoginForm
from sqlalchemy.orm.exc import NoResultFound
from flask import render_template, flash, url_for, redirect, request
from flask_login import current_user, login_user, logout_user



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
    return render_template('setup.html', title='Setup', user=AdminUser)

    