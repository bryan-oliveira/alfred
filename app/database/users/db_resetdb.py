from app import db
from app.models import User, Allergy

if __name__ == '__main__':
    """ Delete all users from database """
    num_users_deleted = db.session.query(User).delete()
    num_allergies_deleted = db.session.query(Allergy).delete()
    db.session.commit()
    print "Deleted ", num_users_deleted, "users and", num_allergies_deleted, "allergies."

