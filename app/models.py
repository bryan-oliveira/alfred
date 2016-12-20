from flask.ext.login import AnonymousUserMixin
from app import bcrypt
from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(1), nullable=True)

    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.SmallInteger, nullable=True, default=False)
    confirmed = db.Column(db.SmallInteger, nullable=True, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    allergy = db.relationship('Allergy', uselist=False, back_populates='user')
    favorite = db.relationship("Favorite", backref="user")

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def get_hash(self):
        return self.password

    def __init__(self, fullname='', username='', email='', password='.', age=0, gender='M',
                 confirmed=False, admin=False):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.age = age
        self.gender = gender
        self.registered_on = datetime.utcnow()
        self.admin = admin
        self.confirmed = confirmed

    def __repr__(self):
        return '<id:%r fullname:%r username:%r email:%r\n' \
               'hash:%r gender:%r age:%r registered on:%r\n' \
               'admin:%r confirmed:%r confirmed on:%r allergy:%r fav:%r>' \
               % (self.id, self.fullname, self.username, self.email,
                  self.password, self.gender, self.age, self.registered_on,
                  self.admin, self.confirmed, self.confirmed_on, self.allergy,
                  self.favorite)


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'id: %r, user id: %r, title: %r' % (self.id, self.user_id, self.title)


class Allergy(db.Model):
    __tablename__ = 'allergy'

    id = db.Column(db.Integer, primary_key=True)
    lowchol = db.Column(db.Boolean, nullable=False, default=False)
    highchol = db.Column(db.Boolean, nullable=False, default=False)
    overw = db.Column(db.Boolean, nullable=False, default=False)
    underw = db.Column(db.Boolean, nullable=False, default=False)
    gluten = db.Column(db.Boolean, nullable=False, default=False)
    fish = db.Column(db.Boolean, nullable=False, default=False)
    sesame = db.Column(db.Boolean, nullable=False, default=False)
    nuts = db.Column(db.Boolean, nullable=False, default=False)
    vegetarian = db.Column(db.Boolean, nullable=False, default=False)
    vegan = db.Column(db.Boolean, nullable=False, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='allergy')

    def __init__(self, lowchol=False, highchol=False , overw=False, underw=False, gluten=False,
                 fish=False, nuts=False, sesame=False, vegetarian=False, vegan=False):
        self.lowchol = lowchol
        self.highchol = highchol
        self.overw = overw
        self.underw = underw
        self.gluten = gluten
        self.fish = fish
        self.sesame = sesame
        self.nuts = nuts
        self.vegetarian = vegetarian
        self.vegan = vegan

    def __repr__(self):
        return '<Low Chol:%r High Chol:%r Over Weight:%r Under Weight:%r ' \
               'Gluten:%r Nuts:%r Fish:%r Sesame:%r Vegetarian:%r Vegan:%r>' % \
               (self.lowchol, self.highchol, self.overw,self.underw, self.gluten, self.nuts,
                self.fish, self.sesame, self.vegetarian, self.vegan)


class AnonymousUser(AnonymousUserMixin):
    # Initializes anonymous guest credentials. Currently used for
    # logging purposes.
    def __init__(self):
        self.username = 'Guest'
        self.id = 0

    def __repr__(self):
        return "Username: %r id: %r" % (self.username, self.id)

