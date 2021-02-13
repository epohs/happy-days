from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import DecimalRangeField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')
    
    
class NewEntry(FlaskForm):
  overall = DecimalRangeField('Overall', places="1", validators=[DataRequired()])
  submit = SubmitField('Add entry')