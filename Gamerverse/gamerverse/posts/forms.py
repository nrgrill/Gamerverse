from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField, EmailField, BooleanField, SelectField, IntegerField, DateField, SelectMultipleField,DateTimeLocalField
from wtforms.validators import DataRequired, NumberRange, ValidationError, StopValidation
from datetime import datetime
from wtforms import widgets
from wtforms.fields import SelectMultipleField
from gamerverse.models import Event, User

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateTimeLocalField('Start Date and Time', format="%Y-%m-%dT%H:%M",validators=[DataRequired()])
    end_date = DateTimeLocalField('End Date and Time', format="%Y-%m-%dT%H:%M",validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()], default='Online')
    attendees = SelectMultipleField('People to Invite (ctrl + click)', validate_choice=False)
    games = TextAreaField('Games', validators=[DataRequired()])
    food = TextAreaField('Food', validators=[DataRequired()])
    nut_allergy = BooleanField('Nut Allergy?')
    formality = SelectField('Formality', choices=['Casual', 'Fancy'])

    submit = SubmitField('Create')   

    def validate(self):
        current_date = datetime.now()
        if not super().validate():
            return False
        if self.start_date.data < current_date:
            self.start_date.errors.append('Must be in the Future!')
            return False
        return True
"""
def get_attendees():
    
    return [(g.email, g.username) for g in User.query.order_by('username')]

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag='ol', prefix_label=False)
    option_widget = widgets.CheckboxInput()

class MultiCheckboxAtLeastOne():
    def __init__(self, message=None):
        if not message:
            message = 'At least one option must be selected.'
        self.message = message

    def __call__(self, form, field):
        if len(field.data) == 0:
            raise StopValidation(self.message)

class RegistrationForm(FlaskForm):
    language = MultiCheckboxField('Language', choices=get_attendees(), validators=[MultiCheckboxAtLeastOne()], coerce=int)

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    
class ExampleForm(FlaskForm):
    choices = MultiCheckboxField('Routes', coerce=int)
    submit = SubmitField("Set User Choices")"""