from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
class EventPostForm(FlaskForm):
    # Nije moguc prazan text i title
    # datum se uzima iz modela automatski
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    city=StringField('City', validators=[DataRequired()])
    time_start=StringField('Time_Start', validators=[DataRequired()])
    time_end=StringField('Time_End', validators=[DataRequired()])
    address=StringField('Address', validators=[DataRequired()])
    contact=StringField('Contact', validators=[DataRequired()])
    pic = FileField('Pic', validators=[FileRequired()])
    submit = SubmitField('Done')
    
class CommentForm(FlaskForm):
    comment = StringField('post', validators=[DataRequired()])
    submit = SubmitField('Done')

class contactnow(FlaskForm):
    # Nije moguc prazan text i title
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Done')
