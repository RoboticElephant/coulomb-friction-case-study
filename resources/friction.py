import logging

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import FrictionModel
from schemas import FrictionSchema
from engineering import Friction
#
# import base64
# from io import BytesIO
# from matplotlib.figure import Figure

logger = logging.getLogger(__name__)

blp = Blueprint("friction", __name__, description="Coulomb Friction")


@blp.route("/friction/<int:friction_id>")
class Coulomb(MethodView):
    @blp.response(200, FrictionSchema)
    def get(self, friction_id):
        logger.info(f"Getting values for id: {friction_id}")
        response = FrictionModel.query.get_or_404(friction_id)
        logger.info(f"Successfully retrieved the data for entry.")

        cf = Friction(v0=response.init_velocity, mu=response.coef_friction, g=response.gravity)
        v_indices, velocities = cf.get_all_velocities()
        # d_indices, distances = cf.get_distance_traveled()
        print(velocities)

        # fig = Figure()
        # ax = fig.subplots(nrows=2, ncols=1)
        # print(ax)
        # ax[0].plot(xs=v_indices, ys=velocities)
        #
        # buf = BytesIO()
        # fig.savefig(buf, format='png')
        #
        # data = base64.b64encode(buf.getbuffer()).decode("ascii")
        # return f"<img src='data:image/png;base64,{data}'/> <br> <img src='data:image/png;base64,{data}'/>"
        return response


@blp.route("/friction")
class CoulombFriction(MethodView):
    @blp.arguments(FrictionSchema)
    @blp.response(200, FrictionSchema)
    def post(self, friction_data):
        v0 = verify_input_value(friction_data['init_velocity'])
        g = verify_input_value(friction_data['gravity'])
        mu = verify_input_value(friction_data['coef_friction'])
        print(f"v0: {v0}, g: {g}, mu: {mu}")

        friction = FrictionModel(init_velocity=v0, coef_friction=mu, gravity=g)

        try:
            db.session.add(friction)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return friction


def verify_input_value(value: float) -> float:
    if value < 0:
        logger.exception("Invalid user input")
        raise ValueError("Input should be greater than 0.")
    return value
