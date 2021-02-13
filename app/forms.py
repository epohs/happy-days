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
  overall = DecimalRangeField('Overall', places="1", validators=[DataRequired(), NumberRange()])
  outlook = DecimalRangeField('Outlook', places="1", validators=[NumberRange()])
  energy = DecimalRangeField('Energy level', places="1", validators=[NumberRange()])
  focus = DecimalRangeField('Focus', places="1", validators=[NumberRange()])
  submit = SubmitField('Add entry')