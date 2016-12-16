from app import db


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
    return True
