
"""Models and database functions for VolunteerPlaces project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Place(db.Model):
    """User of ratings website."""

    __tablename__ = "places"

    # place_id = db.Column(db.Integer, autoincrement=True)
    
    # from API
    vm_id = db.Column(db.Integer, nullable=False, primary_key=True) # vm_id for easy access urls
    name = db.Column(db.String(64), nullable=False)
    place_type = db.Column(db.String(64), nullable=True)
    img_url = db.Column(db.String(128), nullable=True)
    descr = db.Column(db.String(512), nullable=True)
    
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)

    # relationships
    location = db.relationship('Location', backref='locations')


    def __repr__(self):
        """Provide helpful represetration when printed"""
        return "<Place vm_id=%s, %s>" % (self.vm_id, self.name)


class Opportunity(db.Model):
    """Movie from ratings website."""

    __tablename__ = "opportunities"

    # opp_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # from API
    vm_id = db.Column(db.Integer, nullable=False, primary_key=True) # vm_id for easy access urls
    img_url = db.Column(db.String(256), nullable=True)
    parent_place = db.Column(db.Integer, db.ForeignKey('places.vm_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    availability = db.Column(db.String(512), nullable=True) # json-string
    
    # from OG html pages (more trustful)
    time = db.Column(db.String(128), nullable=True)
    descr = db.Column(db.String(256), nullable=True)
    opp_type = db.Column(db.String(8), nullable=True)
    title = db.Column(db.String(128), nullable=True)

    # relationships
    host_place = db.relationship('Place', backref='places')# linked to Place by place_id
    location = db.relationship('Location', backref='locations')


    def __repr__(self):
        """Provide helpful represetration when printed"""
        return "<Opportunity title=%s vm_id=%s>" % (self.title,
                                                    self.vm_id)

class Location(object):
    """docstring for Location"""
    __tablename__ = "locations"

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    lat = db.Column(db.Numeric(6, 4, True), nullable=True)
    lng = db.Column(db.Numeric(6, 4, True) nullable=True)
    st_add1 = db.Column(db.Integer, nullable=True) # street address
    st_add2 = db.Column(db.String(15), nullable=True) # street address 2
    city = db.Column(db.String(15), nullable=True) # city
    zip_code = db.Column(db.Integer(64), nullable=True)
    vm_id = db.Column(db.Integer, nullable=False) # file name which is a vm_id for the place or opportunity
    # relationships

    def __repr__(self):
        return "<Location %s lat=%s, lng=%s>" %(self.location_id,
                                                self.lat,
                                                self.lng)

class Category(db.Model):
    """Categories"""

    __tablename__ = "categories"

    vm_id = db.Column(db.Integer, primary_key=True, nullable=False)
    category_name = db.Column(db.String(32), nullable=False)


    # relationships using placecategory and opportunitycategory as secondaries
    places = db.relationship("PlaceCategory",
                                secondary="places_categories",
                                backref="categories")
    opportunities = db.relationship("OpportunityCategory",
                                    secondary="opportunities_categories",
                                    backref="categories")

    def __repr__(self):
        """Provide helpful represetration when printed"""
        return "<Category category_id=%s %s>" % (self.vm_id,
                                                 self.category_name)


class PlaceCategory(db.Model):
    """Association table for places' categories"""

    __tablename__ = 'places_categories'
    place_category_id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer,
                         db.ForeignKey('places.vm_id'),
                         nullable=False)
    category_id = db.Column(db.Integer, 
                            db.ForeignKey('categories.vm_id'),
                            nullable=False)

class OpportunityCategory(db.Model):
    """Association table for opportunities' categories"""

    __tablename__ = 'opportunities_categories'
    opportunity_category_id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer,
                         db.ForeignKey('opportunities.vm_id'),
                         nullable=False)
    category_id = db.Column(db.Integer, 
                            db.ForeignKey('categories.vm_id'),
                            nullable=False)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///volunteer'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."