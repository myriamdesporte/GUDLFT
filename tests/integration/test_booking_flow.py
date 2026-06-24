"""Integration tests covering full user flows across multiple routes."""

import pytest

import server


@pytest.mark.integration_test
class TestCriticalBookingFlows:
    """
    Critical user flows that must work for the application to be usable at all.
    A failure here means the core booking feature is broken.
    """

    @pytest.fixture(autouse=True)
    def _mock_data(self, monkeypatch, mock_clubs, mock_competitions):
        monkeypatch.setattr(server, "clubs", mock_clubs)
        monkeypatch.setattr(server, "competitions", mock_competitions)

    def test_login_book_and_purchase_decreases_points_and_places(
        self, client, mock_clubs, mock_competitions
    ):
        """Full happy path: log in, open the booking page, purchase places,
        and verify both club points and competition places decreased."""
        club = next(c for c in mock_clubs if c["name"] == "Simply Lift")
        competition = next(c for c in mock_competitions if c["name"] == "Fall Classic")
        initial_points = int(club["points"])
        initial_places = int(competition["numberOfPlaces"])
        places_to_book = 2

        # 1. Log in
        login_response = client.post(
            "/showSummary", data={"email": "john@simplylift.co"}
        )
        assert login_response.status_code == 200
        assert b"Welcome" in login_response.data

        # 2. Open the page for a bookable competition
        book_response = client.get("/book/Fall%20Classic/Simply%20Lift")
        assert book_response.status_code == 200
        assert b"How many places?" in book_response.data

        # 3. Submit the purchase
        purchase_response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Fall Classic",
                "club": "Simply Lift",
                "places": str(places_to_book),
            },
        )
        assert purchase_response.status_code == 200
        assert b"Great-booking complete!" in purchase_response.data

        # 4. Both counters decreased exactly by places_to_book
        assert int(club["points"]) == initial_points - places_to_book
        assert int(competition["numberOfPlaces"]) == initial_places - places_to_book

    def test_past_competition_cannot_be_booked_end_to_end(self, client):
        """Hitting the past-competition URL directly is refused even though
        the user is logged in."""
        client.post("/showSummary", data={"email": "john@simplylift.co"})

        response = client.get("/book/Spring%20Festival/Simply%20Lift")

        assert response.status_code == 200
        assert b"This competition has already taken place" in response.data


@pytest.mark.slow_integration_test
class TestSecondaryBookingFlows:
    """
    Secondary flows that improve the user experience but do not block the core
    booking feature if they fail.
    """

    @pytest.fixture(autouse=True)
    def _mock_data(self, monkeypatch, mock_clubs, mock_competitions):
        monkeypatch.setattr(server, "clubs", mock_clubs)
        monkeypatch.setattr(server, "competitions", mock_competitions)

    def test_login_then_points_board_shows_updated_points(self, client, mock_clubs):
        """After a booking, the public points board reflects the new balance."""
        club = next(c for c in mock_clubs if c["name"] == "Simply Lift")
        client.post("/showSummary", data={"email": "john@simplylift.co"})
        client.post(
            "/purchasePlaces",
            data={
                "competition": "Fall Classic",
                "club": "Simply Lift",
                "places": "3",
            },
        )

        board_response = client.get("/points-board")
        assert board_response.status_code == 200
        assert b"Simply Lift" in board_response.data
        assert club["points"].encode() in board_response.data

    def test_failed_login_then_retry_succeeds(self, client):
        """A user mistyping their email gets a flash message and can retry."""
        first_attempt = client.post("/showSummary", data={"email": "unknown@test.com"})
        assert first_attempt.status_code == 200
        assert b"email was not found" in first_attempt.data

        retry = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert retry.status_code == 200
        assert b"Welcome" in retry.data
