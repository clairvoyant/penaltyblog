import pytest

import penaltyblog as pb


def test_dc_model():
    fb = pb.scrapers.FootballData("ENG Premier League", "2019-2020")
    df = fb.get_fixtures()

    clf = pb.models.BayesianRandomInterceptGoalModel(
        df["goals_home"], df["goals_away"], df["team_home"], df["team_away"]
    )
    clf.fit()
    probs = clf.predict("Liverpool", "Wolves")
    assert type(probs) == pb.models.FootballProbabilityGrid
    assert type(probs.home_draw_away) == list
    assert len(probs.home_draw_away) == 3
    assert 0.6 < probs.total_goals("over", 1.5) < 0.8
    assert 0.3 < probs.asian_handicap("home", 1.5) < 0.4
    assert 0.3 < probs.both_teams_to_score < 0.7


def test_unfitted_raises_error():
    fb = pb.scrapers.FootballData("ENG Premier League", "2019-2020")
    df = fb.get_fixtures()
    clf = pb.models.BayesianRandomInterceptGoalModel(
        df["goals_home"], df["goals_away"], df["team_home"], df["team_away"]
    )

    with pytest.raises(ValueError):
        clf.predict("Liverpool", "Wolves")

    with pytest.raises(ValueError):
        clf.get_params()


def test_unfitted_repr():
    fb = pb.scrapers.FootballData("ENG Premier League", "2019-2020")
    df = fb.get_fixtures()
    clf = pb.models.BayesianRandomInterceptGoalModel(
        df["goals_home"], df["goals_away"], df["team_home"], df["team_away"]
    )

    repr = str(clf)
    assert "Status: Model not fitted" in repr
