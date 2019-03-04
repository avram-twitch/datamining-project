import src.Data as Data
import pytest
import os


@pytest.fixture(scope='module')
def setup_data():

    unique_dir = "./MillionSongSubset/AdditionalFiles/"
    unique_artist_fp = unique_dir + "subset_unique_artists.txt"
    unique_tracks_fp = unique_dir + "subset_unique_tracks.txt"
    data_dir = "./raw_data/"
    all_files = os.listdir(data_dir)
    for i in range(len(all_files)):
        all_files[i] = data_dir + all_files[i]
    data = Data.Data(all_files, unique_artist_fp, unique_tracks_fp)
    return data


def test_generate_dump_filepath(setup_data):
    data = setup_data
    dump_dir = "/path/to/dir/"
    file_count = 100
    fp = data._generate_dump_filepath(dump_dir, file_count)
    assert fp == "/path/to/dir/data_100.pkl"


def test_round_array(setup_data):
    data = setup_data
    in_array = [0.1, 0.9, 1.3, 1.8, 2.2, 2.6, 3.1, 3.8, 4.2, 4.8]
    actual_array = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5]
    out_array = data._round_array(in_array, 0)
    assert out_array == actual_array


def test_array_to_k_gram(setup_data):
    data = setup_data
    in_array = [1, 2, 3, 1, 2, 4, 2, 1]
    actual_2_set = set([(1, 2),
                        (2, 3),
                        (3, 1),
                        (1, 2),
                        (2, 4),
                        (4, 2),
                        (2, 1)])
    actual_3_set = set([(1, 2, 3),
                        (2, 3, 1),
                        (3, 1, 2),
                        (1, 2, 4),
                        (2, 4, 2),
                        (4, 2, 1)])
    out_2_set = data._array_to_k_gram(in_array, 2)
    out_3_set = data._array_to_k_gram(in_array, 3)
    assert set(out_2_set) == actual_2_set
    assert set(out_3_set) == actual_3_set


def test_process_array(setup_data):
    data = setup_data
    in_array = [0.1, 0.9, 1.3, 1.8, 2.2, 2.6, 3.1, 3.8, 4.2, 4.8]
    actual_2_set = set([(0, 1),
                        (1, 1),
                        (1, 2),
                        (2, 2),
                        (2, 3),
                        (3, 3),
                        (3, 4),
                        (4, 4),
                        (4, 5)])
    actual_3_set = set([(0, 1, 1),
                        (1, 1, 2),
                        (1, 2, 2),
                        (2, 2, 3),
                        (2, 3, 3),
                        (3, 3, 4),
                        (3, 4, 4),
                        (4, 4, 5)])

    out_2_set = data._process_array(in_array, 2, 0)
    out_3_set = data._process_array(in_array, 3, 0)
    assert set(out_2_set) == actual_2_set
    assert set(out_3_set) == actual_3_set


def test_process_pitches(setup_data):
    data = setup_data
    in_array = [[0.11, 0.16, 0.1],
                [0.16, 0.11, 0.49],
                [0.1, 0.1, 0.4],
                [0.21, 0.36, 0.1]]
    actual_2_set = set([(0.1, 0.2),
                        (0.2, 0.1),
                        (0.1, 0.1),
                        (0.1, 0.4),
                        (0.1, 0.5),
                        (0.5, 0.4),
                        (0.4, 0.1)])
    actual_3_set = set([(0.1, 0.2, 0.1),
                        (0.2, 0.1, 0.2),
                        (0.2, 0.1, 0.1),
                        (0.1, 0.1, 0.4),
                        (0.1, 0.5, 0.4),
                        (0.5, 0.4, 0.1)])
    out_2_set = data._process_pitches(in_array, 2, 1)
    out_3_set = data._process_pitches(in_array, 3, 1)
    assert set(out_2_set) == actual_2_set
    assert set(out_3_set) == actual_3_set


def test_bad_directory_path_raises_error(setup_data):
    data = setup_data
    with pytest.raises(FileNotFoundError):
        data.create_data(dump_dir="./does/not/exist/")
