from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.fields.html5 import DecimalRangeField
from wtforms.validators import DataRequired, NumberRange, EqualTo

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(message="Username is required")])
  password = PasswordField('Password', validators=[DataRequired(message="Password is required")])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')


class ChangePassword(FlaskForm):
  form_id = HiddenField('Form ID', default='change-password')
  password = PasswordField('New Password', [DataRequired(), EqualTo('confirm', message='Passwords must match')])
  confirm  = PasswordField('Repeat Password')
  submit = SubmitField('Change Password')

 
class NewEntry(FlaskForm):
  
  overall = DecimalRangeField('Overall', places="1", 
                              validators=[DataRequired(message="Overall is required"),
                                         NumberRange(min=0.5, max=5, message="Out of range")])
  outlook = DecimalRangeField('Outlook', places="1", 
                              validators=[NumberRange(min=0, max=5, message="Out of range")])
  energy = DecimalRangeField('Energy level', places="1", 
                              validators=[NumberRange(min=0, max=5, message="Out of range")])
  focus = DecimalRangeField('Focus', places="1", 
                              validators=[NumberRange(min=0, max=5, message="Out of range")])
  submit = SubmitField('Add entry')


