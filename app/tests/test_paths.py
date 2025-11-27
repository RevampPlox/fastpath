from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


class TestPaths:
    BASE_URI = '/api/v1/paths'

    def test_create_path_sucessfull(self, client: TestClient) -> None:
        new_path = {
            'pickup': {'lat': 12.1234567, 'lng': 123.1234567},
            'dropoff': [
                {'lat': 12.1234567, 'lng': 123.1234567},
                {'lat': 12.1234567, 'lng': 123.1234567},
            ],
        }
        response = client.post(self.BASE_URI, json=new_path)
        data = response.json()

        assert response.status_code == HTTPStatus.CREATED
        assert data['pickup']['lat'] == pytest.approx(
            new_path['pickup']['lat'],
        )
        assert data['pickup']['lng'] == pytest.approx(
            new_path['pickup']['lng'],
        )
        assert len(data['dropoff']) == len(new_path['dropoff'])

    def test_create_bad_format_path(self, client: TestClient) -> None:
        new_path = {
            'pickup': {'lat': 'wrong-location', 'lng': 123.1234567},
            'dropoff': [
                {'lat': 12.1234567, 'lng': 123.1234567},
                {'lat': 12.1234567, 'lng': 123.1234567},
            ],
        }
        response = client.post(self.BASE_URI, json=new_path)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_get_paths_should_return_empty(self, client: TestClient) -> None:
        response = client.get(self.BASE_URI)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'data': []}
