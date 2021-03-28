from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=True)
    genres = db.Column(db.ARRAY(db.String()))
    shows = db.relationship(
        'Show',
        backref='venue',
        lazy='joined',
        cascade="all, delete"
    )

    def __repr__(self):
      return f'<Venue: {self.id}, name: {self.name}, city:{self.city}, state: {self.state}, address: {self.address}, phone: {self.phone}, image_link: {self.image_link},facebook_link: {self.facebook_link}, website: {self.website}, seeking_talent: {self.seeking_talent}, seeking_desc: {self.seeking_description}, genres: {self.genres}>'


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(250))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Show',
                            backref=db.backref('artist', lazy=True))

    def __repr__(self):
      return f'<Artist: {self.id}, name: {self.name}, city:{self.city}, state: {self.state}, phone: {self.phone}, image_link: {self.image_link},facebook_link: {self.facebook_link}, genres: {self.genres}>'


class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)

  def __repr__(self):
    return f'<Show: {self.id}, Artist: {self.artist_id}, venue:{self.venue_id}, start_time: {self.start_time}>'
