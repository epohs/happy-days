from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import DecimalRangeField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')
    
    
class NewEntry(FlaskForm):
  
  overall = DecimalRangeField('Overall', places="1", 
                              validators=[DataRequired(), NumberRange(min=0, max=5)])
  outlook = DecimalRangeField('Outlook', places="1", 
                              validators=[NumberRange(min=0, max=5)])
  energy = DecimalRangeField('Energy level', places="1", 
                              validators=[NumberRange(min=0, max=5)])
  focus = DecimalRangeField('Focus', places="1", 
                              validators=[NumberRange(min=0, max=5)])
  submit = SubmitField('Add entry')