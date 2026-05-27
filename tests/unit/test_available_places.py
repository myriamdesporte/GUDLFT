"""Unit tests for available places validation."""

import pytest

import server


class TestAvailablePlaces:
    """Tests that clubs cannot book more places than available."""

    @pytest.fixture(autouse=True)
    def _mock_data(self, monkeypatch, mock_clubs, mock_competitions):
        monkeypatch.setattr(server, "clubs", mock_clubs)
        monkeypatch.setattr(server, "competitions", mock_competitions)

    def test_cannot_book_more_than_available_places(self, client, mock_competitions):
        """Test that booking more places than available is rejected."""
        competition = next(c for c in mock_competitions if c["name"] == "Fall Classic")
        competition["numberOfPlaces"] = "3"

        response = client.post(
            "/purchasePlaces",
            data={"competition": "Fall Classic", "club": "Simply Lift", "places": "5"},
        )

        assert response.status_code == 200
        assert b"Not enough places available" in response.data

    def test_can_book_when_enough_places_available(self, client):
        """Test that booking works when enough places are available."""
        response = client.post(
            "/purchasePlaces",
            data={"competition": "Fall Classic", "club": "Simply Lift", "places": "2"},
        )

        assert response.status_code == 200
        assert b"Great-booking complete!" in response.data
