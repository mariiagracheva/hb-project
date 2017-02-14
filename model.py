
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

    place_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    vm_id = db.Column(db.Integer, nullable=False) # vm_id for easy access urls
    name = db.Column(db.String(64), nullable=False)
    latitude = db.Column(db.Numeric(6, 4, True))
    longitude = db.Column(db.String(64), nullable=True)
    street_add1 = db.Column(db.Integer, nullable=True) # street address
    street_add2 = db.Column(db.String(15), nullable=True) # street address 2
    city = db.Column(db.String(15), nullable=True) # city
    zip_code = db.Column(db.Integer(64), nullable=True)
    description = db.Column(db.String(512), nullable=True)
    place_type = db.Column(db.String(64), nullable=True)
    imgurl = db.Column(db.String(128), nullable=True)


    def __repr__(self):
        """Provide helpful represetration when printed"""
        return "<Place id=%s vm_id=%s, %s>" % (self.place_id, self.vm_id, self.name)


class Opportunity(db.Model):
    """Movie from ratings website."""

    __tablename__ = "opportunities"

    opp_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    vm_id = db.Column(db.Integer, nullable=False) # vm_id for easy access urls
    time = db.Column(db.String, nullable=False)
    address = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    img_url = db.Column(db.String(256), nullable=True)
    opp_type = db.Column(db.String(8), nullable=True)
    title = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        """Provide helpful represetration when printed"""
        return "<Opportunity opp_id=%s title=%s vm_id=%s>" % (self.opp_id,
                                                            self.title,
                                                            self.vm_id)


class Category(db.Model):
    """Categories"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(32), nullable=True)

    def __repr__(self):
        """Provide helpful represetration when printed"""
        return "<Category category_id=%s %s>" % (self.category_id,
                                                 self.category_name)

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