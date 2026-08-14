from game import advance_accumulator, FIXED_DT


def test_accumulator_runs_one_step():
    leftover = advance_accumulator(0.0, FIXED_DT, FIXED_DT, 0.25)
    assert leftover < FIXED_DT


def test_accumulator_accumulates_without_stepping():
    leftover = advance_accumulator(0.0, FIXED_DT / 2, FIXED_DT, 0.25)
    assert leftover == FIXED_DT / 2
    assert int(leftover / FIXED_DT) == 0  # fewer than one step consumed


def test_accumulator_clamps_long_frames():
    assert advance_accumulator(0.0, 0.5, FIXED_DT, 0.25) <= 0.25