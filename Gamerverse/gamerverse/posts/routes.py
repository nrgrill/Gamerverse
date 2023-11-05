from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from gamerverse import db, mail
from gamerverse.models import Event, User
from gamerverse.posts.forms import EventForm
from flask_mail import Message
import re

posts = Blueprint('posts', __name__)

import urllib.parse

def location_to_google_maps_link(location):
    # Replace spaces with '+' and encode special characters
    formatted_location = urllib.parse.quote(location.replace(" ", "+"))

    # Construct the Google Maps URL
    google_maps_url = f"https://www.google.com/maps/place/{formatted_location}"

    return google_maps_url

@posts.route("/post/<int::post_id>/discord>")
def discord_connector(id):
    event = Event.query.get_or_404(id)
    return event

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = EventForm()
    form.attendees.choices = [(g.email, g.username) for g in User.query.order_by('username')]
    if form.validate_on_submit():
        # new_attendees = str(form.attendees.data)
        # new_attendees = replace("'[]", "", str(form.attendees.data))
        new_attendees = str(form.attendees.data).replace("[", '')
        new_attendees = new_attendees.replace("]", '')
        new_attendees = new_attendees.replace("'", '')
        if form.location.data != 'Online':
            maps_link = location_to_google_maps_link(form.location.data)
        else:
            maps_link = "#"
        
        post = Event(title=form.title.data, description=form.description.data, author=current_user, map_link=maps_link,
                     start_date=form.start_date.data, end_date=form.end_date.data, attendees=new_attendees, location=form.location.data,
                     games=form.games.data, food=form.food.data, nut_allergy=form.nut_allergy.data, formality=form.formality.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Event.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    event = Event.query.get_or_404(post_id)
    if event.author != current_user:
        abort(403)
    form = EventForm()
    form.attendees.choices = [(g.email, g.username) for g in User.query.order_by('username')]
    if form.validate_on_submit():
        db.session.delete(event)
        new_attendees = str(form.attendees.data).replace("[", '')
        new_attendees = new_attendees.replace("]", '')
        new_attendees = new_attendees.replace("'", '')
        if form.location.data != 'Online':
            maps_link = location_to_google_maps_link(form.location.data)
        else:
            maps_link = "#"
        new_event = Event(title=form.title.data, description=form.description.data, author=current_user, map_link=maps_link,
                     start_date=form.start_date.data, end_date=form.end_date.data, attendees=new_attendees, location=form.location.data,
                     games=form.games.data, food=form.food.data, nut_allergy=form.nut_allergy.data, formality=form.formality.data)
        db.session.add(new_event)
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=new_event.id))
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
        form.start_date.data = event.start_date
        form.end_date.data = event.end_date
        form.location.data = event.location
        form.attendees.data = event.attendees
        form.games.data = event.games
        form.food.data = event.food
        form.nut_allergy.data = event.nut_allergy
        form.formality.data = event.formality
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    event = Event.query.get_or_404(post_id)
    if event.author != current_user:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

# Parameter needs to be a list of valid emails
def send_invite_email(attendeeList):
    for i in attendeeList:
        msg = Message('Inited to a PARTY', 
                sender='thegamerversehelp@gmail.com', 
                recipients=[i])
        msg.body = f'''You have been invited to a new gamer event. To view the details, please login to your account. 
        '''

#@posts.route("/example", methods=["GET", "POST"])
#def example():
#  form = ExampleForm()
#  # populate the forms dynamically with the choices in the database
#  form.check_options.choices = [(c.id, c.desc) for c in Choices.query.all()]
#  # if it's a post request and we validated successfully
#  if request.POST and form.validate_on_submit():
#    # get our choices again, could technically cache these in a list if we wanted but w/e
#    c_records = Choices.query.all()
#    # need a list to hold our choices
#    accepted = []
#    # looping through the choices, we check the choice ID against what was passed in the form
#    for choice in c_records:
#      # when we find a match, we then append the Choice object to our list
#      if choice.id in form.check_options.data:
#        accepted.append(choice)
#    # now all we have to do is update the users choices records
#    user.choices = accepted
#    db.session.add(user)
#    db.session.commit(user)
#  else:
#    # tell the form what's already selected
#    form.choices.data = [c.id for c in user.choices]
#    return render_template('example.html', form=form)