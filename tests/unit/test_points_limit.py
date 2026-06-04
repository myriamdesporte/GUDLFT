"""Unit tests for points limit validation."""

import pytest

import server


class TestPointsLimit:
    """Tests that clubs cannot use more points than they have."""

    @pytest.fixture(autouse=True)
    def _mock_data(self, monkeypatch, mock_clubs, mock_competitions):
        monkeypatch.setattr(server, "clubs", mock_clubs)
        monkeypatch.setattr(server, "competitions", mock_competitions)

    def test_cannot_book_more_places_than_points(self, client):
        """Test that booking more places than available points is rejected."""
        # Iron Temple has 4 points, try to book 5
        response = client.post(
            "/purchasePlaces",
            data={"competition": "Fall Classic", "club": "Iron Temple", "places": "5"},
        )

        assert response.status_code == 200
        assert b"Not enough points" in response.data

    def test_can_book_places_equal_to_points(self, client):
        """Test that booking exactly the number of available points works."""
        # Iron Temple has 4 points, book exactly 4
        response = client.post(
            "/purchasePlaces",
            data={"competition": "Fall Classic", "club": "Iron Temple", "places": "4"},
        )

        assert response.status_code == 200
        assert b"Great-booking complete!" in response.data

    def test_welcome_page_hides_booking_link_when_no_points(self, client, monkeypatch):
        """When a club has 0 points, no Book Places link is rendered."""
        broke_club = [
            {"name": "Broke Club", "email": "broke@example.com", "points": "0"},
        ]
        monkeypatch.setattr(server, "clubs", broke_club)

        response = client.post("/showSummary", data={"email": "broke@example.com"})

        assert response.status_code == 200
        assert b"Fall Classic" in response.data
        assert b"/book/" not in response.data

    def test_welcome_page_shows_booking_link_when_points_available(self, client):
        """A club with points still sees the Book Places link."""
        # Iron Temple has 4 points and Fall Classic is a future competition
        response = client.post("/showSummary", data={"email": "admin@irontemple.com"})

        assert response.status_code == 200
        assert b"/book/Fall%20Classic/" in response.data

    def test_booking_is_limited_by_club_available_places(self, client):
        """The booking form is limited to the number of club points allowed."""
        # Iron Temple has 4 points, Fall Classic has 13 places
        response = client.get("/book/Fall%20Classic/Iron%20Temple")

        assert response.status_code == 200
        assert b'max="4"' in response.data

    def test_booking_input_min_is_zero(self, client):
        """The booking form prevents negative numbers via the input min attribute."""
        response = client.get("/book/Fall%20Classic/Iron%20Temple")

        assert response.status_code == 200
        assert b'min="0"' in response.data
