import numpy as np
import logging

logger = logging.getLogger(__name__)


class Friction:
    """
    This is a class to work with Coulomb's Friction, which is friction on a dry surface.

    Assumptions:
    - Block is sliding on a horizontal surface
    - No other forces are being imparted into the system during movement.
    """
    def __init__(self, mu, v0, g, steps=20):
        self.mu = mu
        self.v0 = v0
        self.g = g
        logger.info(
            f"Friction being called with initial velocity: {v0}, coefficient of friction: {mu} and gravity: {g}")

        self.acceleration = - self.mu * self.g
        self.total_time = - self.v0 / self.acceleration
        self.indices = []
        self.change_steps_for_measurements(steps)

    def change_steps_for_measurements(self, steps):
        """
        Changes the number of steps used for measurements. This can be used to break up the total time from some initial
        velocity to the final velocity of 0.

        This will change the indices being used to determine all the velocities and distance traveled.

        :param steps: Number of steps to take from start time to end time.
        :return: None
        """
        logger.info(f"Changing the number of steps to {steps}")
        self.indices = np.linspace(0, self.total_time, num=steps, endpoint=True)

    def get_velocity_at_time(self, time):
        """
        This function will get the new velocity at a given time.
        It will also update the initial velocity.

        :param time: elapsed time
        :param v0: Initial velocity if different then class's variable
        :return: current velocity at a given time
        """
        return self.v0 + self.acceleration * time

    def get_all_velocities(self):
        """
        Gets all the velocities, from initial to 0, based on the frequency of the measurements.

        :return: (indices[], velocities[])
        """
        return self.indices, [self.get_velocity_at_time(idx) for idx in self.indices]

    def get_distance_traveled(self):
        """
        Gets the distance traveled at each time interval.

        :return: (indices[], distance[])
        """
        dist = [self.v0 * t + 0.5 * self.acceleration * t**2 for t in self.indices]
        return self.indices, dist
