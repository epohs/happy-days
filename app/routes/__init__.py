from flask import render_template, url_for, redirect, request
from app import app, assets
from flask_login import current_user
from app.routes import account
from app.routes import dashboard
from app.routes import entries
from flask_assets import Bundle


#app.url_map.strict_slashes = False

def make_asset_bundles():
  
  css = Bundle('css/reset.css', 'css/fonts.css', 'css/colors.css', 'css/base.css', 'css/responsive.css',
              filters='cssmin', output='packed/app.css')
    
  js = Bundle('js/base.js', 'js/entries.js',
              filters='jsmin', output='packed/app.js')

  assets.register('css_all', css)              
  assets.register('js_all', js)


  



@app.before_request
def clear_trailing():

    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])




@app.route('/')
def index():
  
  logged_in = account.login_check()
  
  return redirect(url_for(logged_in[1]))
  
  



@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html', title='Page not found.. play minesweeper instead.'), 404