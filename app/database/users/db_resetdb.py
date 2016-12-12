from app import db
from app.models import Users, Allergy

if __name__ == '__main__':
    num_users_deleted = db.session.query(Users).delete()
    num_allergies_deleted = db.session.query(Allergy).delete()
    db.session.commit()
    print "Deleted ", num_users_deleted, "users and", num_allergies_deleted, "allergies."

