import requests

from plotly.subplots import make_subplots
import plotly.graph_objects as go

# This was only used to plot the data. The real work here is the creation of the REST API.


def plot_friction(db_id, url="http://127.0.0.1:5005"):
    # Get velocity and distance for given Friction
    response = requests.get(f"{url}/friction/{db_id}")
    if response.status_code != 200:
        raise ValueError("Invalid ID entered or issue with the server.")

    data = response.json()

    fig = make_subplots(rows=2, subplot_titles=("Position vs. Time", "Velocity vs. Time"))
    # Add traces
    fig.add_trace(go.Scatter(x=data["idx"], y=data["distances"], name="Distance"), row=1, col=1)
    fig.add_trace(go.Scatter(x=data["idx"], y=data["velocities"], name="Velocity"), row=2, col=1)

    # Update xaxis properties
    fig.update_xaxes(title_text="Time (s)", row=1, col=1)
    fig.update_xaxes(title_text="Time (s)", row=2, col=1)

    # Update yaxis properties
    fig.update_yaxes(title_text="Position (m)", row=1, col=1)
    fig.update_yaxes(title_text="Velocity (m/s)", row=2, col=1)

    # Update title and subtitle for plot
    fig.update_layout(title=f"Coulomb Friction of Block on Horizontal Plane: "
                            f"<br><sup>Initial Velocity: {data['init_velocity']} m/s, "
                            f"Friction Coefficient: {data['coef_friction']}, "
                            f"Gravity: {data['gravity']} m/s^2</sup>")
    fig.show()


def get_user_input(input_str: str) -> int:
    while True:
        try:
            value = int(input(input_str))
            if value <= 0:
                raise ValueError("Input should be greater than 0.")
            return value
        except ValueError:
            print("Invalid input. It should be a non-negative number. Please try again!")


def run_and_plot_coulomb_friction():
    id_selected = get_user_input("Please enter the Friction ID you wish to plot: ")
    try:
        plot_friction(id_selected)
    except ValueError:
        print(f"There is an issue with the db_id: {id_selected}. Was not able to plot data.")


if __name__ == '__main__':
    run_and_plot_coulomb_friction()
