from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
allergies = Table('allergies', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('soy', BOOLEAN, nullable=False),
    Column('milk', BOOLEAN, nullable=False),
    Column('eggs', BOOLEAN, nullable=False),
    Column('nuts', BOOLEAN, nullable=False),
    Column('gluten', BOOLEAN, nullable=False),
    Column('fish', BOOLEAN, nullable=False),
    Column('sesame', BOOLEAN, nullable=False),
)

allergy = Table('allergy', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('lowchol', Boolean, nullable=False),
    Column('highchol', Boolean, nullable=False),
    Column('overw', Boolean, nullable=False),
    Column('underw', Boolean, nullable=False),
    Column('gluten', Boolean, nullable=False),
    Column('fish', Boolean, nullable=False),
    Column('sesame', Boolean, nullable=False),
    Column('nuts', Boolean, nullable=False),
    Column('vegetarian', Boolean, nullable=False),
    Column('vegan', Boolean, nullable=False),
)

users = Table('users', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('age', INTEGER),
    Column('fullname', VARCHAR(length=50), nullable=False),
    Column('username', VARCHAR(length=50), nullable=False),
    Column('gender', VARCHAR(length=1)),
    Column('password', VARCHAR(length=15), nullable=False),
    Column('allergies_id', INTEGER),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('age', Integer),
    Column('fullname', String(length=50), nullable=False),
    Column('username', String(length=50), nullable=False),
    Column('gender', String(length=1)),
    Column('password', String(length=15), nullable=False),
    Column('allergy_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['allergies'].drop()
    post_meta.tables['allergy'].create()
    pre_meta.tables['users'].columns['allergies_id'].drop()
    post_meta.tables['users'].columns['allergy_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['allergies'].create()
    post_meta.tables['allergy'].drop()
    pre_meta.tables['users'].columns['allergies_id'].create()
    post_meta.tables['users'].columns['allergy_id'].drop()
