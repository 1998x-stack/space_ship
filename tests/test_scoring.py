from systems.scoring import Scoring


def test_combo_multiplier(tmp_path):
    s = Scoring(str(tmp_path / "h.txt"))
    for _ in range(20):
        s.add_kill(10)
    assert s.multiplier == 3
    assert s.score == (sum(1 + i // 10 for i in range(1, 21)) * 10)
    s.player_hit()
    assert s.combo == 0
    assert s.multiplier == 1


def test_high_score_persist(tmp_path):
    p = str(tmp_path / "h.txt")
    s = Scoring(p)
    s.score = 500
    s.save_high_score()
    assert Scoring(p).load_high_score() == 500


def test_load_high_score_missing_or_bad(tmp_path):
    good = Scoring(str(tmp_path / "a.txt"))
    good.save_high_score()
    bad = Scoring(str(tmp_path / "b.txt"))
    bad.score = 7
    bad.save_high_score()
    import pathlib
    pathlib.Path(str(tmp_path / "bad.txt")).write_text("not a number")
    assert good.load_high_score() == 0