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
    Column('user_id', INTEGER),
)

allergy = Table('allergy', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('soy', Boolean, nullable=False),
    Column('milk', Boolean, nullable=False),
    Column('eggs', Boolean, nullable=False),
    Column('nuts', Boolean, nullable=False),
    Column('gluten', Boolean, nullable=False),
    Column('fish', Boolean, nullable=False),
    Column('sesame', Boolean, nullable=False),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['allergies'].drop()
    post_meta.tables['allergy'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['allergies'].create()
    post_meta.tables['allergy'].drop()
