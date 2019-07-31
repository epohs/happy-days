from flask import render_template, url_for
from app import app

#app.url_map.strict_slashes = False


@app.before_request
def clear_trailing():
    from flask import redirect, request

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
            'text': 'Home',
            'href': url_for('index')
        }
    ]

    return render_template('index.html', title='Links', bullets=bullets)
