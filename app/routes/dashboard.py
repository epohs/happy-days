from app import app
from flask import render_template, flash, url_for, redirect, request

@app.route('/dashboard')
def dashboard():
  return render_template('dashboard.html', title='Dashboard')