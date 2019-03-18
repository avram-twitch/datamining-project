import src.LocalitySensitiveHash as LSH
import pytest
import numpy as np


@pytest.fixture(scope='module')
def setup_data():

    tau = 0.85
    t = 160
    r = 5
    b = 32
    euclidean = False
    lsh = LSH.LSH(tau=tau, t=t, r=r, b=b, euclidean=euclidean)
    return lsh


def test_convert_to_unit(setup_data):

    lsh = setup_data
    random_vectors = [np.random.rand(100) for x in range(10)]
    for v in random_vectors:
        unit_vector = lsh._convert_to_unit(v)
        norm = np.linalg.norm(unit_vector)
        assert pytest.approx(norm) == 1.0


def test_generate_jaccard_hashes(setup_data):

    lsh = setup_data
    t = 160
    d = 100
    lsh._generate_jaccard_hashes(t=t, d=d)
    assert len(lsh.vectors) == t
    assert len(lsh.offsets) == t


def test_generate_unit_vector(setup_data):

    lsh = setup_data

    for d in range(10):
        out = lsh._generate_unit_vector(d)
        assert len(out) == d
