from flask.ext.login import AnonymousUserMixin
from app import db

# u = Users(username="newuser", fullname="New User", gender="Male", age=20, password="123123")
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=True)
    fullname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1), nullable=True)
    password = db.Column(db.String(15), nullable=False)

    allergy_id = db.Column(db.Integer, db.ForeignKey('allergy.id'))
    allergy = db.relationship('Allergy', backref='users')

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

    def __repr__(self):
        return '<id:%r fullname:%r username:%r gender:%r age:%r allergy:%r>' \
               % (self.id, self.username, self.fullname, self.gender, self.age, self.allergy)


# a = Allergy(lowchol=False, highchol=False, overw=False, underw=False, gluten=False,
# fish=False, sesame=False, nuts=False, vegetarian=False, vegan=False)
class Allergy(db.Model):
    __tablename__ = 'allergy'

    id = db.Column(db.Integer, primary_key=True)
    lowchol = db.Column(db.Boolean, nullable=False)
    highchol = db.Column(db.Boolean, nullable=False)
    overw = db.Column(db.Boolean, nullable=False)
    underw = db.Column(db.Boolean, nullable=False)
    gluten = db.Column(db.Boolean, nullable=False)
    fish = db.Column(db.Boolean, nullable=False)
    sesame = db.Column(db.Boolean, nullable=False)
    nuts = db.Column(db.Boolean, nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False)
    vegan = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Low Chol:%r High Chol:%r Over Weight:%r Under Weight:%r ' \
               'Gluten:%r Nuts:%r Fish:%r Sesame:%r Vegatarian:%r Vegan:%r>' % \
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

