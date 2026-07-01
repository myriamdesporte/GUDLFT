"""Unit tests for the public points display board."""

import pytest

import server


class TestPointsBoard:
    """Tests for the points display board feature."""

    @pytest.fixture(autouse=True)
    def _mock_clubs(self, monkeypatch, mock_clubs):
        monkeypatch.setattr(server, "clubs", mock_clubs)

    def test_points_board_is_accessible(self, client):
        """Test that the points board page loads successfully."""
        response = client.get("/points-board")
        assert response.status_code == 200

    def test_points_board_shows_all_clubs(self, client, mock_clubs):
        """Test that the points board displays all clubs."""
        response = client.get("/points-board")
        for club in mock_clubs:
            assert club["name"].encode() in response.data

    def test_points_board_shows_points(self, client, mock_clubs):
        """Test that the points board displays points for each club."""
        response = client.get("/points-board")
        for club in mock_clubs:
            assert club["points"].encode() in response.data

    def test_points_board_is_public(self, client):
        """Test that the points board is accessible without login."""
        response = client.get("/points-board")
        assert response.status_code == 200
        assert b"Club Points Board" in response.data

    def test_back_link_targets_index_without_email(self, client):
        """With no email query param the Back to Home link points to index."""
        response = client.get("/points-board")
        assert response.status_code == 200
        assert b'href="/"' in response.data

    def test_back_link_targets_show_summary_with_valid_email(self, client):
        """With a known email the Back to Home link returns to the welcome page."""
        response = client.get("/points-board?email=john@simplylift.co")
        assert response.status_code == 200
        assert b"/showSummary?email=john" in response.data

    def test_back_link_falls_back_to_index_with_unknown_email(self, client):
        """An unknown email is ignored and the link falls back to index."""
        response = client.get("/points-board?email=unknown@test.com")
        assert response.status_code == 200
        assert b"/showSummary?email=" not in response.data
        assert b'href="/"' in response.data
