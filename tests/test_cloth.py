import pytest

from physics import cloth as mod

CASES = [
    ('verlet_step', [[[0, 0]], [[0, 0]], [[1, 0]], 1, 0.9], [[1.0, 0.0]], False),
    ('distance_constraint', [[0, 0], [2, 0], 1, 1], [[0.5, 0.0], [1.5, 0.0]], False),
    ('collide_circle', [[0, 0], [0, 0], 1], [0, 0], False),
    ('collide_circle', [[2, 0], [0, 0], 1], [2, 0], False),
    ('wind_force', [[0, 1], [1, 1], 2], [0, 2], False),
    ('stitch_seam', [[0, 0], [2, 2], 0.5], [1.0, 1.0], True),
    ('substeps', [0.1, 0.03], 4, False),
    ('self_collision_pairs', [[[0, 0], [0.5, 0], [3, 0]], 1], [[0, 1]], False),
    ('lod_stride', [10, 5, 100], 1, False),
    ('lod_stride', [200, 5, 100], 8, False),
    ('anchor_blend', [[0, 0], [2, 4], 0.25], [0.5, 1.0], True),
    ('commit_batch', [[True, True]], True, False),
    ('verlet_step', [[[1, 1]], [[1, 0]], [[0, 0]], 1, 1.0], [[1.0, 2.0]], False),
    ('distance_constraint', [[0, 0], [3, 0], 3, 1], [[0.0, 0.0], [3.0, 0.0]], False),
    ('self_collision_pairs', [[[0, 0], [5, 0]], 1], [], False),
]


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_cloth_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert result == pytest.approx(expected)
    else:
        assert result == expected
