"""Unit tests for the 12-places-per-competition limit."""

import pytest

import server


class TestMax12Places:
    """Tests that clubs cannot book more than 12 places per competition."""

    @pytest.fixture(autouse=True)
    def _mock_data(self, monkeypatch, mock_clubs, mock_competitions):
        monkeypatch.setattr(server, "clubs", mock_clubs)
        monkeypatch.setattr(server, "competitions", mock_competitions)

    def test_cannot_book_more_than_12_places(self, client):
        """Test that booking more than 12 places is rejected."""
        response = client.post(
            "/purchasePlaces",
            data={"competition": "Fall Classic", "club": "Simply Lift", "places": "13"},
        )

        assert response.status_code == 200
        assert b"Cannot book more than 12 places" in response.data

    def test_can_book_exactly_12_places(self, client):
        """Test that booking exactly 12 places works."""
        response = client.post(
            "/purchasePlaces",
            data={"competition": "Fall Classic", "club": "Simply Lift", "places": "12"},
        )

        assert response.status_code == 200
        assert b"Great-booking complete!" in response.data
