import json
import logging

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import FrictionModel
from schemas import PlainFrictionSchema, FrictionSchema
from engineering import Friction

logger = logging.getLogger(__name__)

blp = Blueprint("friction", __name__, description="Coulomb Friction")


@blp.route("/friction/<int:friction_id>")
class Coulomb(MethodView):
    @blp.response(200, FrictionSchema)
    def get(self, friction_id):
        logger.info(f"Getting values for id: {friction_id}")
        response = FrictionModel.query.get_or_404(friction_id)
        logger.info(f"Successfully retrieved the data for entry.")
        response.velocities = json.loads(response.velocities)
        response.idx = json.loads(response.idx)
        response.distances = json.loads(response.distances)

        return response


@blp.route("/friction")
class CoulombFriction(MethodView):

    @blp.response(200, PlainFrictionSchema(many=True))
    def get(self):
        return FrictionModel.query.all()

    @blp.arguments(PlainFrictionSchema)
    @blp.response(200, PlainFrictionSchema)
    def post(self, friction_data):
        v0 = verify_input_value(friction_data['init_velocity'])
        g = verify_input_value(friction_data['gravity'])
        mu = verify_input_value(friction_data['coef_friction'])
        print(f"v0: {v0}, g: {g}, mu: {mu}")
        cf = Friction(v0=v0, mu=mu, g=g)
        idx, vel = cf.get_all_velocities()
        _, dist = cf.get_distance_traveled()

        friction = FrictionModel(
            init_velocity=v0,
            coef_friction=mu,
            gravity=g,
            velocities=json.dumps(list(vel)),
            idx=json.dumps(list(idx)),
            distances=json.dumps(list(dist))
        )

        try:
            db.session.add(friction)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return friction


def verify_input_value(value: float) -> float:
    """
    This will make sure that the input value is greater or equal to 0. Otherwise, it will return a `ValueError`
    :param value: float value to verify whether it is not negative
    :return: value | ValueError
    """
    if value < 0:
        logger.exception("Invalid user input")
        raise ValueError("Input should be greater than 0.")
    return value
