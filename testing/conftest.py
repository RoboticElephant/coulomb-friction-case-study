import os
import json

import pytest

from app import create_app, db
from models.friciton import FrictionModel

# --------
# Fixtures
# --------


@pytest.fixture(scope='module')
def test_client():
    # Set the testing database prior to creating the Flask application
    os.environ['DATABASE'] = "sqlite:///test_data.db"
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            # This is where the testing happens
            yield testing_client


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert friction data. This data isn't accurate, but is used just for testing
    friction = FrictionModel(
        init_velocity=10,
        coef_friction=0.3,
        gravity=9.81,
        velocities=json.dumps(list(range(0, 10))),
        idx=json.dumps(list(range(0, 10))),
        distances=json.dumps(list(range(0, 10)))
    )

    db.session.add(friction)
    # Commit the changes for friction
    db.session.commit()

    yield  # This is where the testing happens

    db.drop_all()


# @pytest.fixture(scope='module')
# def cli_test_client():
#     # Set the Testing configuration prior to creating the Flask application
#     os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
#     flask_app = create_app()
#
#     runner = flask_app.test_cli_runner()
#
#     yield runner  # this is where the testing happens!

