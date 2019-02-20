import src.Minhash as Minhash


def test_import():
    k = 10
    m = 100
    minhash = Minhash.Minhash(k=k, m=m)
    assert minhash == minhash


def test_initialization():
    k = 10
    m = 100
    minhash = Minhash.Minhash(k=k, m=m)
    assert minhash.k == k
    assert len(minhash.salts) == k
    assert minhash.salts == [i for i in range(k)]


def test_correct_number_of_hash_values_per_data():
    data = [[1, 2], [2, 3, 4], [4, 5, 6, 7]]
    k = 10
    m = 100
    minhash = Minhash.Minhash(k=k, m=m)
    minhash.run(data)
    assert len(minhash.hashes) == len(data)
    for hash_ in minhash.hashes:
        assert len(hash_) == k


def test_hash_function():
    k = 10
    m = 100
    minhash = Minhash.Minhash(k=k, m=m)
    string = 'abc'
    for i in range(100):
        hash_ = minhash._hash(string, i)
        assert hash_ < 100
        assert hash_ >= 0


def test_hashing_row_of_data():
    data = [x for x in range(10)]
    k = 10
    m = 100
    minhash = Minhash.Minhash(k=k, m=m)
    out = minhash._hash_row(data)
    assert len(out) == k


def test_calculating_similarity_returns_correct_values():
    k = 5
    m = 100
    minhash = Minhash.Minhash(k=k, m=m)
    # Mock hashes
    minhash.hashes = [[1, 2, 3, 4, 5],
                      [1, 2, 3, 8, 9],
                      [1, 2, 7, 8, 9]]

    assert minhash.get_similarity(0, 1) == 0.6
    assert minhash.get_similarity(0, 2) == 0.4
    assert minhash.get_similarity(1, 2) == 0.8
