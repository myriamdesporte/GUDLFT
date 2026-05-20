"""Unit tests for points deduction after booking."""

import pytest

import server


class TestPointsDeduction:
    """Tests that points are correctly deducted after purchasing places."""

    @pytest.fixture(autouse=True)
    def _mock_data(self, monkeypatch, mock_clubs, mock_competitions):
        monkeypatch.setattr(server, "clubs", mock_clubs)
        monkeypatch.setattr(server, "competitions", mock_competitions)

    def test_points_are_deducted_after_booking(self, client, mock_clubs):
        """Test that club points decrease after a successful booking."""
        club = next(c for c in mock_clubs if c["name"] == "Simply Lift")
        initial_points = int(club["points"])
        places_to_book = 3

        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Fall Classic",
                "club": "Simply Lift",
                "places": str(places_to_book),
            },
        )

        assert response.status_code == 200
        assert int(club["points"]) == initial_points - places_to_book

    def test_competition_places_decrease_after_booking(self, client, mock_competitions):
        """Test that competition places decrease after a successful booking."""
        competition = next(c for c in mock_competitions if c["name"] == "Fall Classic")
        initial_places = int(competition["numberOfPlaces"])
        places_to_book = 2

        client.post(
            "/purchasePlaces",
            data={
                "competition": "Fall Classic",
                "club": "Simply Lift",
                "places": str(places_to_book),
            },
        )

        assert int(competition["numberOfPlaces"]) == initial_places - places_to_book

    def test_purchase_unknown_competition_redirects_to_index(self, client):
        """Posting an unknown competition name redirects to the login page."""
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Unknown Competition",
                "club": "Simply Lift",
                "places": "1",
            },
        )

        assert response.status_code == 302
        assert response.location.endswith("/")

    def test_purchase_unknown_club_redirects_to_index(self, client):
        """Posting an unknown club name redirects to the login page."""
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Fall Classic",
                "club": "Unknown Club",
                "places": "1",
            },
        )

        assert response.status_code == 302
        assert response.location.endswith("/")
