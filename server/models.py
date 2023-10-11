from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship
    missions = db.relationship('Mission', backref='planet', cascade = 'all, delete')

    # Add serialization rules

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    field_of_study = db.Column(db.String, nullable = False)

    # Add relationship
    missions = db.relationship('Mission', backref='scientist', cascade = 'all, delete')

    # Add serialization rules

    # Add validation
    @validates('name','field_of_study')
    def val_science(self,key,value):
        if not value:
            raise ValueError
        return value


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)

    # Add relationships
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable = False)

    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'), nullable = False)

    # Add serialization rules
    serialize_rules = ('-planet.missions','-scientist.missions')

    # Add validation
    
    #validatation breaks delete just use nullable

    @validates('planet_id','scientist_id','name')
    def val_mission(self,key,value):
        if not value:
            raise ValueError
        return value


# add any models you may need.
