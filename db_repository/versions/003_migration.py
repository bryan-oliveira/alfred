from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
allergy = Table('allergy', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('soy', BOOLEAN, nullable=False),
    Column('milk', BOOLEAN, nullable=False),
    Column('eggs', BOOLEAN, nullable=False),
    Column('nuts', BOOLEAN, nullable=False),
    Column('gluten', BOOLEAN, nullable=False),
    Column('fish', BOOLEAN, nullable=False),
    Column('sesame', BOOLEAN, nullable=False),
    Column('user_id', INTEGER),
)

allergies = Table('allergies', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('soy', Boolean, nullable=False),
    Column('milk', Boolean, nullable=False),
    Column('eggs', Boolean, nullable=False),
    Column('nuts', Boolean, nullable=False),
    Column('gluten', Boolean, nullable=False),
    Column('fish', Boolean, nullable=False),
    Column('sesame', Boolean, nullable=False),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('age', Integer),
    Column('fullname', String(length=50), nullable=False),
    Column('username', String(length=50), nullable=False),
    Column('gender', String(length=1)),
    Column('password', String(length=15), nullable=False),
    Column('allergies_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['allergy'].drop()
    post_meta.tables['allergies'].create()
    post_meta.tables['users'].columns['allergies_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['allergy'].create()
    post_meta.tables['allergies'].drop()
    post_meta.tables['users'].columns['allergies_id'].drop()
