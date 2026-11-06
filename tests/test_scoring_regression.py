from systems.scoring import Scoring


def test_lower_score_does_not_erase_record(tmp_path):
    path = tmp_path / "high.txt"
    path.write_text("900")
    score = Scoring(str(path))
    score.score = 100
    score.save_high_score()
    assert score.load_high_score() == 900


def test_new_record_is_saved(tmp_path):
    path = tmp_path / "high.txt"
    path.write_text("100")
    score = Scoring(str(path))
    score.score = 900
    score.save_high_score()
    assert score.load_high_score() == 900


def test_missing_record_is_created(tmp_path):
    path = tmp_path / "high.txt"
    score = Scoring(str(path))
    score.score = 300
    score.save_high_score()
    assert score.load_high_score() == 300
