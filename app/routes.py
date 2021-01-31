from flask import render_template, flash, url_for, redirect, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from config import AdminUser

#app.url_map.strict_slashes = False


@app.before_request
def clear_trailing():

    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])




@app.route('/')
def index():
    bullets = [
        {
            'text': 'Links',
            'href': url_for('links')
        }
    ]
    return render_template('index.html', title='Hello, World.', bullets=bullets)




@app.route('/links')
def links():

    bullets = [
        {
            'text': 'Flask, nginx, gunicorn, supervisor',
            'href': 'https://medium.com/ymedialabs-innovation/deploy-flask-app-with-nginx-using-gunicorn-and-supervisor-d7a93aa07c18'
        },
        {
            'text': 'Gunicorn',
            'href': 'http://docs.gunicorn.org/en/19.0/settings.html'
        },
        {
            'text': 'Flask tutorial',
            'href': 'https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world'
        },
        {
            'text': 'Minesweeper',
            'href': request.host_url + 'fuh'
        },
        {
            'text': 'Home',
            'href': url_for('index')
        }
    ]

    return render_template('index.html', title='Links', bullets=bullets)





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



@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html', title='Page not found.. play minesweeper instead.'), 404