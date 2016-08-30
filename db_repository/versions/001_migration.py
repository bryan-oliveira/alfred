from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
allergies2 = Table('allergies2', pre_meta,
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

users2 = Table('users2', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('age', INTEGER),
    Column('fullname', VARCHAR(length=50), nullable=False),
    Column('username', VARCHAR(length=50), nullable=False),
    Column('gender', VARCHAR(length=1)),
    Column('password', VARCHAR(length=15), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['allergies2'].drop()
    pre_meta.tables['users2'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['allergies2'].create()
    pre_meta.tables['users2'].create()
