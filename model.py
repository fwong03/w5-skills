"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Part 1: Compose ORM

class Model(db.Model):

    __tablename__ = "models"

    model_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, nullable=False)

    # "brand_name" is the same as "name" in the Brands table.
    brand_name = db.Column(db.String(50), db.ForeignKey('brands.name'),
                           nullable=False)
    name = db.Column(db.String(50), nullable=False)

    # Establish backreference from Brands to Models. When I am on a brand
    # object and do ".models", get list of models of that brand.

    brand = db.relationship('Brand', backref=db.backref('models',
                            order_by=year))

    def __repr__(self):
        return "<model_id=%r, year=%r, brand_name=%r, name=%r>" % (
            self.model_id, self.year, self.brand_name, self.name)


class Brand(db.Model):

    __tablename__ = "brands"

    brand_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # name is the same as brand_name in the Models table.
    name = db.Column(db.String(50), db.ForeignKey('models.brand_name'),
                     nullable=False)
    founded = db.Column(db.Integer)
    headquarters = db.Column(db.String(50))
    discontinued = db.Column(db.Integer)

    # Establish backreference from Models to Brands. When I am on a model
    # object and do ".brand", get the brand of that model.

    model = db.relationship('Model', backref=db.backref('brand'))

    def __repr__(self):
        return "<brand_id=%r, name=%r, founded=%r, HQ=%r, disc=%r" % (
            self.brand_id, self.name, self.founded, self.headquarters,
            self.discontinued)


# End Part 1
##############################################################################
# Helper functions


def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auto.db'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."
