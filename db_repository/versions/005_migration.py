from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('fullname', String(length=50), nullable=False),
    Column('username', String(length=50), nullable=False),
    Column('email', String),
    Column('password', String(length=15), nullable=False),
    Column('age', Integer),
    Column('gender', String(length=1)),
    Column('registered_on', DateTime),
    Column('admin', Boolean, default=ColumnDefault(False)),
    Column('confirmed', Boolean, default=ColumnDefault(False)),
    Column('confirmed_on', DateTime),
    Column('allergy_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['registered_on'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['registered_on'].drop()
