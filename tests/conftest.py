from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from meal_planner.models import Base
import pytest


@pytest.fixture(scope='session')
def engine():
    return create_engine('sqlite:///test_db')


@pytest.yield_fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.yield_fixture
def dbsession(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()

#--- Test data
@pytest.fixture(scope='session')
def data_recipes():
    recipes = {
        'salty_soup': {
            'ingredients': [
                {
                    'name': 'salt',
                    'unit': 'tbsp',
                    'quantity': 1
                },
                {
                    'name': 'water'
                },
                {
                    'name': 'potato',
                    'unit': 'kg',
                    'quantity': 0.5
                }
            ],
            'description': 'add salt, water, potato',
            'nr_meals': 3
        },
        'carrot_stew': {
            'ingredients': [
                {
                    'name': 'carrots',
                    'unit': 'kg',
                    'quantity': 0.5
                },
                {
                    'name': 'water',
                    'quantity': 1,
                    'unit': 'dash'
                },
                {
                    'name': 'potato',
                    'unit': 'kg',
                    'quantity': 0.2
                },
                {
                    'name': 'salt',
                    'unit': 'tbsp',
                    'quantity': 0.5
                },
            ],
            'description': 'mix carrot, water, potato',
            'nr_meals': 2
        }
    }
    yield recipes