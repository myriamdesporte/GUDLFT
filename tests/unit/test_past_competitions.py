"""Unit tests for preventing booking in past competitions."""

import pytest

import server


class TestPastCompetitions:
    """Tests that booking in past competitions is not allowed."""

    @pytest.fixture(autouse=True)
    def _mock_data(self, monkeypatch, mock_clubs, mock_competitions):
        monkeypatch.setattr(server, "clubs", mock_clubs)
        monkeypatch.setattr(server, "competitions", mock_competitions)

    def test_cannot_book_past_competition(self, client):
        """Test that booking a past competition shows an error."""
        # Spring Festival competition took place in March 2026, which is in the past
        response = client.get("/book/Spring%20Festival/Simply%20Lift")
        assert response.status_code == 200
        assert b"This competition has already taken place" in response.data

    def test_can_book_future_competition(self, client):
        """Test that booking a future competition works normally."""
        # Fall classic competition will take place in October 2026
        response = client.get("/book/Fall%20Classic/Simply%20Lift")
        assert response.status_code == 200
        assert b"How many places?" in response.data

    def test_book_unknown_competition_redirects_to_index(self, client):
        """Test that booking an unknown competition redirects to the login page."""
        response = client.get("/book/Unknown%20Competition/Simply%20Lift")
        assert response.status_code == 302
        assert response.location.endswith("/")

    def test_book_unknown_club_redirects_to_index(self, client):
        """Test that booking with an unknown club redirects to the login page."""
        response = client.get("/book/Fall%20Classic/Unknown%20Club")
        assert response.status_code == 302
        assert response.location.endswith("/")
