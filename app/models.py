from app import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=True)
    fullname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1), nullable=True)
    password = db.Column(db.String(15), nullable=False)

    # allergies_id = database.Column(database.Integer, database.ForeignKey('allergies.id'))
    # allergies = database.relationship('Allergy', backref='users')

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
            return str(self.id)  # python3

    def __repr__(self):
        return '<id:%r name:%r>' % (self.id, self.fullname)


class Allergy(db.Model):
    __tablename__ = 'allergies'

    id = db.Column(db.Integer, primary_key=True)
    soy = db.Column(db.Boolean, nullable=False)
    milk = db.Column(db.Boolean, nullable=False)
    eggs = db.Column(db.Boolean, nullable=False)
    nuts = db.Column(db.Boolean, nullable=False)
    gluten = db.Column(db.Boolean, nullable=False)
    fish = db.Column(db.Boolean, nullable=False)
    sesame = db.Column(db.Boolean, nullable=False)
    # user_id = database.Column(database.Integer, database.ForeignKey('users.id'))

    def __repr__(self):
        return '<nuts:%r soy:%r gluten:%r fish:%r sesame:%r milk:%r>' % (self.nuts, self.soy, self.gluten, self.fish, self.sesame, self.milk)
