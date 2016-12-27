from app import db
from app.models import User, Allergy, Favorite

if __name__ == '__main__':
    """ Delete all users/allergies from database """
    num_users_deleted = db.session.query(User).delete()
    num_allergies_deleted = db.session.query(Allergy).delete()
    num_favorites_deleted = db.session.query(Favorite).delete()
    db.session.commit()

    print "Deleted: \n%s users\n%s allergies\n%s favorites" % (num_users_deleted,
                                                                num_allergies_deleted,
                                                                num_favorites_deleted)

