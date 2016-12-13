# from alfred_db import Users
# from sqlalchemy_init import get_session
# from sqlalchemy import and_
from app import models


def get_user_by_id(id_):
    user = models.Users.query.get(id_)
    allergy = models.Allergy.query.get(user.id)
    return user, allergy


def is_username_free(username):

    users = models.Users.query.all()

    for person in users:
        if person.username == username:
            return False
    return True


def get_user_restriciton_tags(id_, usage=0):
    """ Return a list of tags_0 according to user's allergies/preferences.
    usage: select what tag format to return. 0 = for recipe search
                                             1 = for displaying     
    example for user with Nut allergy: 
    0 - return [peanut free, tree nut free] to search against known recipe tags_0
    1 - return [Nuts] to print to header """
    tags_0 = []
    tags_1 = []
    if id_ != 0:
        user = models.Users.query.get(id_)

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
            tags_0.append('nuts')
            tags_0.append('peanut free')
            tags_0.append('tree nut free')
            tags_1.append('Tree Nut Free')

        if user.allergy.fish:
            tags_0.append('fish')
            tags_0.append('swordfish')
            tags_0.append('shellfish')
            tags_0.append('snapper')
            tags_0.append('sardine')
            tags_0.append('salmon')
            tags_0.append('tuna')
            tags_0.append('bass')
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


def list_all_users():
    users = models.Users.query.all()
    for user in users:
        print user, user.password

if __name__ == '__main__':
    list_all_users()
    # get_user_restriciton_tags(1)

