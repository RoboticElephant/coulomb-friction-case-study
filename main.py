# from engineering.coulomb_friction import Friction
from engineering import Friction
import logging_config
import logging

from plotly.subplots import make_subplots
import plotly.graph_objects as go

logger = logging.getLogger(__name__)


def plot_friction(v0, mu, g):
    # Get velocity and distance for given Friction
    cf = Friction(v0=v0, mu=mu, g=g)
    v_indices, velocities = cf.get_all_velocities()
    d_indices, distances = cf.get_distance_traveled()

    fig = make_subplots(rows=2, subplot_titles=("Position vs. Time", "Velocity vs. Time"))
    # Add traces
    fig.add_trace(go.Scatter(x=d_indices, y=distances, name="Distance"), row=1, col=1)
    fig.add_trace(go.Scatter(x=v_indices, y=velocities, name="Velocity"), row=2, col=1)

    # Update xaxis properties
    fig.update_xaxes(title_text="Time (s)", row=1, col=1)
    fig.update_xaxes(title_text="Time (s)", row=2, col=1)

    # Update yaxis properties
    fig.update_yaxes(title_text="Position (m)", row=1, col=1)
    fig.update_yaxes(title_text="Velocity (m/s)", row=2, col=1)

    # Update title and subtitle for plot
    fig.update_layout(title=f"Coulomb Friction of Block on Horizontal Plane: "
                            f"<br><sup>Initial Velocity: {v0} m/s, Friction Coefficient: {mu}, Gravity: {g} m/s^2</sup>")
    fig.show()


def get_user_input(input_str: str) -> float:
    while True:
        try:
            value = float(input(input_str))
            return verify_input_value(value)
        except ValueError:
            logger.exception("Invalid user input")
            print("Invalid input. It should be a non-negative number. Please try again!")


def get_user_input_gravity() -> float:
    while True:
        try:
            response = input("Please input gravity (m/s^2) or hit enter if you want to use 9.81 m/s^2: ")
            if response == '':
                return 9.81

            value = float(response)
            return verify_input_value(value)
        except ValueError:
            logger.exception("Invalid user input for gravity")
            print("Invalid input for gravity. Please try again!")


def verify_input_value(value: float):
    if value < 0:
        raise ValueError("Input should be greater than 0.")
    return value


def run_and_plot_coulomb_friction():
    initial_velocity = get_user_input("Please input the initial velocity (m/s): ")
    friction_coef = get_user_input("Please input the coefficient of friction: ")
    gravity = get_user_input_gravity()
    print(f"'{initial_velocity}', '{friction_coef}', '{gravity}'")
    plot_friction(initial_velocity, friction_coef, gravity)


if __name__ == '__main__':
    run_and_plot_coulomb_friction()
