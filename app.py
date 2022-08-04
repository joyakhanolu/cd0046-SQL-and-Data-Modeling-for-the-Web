#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from forms import *
from flask_migrate import Migrate
from models import Artist, Venue, Show, db
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = -1
  if isinstance(value, str):
    date = dateutil.parser.parse(value)
  else:
    date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data = Venue.query.distinct(Venue.city, Venue.state).all()
  venues = Venue.query.all()
  return render_template('pages/venues.html', areas=data, venues=venues)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response = Venue.query.filter(Venue.name.ilike('%' + request.form.get('search_term') + '%')).all()
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = Venue.query.get(venue_id)
  shows = db.session.query(
    Show.venue_id,
    Artist.image_link,
    Artist.id,
    Artist.name,
    Show.start_time,
    Venue.name,
    Venue.image_link,
    ).join(Venue).join(Artist).all()
  upcoming_shows = []
  for show in shows:
    if show[0] == venue_id:
      if show[4] > datetime.now():
        upcoming_shows.append(show)
  past_shows = []
  for show in shows:
    if show[0] == venue_id:
      if show[4] < datetime.now():
        past_shows.append(show)  

  return render_template('pages/show_venue.html', venue=data, upcoming_shows=upcoming_shows, past_shows=past_shows)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  form = VenueForm()
  try:
    
    name=request.form.get('name'),
    city=request.form.get('city'),
    state=request.form.get('state'),
    address=request.form.get('address'),
    phone=request.form.get('phone'),
    genres=request.form.get('genres'),
    facebook_link=request.form.get('facebook_link'),
    image_link=request.form.get('image_link'),
    website_link=request.form.get('website_link'),
    seeking_talent=request.form.get('seeking_talent'),
    seeking_description=request.form.get('seeking_description'),
    

    venue = Venue(
      name=name,
      city=city,
      state=state,
      address=address,
      phone=phone,
      image_link=image_link,
      genres=genres,
      facebook_link=facebook_link,
      website=website_link,
      looking_for_talent=seeking_talent,
      seeking_description=seeking_description
    )
    

    
  # TODO: modify data to be the data object returned from db insertion

    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()

    flash('Venue ' + venue.name + ' was successfully deleted!')


  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + venue.name + ' could not be deleted.')

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response = Artist.query.filter(Artist.name.ilike('%' + request.form.get('search_term') + '%')).all()
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  data = Artist.query.get(artist_id)
  shows = db.session.query(
    Show.artist_id,
    Show.venue_id,
    Show.start_time,
    Venue.name,
    Venue.image_link,
    ).join(Venue).all()
  upcoming_shows = []
  for show in shows:
    if show[0] == artist_id:
      if show[2] > datetime.now():
        upcoming_shows.append(show)
  past_shows = []
  for show in shows:
    if show[0] == artist_id:
      if show[2] < datetime.now():
        past_shows.append(show)  

      
  return render_template('pages/show_artist.html', artist=data, shows=shows, past_shows=past_shows, upcoming_shows=upcoming_shows)


@app.route('/artists/<artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a artist_id, and using
  # SQLAlchemy ORM to delete an artist. Handle cases where the session commit could fail.
  try:
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()

    flash('Venue ' + artist.name + ' was successfully deleted!')


  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + artist.name + ' could not be deleted.')

  # BONUS CHALLENGE: Implement a button to delete an Artist on a Artist Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))



#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist=Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  Artist.query.get(artist_id)
  try:
    name=request.form.get('name'),
    city=request.form.get('city'),
    state=request.form.get('state'),
    phone=request.form.get('phone'),
    genres=request.form.get('genres'),
    facebook_link=request.form.get('facebook_link'),
    image_link=request.form.get('image_link'),
    website_link=request.form.get('website_link'),
    seeking_venue=request.form.get('seeking_venue'),
    seeking_description=request.form.get('seeking_description'),

    artist = Artist(
      name=name,
      city=city,
      state=state,
      phone=phone,
      genres=genres,
      facebook_link=facebook_link,
      image_link=image_link,
      website_link=website_link,
      seeking_venue=seeking_venue,
      seeking_description=seeking_description
    )
  # artist record with ID <artist_id> using the new attributes

    db.session.commit()

  except:
    db.session.rollback()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue=Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    venue = Venue.query.get(venue_id)
    name=request.form.get('name'),
    city=request.form.get('city'),
    state=request.form.get('state'),
    phone=request.form.get('phone'),
    genres=request.form.get('genres'),
    facebook_link=request.form.get('facebook_link'),
    image_link=request.form.get('image_link'),
    website_link=request.form.get('website_link'),
    seeking_talent=request.form.get('seeking_talent'),
    seeking_description=request.form.get('seeking_description'),

    venue = Venue(
      name=name,
      city=city,
      state=state,
      phone=phone,
      genres=genres,
      facebook_link=facebook_link,
      image_link=image_link,
      website_link=website_link,
      seeking_talent=seeking_talent,
      seeking_description=seeking_description
    )

    db.session.commit()

  except:
    db.session.rollback()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  try:
    form = ArtistForm()
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    genres = request.form.get('genres')
    facebook_link = request.form.get('facebook_link')
    image_link = request.form.get('image_link')
    website_link = request.form.get('website_link')
    seeking_venue = request.form.get('seeking_venue')
    seeking_description = request.form.get('seeking_description')

    artist = Artist(
      name=name,
      city=city,
      state=state,
      phone=phone,
      genres=genres,
      facebook_link=facebook_link,
      image_link=image_link,
      website_link=website_link,
      looking_for_venues=seeking_venue,
      seeking_description=seeking_description
    )

    db.session.add(artist)
    db.session.commit()
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.

  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  data = db.session.query(
    Show.venue_id,
    Venue.name,
    Show.artist_id,
    Show.start_time,
    Artist.name,
    Artist.image_link
  ).join(Venue).join(Artist).all()
  for datas in data:
    print(datas[1])
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    form = ShowForm()
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')

    show = Show(
      artist_id=artist_id,
      venue_id=venue_id,
      start_time=start_time
    )

    db.session.add(show)
    db.session.commit()

    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')

  finally:
    db.session.close()

  # on successful db insert, flash success

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
