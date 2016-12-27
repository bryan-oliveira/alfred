from app import models
from app import db
from datetime import datetime


def toggle_recipe_is_favorite(user_id, title):
    """
    Check if recipe is in user's favorite list. If it isn't add it, otherwise remove
    """
    user = models.User.query.filter_by(id=user_id).first()
    check = False

    # Look for recipe in user's list and remove it
    for fav in user.favorite:
        if fav.title.strip().lower() == title.strip().lower():
            db.session.delete(fav)
            check = True

    # If recipe not found in user's list. Add it
    if not check:
        fav = models.Favorite()
        fav.title = title
        user.favorite.append(fav)

    db.session.commit()


def get_user_by_id(id_):
    user = models.User.query.get(id_)
    allergy = models.Allergy.query.get(user.id)
    return user, allergy


def is_username_free(username):

    users = models.User.query.all()

    for person in users:
        if person.username == username:
            return False
    return True


def email_is_free(email):
    if models.User.query.filter_by(email=email).first():
        return False
    return True


def get_user_restriction_tags(id_, usage=0):
    """ Return a list of tags_0 according to user's allergies/preferences.
    usage: select what tag format to return. 0 = for recipe search
                                             1 = for displaying     
    example for user with Nut allergy: 
    0 - return [peanut free, tree nut free] to search against known recipe tags_0
    1 - return [Nuts] to print to header """
    tags_0 = []
    tags_1 = []
    if id_ != 0:
        user = models.User.query.get(id_)

        if user.allergy.lowchol:
            tags_0.append('lowchol')
            tags_1.append('Low Cholesterol')

        if user.allergy.highchol:
            tags_0.append('highchol')
            tags_1.append('High Cholesterol')

        if user.allergy.overw:
            tags_0.append('overw')
            tags_1.append('Weight Loss')

        if user.allergy.underw:
            tags_0.append('underw')
            tags_1.append('Weight Gain')

        if user.allergy.gluten:
            tags_0.append('gluten')
            tags_0.append('wheat/gluten-free')
            tags_1.append('Gluten Free')

        if user.allergy.nuts:
            tags_0.append('peanut free')
            tags_0.append('tree nut free')
            tags_1.append('Tree Nut Free')

        if user.allergy.fish:
            tags_0.append('pescatarian')
            tags_1.append('Pescatarian')

        if user.allergy.sesame:
            # TODO: Make changes to NOT include this
            tags_0.append('sesame')

        if user.allergy.vegetarian:
            tags_0.append('vegetarian')
            tags_1.append('Vegetarian')

        if user.allergy.vegan:
            tags_0.append('vegan')
            tags_1.append('Vegan')

    if usage == 0:
        return tags_0
    return tags_1


def confirm_user(user):
    user.confirmed = True
    user.confirmed_on = datetime.now()
    db.session.add(user)
    db.session.commit()
    return True


def list_all_users():
    print "Users"

    # Query model for users and print them
    users = models.User.query.all()
    for user in users:
        print user, user.password
    print len(users), "users."
    print "===================="

    # Query model for allergies and print them
    print "Allergy"
    allergies = models.Allergy.query.all()
    for allergy in allergies:
        print allergy
    print len(allergies), "allergies."
    print "===================="

    # Query model for favorites and print them
    print "Favorites"
    favs = models.Favorite.query.all()
    for fav in favs:
        print fav
    print len(favs), "favorites."
    print "===================="

if __name__ == '__main__':
    list_all_users()
    # get_user_restriciton_tags(1)

