import pytest
from engineering import Friction

MU = 0.5
V0 = 1.0
G = 1.0


def test_get_velocity_at_time():
    mu = 0.3
    v0 = 10
    g = 9.81
    t = 1
    cf = Friction(mu=mu, v0=v0, g=g)
    actual = v0 - mu * g * t
    assert cf.get_velocity_at_time(t) == actual


def test_get_velocity_at_time_should_raise_exception():
    cf = Friction(mu=MU, v0=V0, g=G)
    with pytest.raises(ValueError):
        cf.get_velocity_at_time(-10)


def test_get_all_velocities():
    cf = Friction(mu=MU, v0=V0, g=G)
    idx, vel = cf.get_all_velocities()
    assert len(idx) == len(cf.indices)
    assert (vel[0] == V0) & (vel[-1] == 0)


def test_get_distance_traveled():
    cf = Friction(mu=MU, v0=V0, g=G)
    _, dist = cf.get_distance_traveled()

    assert (dist[0] == 0.0) & (dist[-1] == 1.0)
