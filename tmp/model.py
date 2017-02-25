
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
    
    # from API
    vm_id = db.Column(db.Integer, nullable=False, primary_key=True) # vm_id for easy access urls
    name = db.Column(db.Text, nullable=True)
    place_type = db.Column(db.Text, nullable=True)
    img_url = db.Column(db.Text, nullable=True)
    descr = db.Column(db.Text, nullable=True)
    categoryIds = db.Column(db.Text, nullable=True)
    mission = db.Column(db.Text, nullable=True)

    # location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)

    # relationships
    # location = db.relationship('Location', backref='places')
    def __repr__(self):
        """Provide helpful represetration when printed"""
        return "<Place vm_id=%s, %s>" % (self.vm_id, self.name.encode('ascii', 'ignore'))


class Opportunity(db.Model):
    """Movie from ratings website."""

    __tablename__ = "opportunities"

    # from API
    vm_id = db.Column(db.Integer, nullable=False, primary_key=True) # vm_id for easy access urls
    img_url = db.Column(db.Text, nullable=True)
    parent_place = db.Column(db.Integer, db.ForeignKey('places.vm_id'), nullable=True)
    # location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=True)
    descr = db.Column(db.Text, nullable=True)
    title = db.Column(db.Text, nullable=True)
    tags = db.Column(db.Text, nullable=True)
    categoryIds = db.Column(db.Text, nullable=True)

    # from OG html pages (more trustful)
    opp_time = db.Column(db.Text, nullable=True)

    # relationships
    host_place = db.relationship('Place', backref='places')# linked to Place by place_id
    # location = db.relationship('Location', backref='locations')


    def __repr__(self):
        """Provide helpful represetration when printed"""
        return "<Opportunity title=%s vm_id=%s>" % (self.title,
                                                    self.vm_id)


# ================= Location tables ==========================================

class Location(db.Model):
    """docstring for Location"""
    __tablename__ = "locations"

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    # from htmls
    lat = db.Column(db.String(16), nullable=True)
    lng = db.Column(db.String(16), nullable=True)
    st_add1 = db.Column(db.String(128), nullable=True) # street address
    st_add2 = db.Column(db.String(128), nullable=True) # street address 2
    city = db.Column(db.String(32), nullable=True) # city
    zip_code = db.Column(db.Integer, nullable=True)
    # vm_id = db.Column(db.Integer, nullable=False) # file name which is a vm_id for the place or opportunity
    
    # relationships using placelocation and opportunitylocation as secondaries
    places = db.relationship("Place",
                            secondary="places_locations",
                            backref="locations")
    opportunities = db.relationship("Opportunity",
                                    secondary="opportunities_locations",
                                    backref="locations")

    def __repr__(self):
        return "<Location %s lat=%s, lng=%s>" %(self.location_id,
                                                self.lat,
                                                self.lng)

class PlaceLocation(db.Model):
    """Association table for places' locations"""

    __tablename__ = 'places_locations'
    place_location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    place_id = db.Column(db.Integer,
                         db.ForeignKey('places.vm_id'),
                         nullable=False)
    location_id = db.Column(db.Integer, 
                            db.ForeignKey('locations.location_id'),
                            nullable=False)



    def __repr__(self):
        return "<place_location place_id=%s, location_id=%s>" %(self.place_id,
                                                                self.location_id)

class OpportunityLocation(db.Model):
    """Association table for places' categories"""

    __tablename__ = 'opportunities_locations'
    opportunity_location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    opportunity_id = db.Column(db.Integer,
                         db.ForeignKey('opportunities.vm_id'),
                         nullable=False)
    location_id = db.Column(db.Integer, 
                            db.ForeignKey('locations.location_id'),
                            nullable=False)


# =============== Category tables ============================================

class Category(db.Model):
    """Categories"""

    __tablename__ = "categories"

    vm_id = db.Column(db.Integer, primary_key=True, nullable=False)
    category_name = db.Column(db.String(32), nullable=False)


    # relationships using placecategory and opportunitycategory as secondaries
    places = db.relationship("Place",
                                secondary="places_categories",
                                backref="categories")
    opportunities = db.relationship("Opportunity",
                                    secondary="opportunities_categories",
                                    backref="categories")

    def __repr__(self):
        """Provide helpful represetration when printed"""
        return "<Category category_id=%s %s>" % (self.vm_id,
                                                 self.category_name)


class PlaceCategory(db.Model):
    """Association table for places' categories"""

    __tablename__ = 'places_categories'
    place_category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    place_id = db.Column(db.Integer,
                         db.ForeignKey('places.vm_id'),
                         nullable=False)
    category_id = db.Column(db.Integer, 
                            db.ForeignKey('categories.vm_id'),
                            nullable=False)

class OpportunityCategory(db.Model):
    """Association table for opportunities' categories"""

    __tablename__ = 'opportunities_categories'
    opportunity_category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flat'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."

