"""Unit tests for the search tools helpers."""

from helpers import find_club_by_email, find_club, find_competition


class TestFindClubByEmail:
    """find_club_by_email() searches for a club based on email, ignoring case."""

    def test_returns_matching_club(self, mock_clubs):
        simply_lift = next(c for c in mock_clubs if c["name"] == "Simply Lift")
        assert find_club_by_email(mock_clubs, "john@simplylift.co") == simply_lift

    def test_match_is_case_insensitive(self, mock_clubs):
        simply_lift = next(c for c in mock_clubs if c["name"] == "Simply Lift")
        assert find_club_by_email(mock_clubs, "JOHN@SIMPLYLIFT.CO") == simply_lift

    def test_surrounding_whitespace_is_ignored(self, mock_clubs):
        simply_lift = next(c for c in mock_clubs if c["name"] == "Simply Lift")
        assert find_club_by_email(mock_clubs, "  john@simplylift.co  ") == simply_lift

    def test_returns_none_when_email_unknown(self, mock_clubs):
        assert find_club_by_email(mock_clubs, "unknown@test.com") is None

    def test_returns_none_on_empty_string(self, mock_clubs):
        assert find_club_by_email(mock_clubs, "") is None

    def test_returns_none_on_whitespace_only_string(self, mock_clubs):
        assert find_club_by_email(mock_clubs, "   ") is None

    def test_returns_none_on_empty_collection(self):
        assert find_club_by_email([], "john@simplylift.co") is None


class TestFindClub:
    """find_club() searches for a club by its 'name' field."""

    def test_returns_matching_club(self, mock_clubs):
        iron_temple = next(c for c in mock_clubs if c["name"] == "Iron Temple")
        assert find_club(mock_clubs, "Iron Temple") == iron_temple

    def test_returns_none_when_name_unknown(self, mock_clubs):
        assert find_club(mock_clubs, "Ghost Club") is None

    def test_returns_none_on_empty_collection(self):
        assert find_club([], "Simply Lift") is None


class TestFindCompetition:
    """find_competition() searches for a competition by its 'name' field."""

    def test_returns_matching_competition(self, mock_competitions):
        fall_classic = next(c for c in mock_competitions if c["name"] == "Fall Classic")
        assert find_competition(mock_competitions, "Fall Classic") == fall_classic

    def test_returns_none_when_name_unknown(self, mock_competitions):
        assert find_competition(mock_competitions, "Winter Cup") is None

    def test_returns_none_on_empty_collection(self):
        assert find_competition([], "Spring Festival") is None
