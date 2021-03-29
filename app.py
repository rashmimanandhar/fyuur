#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from models import *
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify, abort



import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
import traceback




#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = Venue.query.all()
  places = Venue.query.distinct(Venue.city, Venue.state).all()
  data = []
  for place in places:
    venue_info = {
      'city': place.city,
      'state': place.state,
      'venues': []
    }

    place_venues = []
    for venue in venues:
      if venue.city == place.city and venue.state == place.state:
        num_upcoming_shows = []
        for show in venue.shows:
          if show.start_time > datetime.now():
            num_upcoming_shows.append(show)
        place_venues.append({
          'id': venue.id,
          'name': venue.name,
          'num_upcoming_shows': len(num_upcoming_shows)
        })
    venue_info['venues']=place_venues
    data.append(venue_info)

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  search_result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  data = []

  for result in search_result:
    data.append({
      "id": result.id,
      "name": result.name,
      "num_upcoming_shows": len(Show.query.filter(Show.venue_id == result.id).filter(Show.start_time > datetime.now()).all()),
    })
  
  response={
    "count": len(search_result),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
 
  venue_show = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).all()
  past_shows = []
  upcoming_shows = []
  for show in venue_show:
    show_info = {
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
      }
    if show.start_time < datetime.now():
      past_shows.append(show_info)
    else:
      upcoming_shows.append(show_info)

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows":past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
 
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form, meta={'csrf': False})
  error = True
  if not form.validate():
    error = False
    try:
      name = form.name.data,
      city = form.city.data
      state = form.state.data
      address = form.address.data
      phone = form.phone.data
      genres = form.genres.data
      image_link = form.image_link.data
      facebook_link = form.facebook_link.data
      website = form.website.data
      seeking_talent = True if 'seeking_talent' in form else False 
      seeking_description = form.seeking_description.data

      venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
      
      db.session.add(venue)
      db.session.commit()
    except:
      error = True
      e = sys.exc_info()[0]
      traceback.print_exc() 
      print( "<p>Error: %s</p>" % e )
      flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      abort (400)
    else:
      flash('Venue ' + form.name.data + ' was successfully listed!')
  else:
    message = []
    for field, err in form.erros.items():
      message.append(field + ' ' + '|'.join(err))
    flash('Errors '+ str(message))
  
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = []
  artists = Artist.query.with_entities(Artist.id,Artist.name).all();
  for artist in artists:
    artist_info = {
      'id': artist.id,
      'name': artist.name
    }
    data.append(artist_info)
 
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  search_result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  data = []

  for result in search_result:
    data.append({
      "id": result.id,
      "name": result.name,
      "num_upcoming_shows": len(Show.query.filter(Show.artist_id == result.id).filter(Show.start_time > datetime.now()).all()),
    })
  
  response={
    "count": len(search_result),
    "data": data
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)
  artist_show = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).all()
  past_shows = []
  upcoming_shows = []
  for show in artist_show:
    show_info = {
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time.strftime('%Y-%m-%d %H:%M:%S')
      }
    if show.start_time < datetime.now():
      past_shows.append(show_info)
    else:
      upcoming_shows.append(show_info)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows":past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  error = True
  if not form.validate():
    error = False
    try:
      name = form.name.data
      city = form.city.data
      state = form.state.data
      phone = form.phone.data
      genres = form.genres.data,
      facebook_link = form.facebook_link.data
      image_link = form.image_link.data
      website = form.website.data
      seeking_venue = True if 'seeking_venue' in request.form else False
      seeking_description = form.seeking_description.data

      artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link, image_link=image_link, website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
      
      db.session.add(artist)
      db.session.commit()
    except:
      error = True
      e = sys.exc_info()[0]
      traceback.print_exc() 
      print( "<p>Error: %s</p>" % e )
      flash('An error occurred. Venue ' + reqData['name'] + ' could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      abort (400)
    else:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
      message = []
      for field, err in form.erros.items():
        message.append(field + ' ' + '|'.join(err))
      flash('Errors ' + str(message))
 
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = db.session.query(Show).join(Venue).join(Artist).all()
  data = []
  for show in shows:
    show_info = {
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
    }
    data.append(show_info);
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  error = False
  artist_id = request.form['artist_id']
  venue_id = request.form['venue_id']
  start_time = request.form['start_time']
  try:

    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    e = sys.exc_info()[0]
    traceback.print_exc() 
    print( "<p>Error: %s</p>" % e )
    flash('An error occurred. Venue ' + reqData['name'] + ' could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    flash('Show was successfully listed!')
  
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
