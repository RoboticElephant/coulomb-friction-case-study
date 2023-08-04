import json
import logging

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import FrictionModel
from schemas import PlainFrictionSchema, FrictionSchema
from engineering import Friction

# from plotly.subplots import make_subplots
# import plotly.graph_objects as go

logger = logging.getLogger(__name__)

blp = Blueprint("friction", __name__, description="Coulomb Friction")


# @blp.route("/friction/plot/<int:friction_id>")
# class PlotCoulombFriction(MethodView):
#     @blp.response(200, PlainFrictionSchema)
#     def get(self, friction_id):
#         logger.info(f"Plotting data for id: {friction_id}")
#         response = FrictionModel.query.get_or_404(friction_id)
#
#         indices = json.loads(response.idx)
#         velocities = json.loads(response.velocities)
#         distances = json.loads(response.distances)
#
#         fig = make_subplots(rows=2, subplot_titles=("Position vs. Time", "Velocity vs. Time"))
#         # Add traces
#         fig.add_trace(go.Scatter(x=indices, y=distances, name="Distance"), row=1, col=1)
#         fig.add_trace(go.Scatter(x=indices, y=velocities, name="Velocity"), row=2, col=1)
#
#         # Update xaxis properties
#         fig.update_xaxes(title_text="Time (s)", row=1, col=1)
#         fig.update_xaxes(title_text="Time (s)", row=2, col=1)
#
#         # Update yaxis properties
#         fig.update_yaxes(title_text="Position (m)", row=1, col=1)
#         fig.update_yaxes(title_text="Velocity (m/s)", row=2, col=1)
#
#         # Update title and subtitle for plot
#         fig.update_layout(title=f"Coulomb Friction for a Block on a Horizontal Plane:"
#                                 f"<br><sup>Initial Velocity: {response.init_velocity} m/s, "
#                                 f"Friction Coefficient: {response.coef_friction}, "
#                                 f"Gravity: {response.gravity} m/s^2</sup>")
#         fig.show()


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
    if value < 0:
        logger.exception("Invalid user input")
        raise ValueError("Input should be greater than 0.")
    return value
