from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


def test_create_path_sucessfull(client: TestClient) -> None:
    new_path = {
        'pickup': {'lat': 12.1234567, 'lng': 123.1234567},
        'dropoff': [
            {'lat': 12.1234567, 'lng': 123.1234567},
            {'lat': 12.1234567, 'lng': 123.1234567},
        ],
    }
    response = client.post('/api/v1/paths', json=new_path)
    data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert data['pickup']['lat'] == pytest.approx(new_path['pickup']['lat'])
    assert data['pickup']['lng'] == pytest.approx(new_path['pickup']['lng'])
    assert len(data['dropoff']) == len(new_path['dropoff'])
