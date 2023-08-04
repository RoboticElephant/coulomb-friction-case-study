import pytest

from resources.friction import verify_input_value


def test_verify_input_value_should_return_valid_float():
    expected_value = 10.0
    assert verify_input_value(expected_value) == expected_value


def test_verify_input_value_should_throw_exception():
    with pytest.raises(ValueError):
        verify_input_value(-1.0)


def test_get_all_frictions(test_client):
    response = test_client.get('/friction')
    assert response.status_code == 200


def test_get_friction_should_return_valid_output(test_client, init_database):
    response = test_client.get('/friction/1')
    assert response.status_code == 200
    assert b'"init_velocity":10.0' in response.data


def test_get_friction_should_return_404_unknown_value(test_client, init_database):
    response = test_client.get('/friction/2')
    assert response.status_code == 404


def test_post_add_friction(test_client):
    response = test_client.post('/friction',
                                json={'init_velocity': 110.1,
                                      'gravity': 9.81,
                                      'coef_friction': 42.0}, follow_redirects=True)
    assert response.status_code == 200
    assert b'"init_velocity":110.1' in response.data
    assert b'"gravity":9.81' in response.data
    assert b'"coef_friction":42.0' in response.data


def test_post_add_friction_should_return_422_for_improper_input(test_client):
    response = test_client.post('/friction',
                                json={'init_velocity': "abcd",
                                      'gravity': 9.81,
                                      'coef_friction': 42.0}, follow_redirects=True)
    assert response.status_code == 422
    assert b'"Not a valid number."' in response.data
