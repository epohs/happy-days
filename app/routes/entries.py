from app import app
from flask import render_template, flash, url_for, redirect, request

@app.route('/new')
def new_entry():
  return render_template('entry/new.html', title='New entry')