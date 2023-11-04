from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, EmailField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    month = IntegerField('Month', validators=[DataRequired(), NumberRange(min=1, max=12)])
    day = IntegerField('Day', validators=[DataRequired(), NumberRange(min=1, max=31)])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=2000, max=10000)])
    attendees = EmailField('Emails to Invite', validators=[DataRequired()])
    games = TextAreaField('Games', validators=[DataRequired()])
    food = TextAreaField('Food', validators=[DataRequired()])
    nut_allergy = BooleanField('Nut Allergy?', validators=[DataRequired()])
    formality = SelectField('Formality', choices=['Casual', 'Fancy'])

    submit = SubmitField('Post')
