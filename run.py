import os
import sys
from src.RawDataProcessor import RawDataProcessor
from src.DictToMatrix import DictToMatrix
# from src.Minhash import Minhash


def process_raw_data():
    """
    Processes raw h5 files into lists of pickled dicts.
    """

    print("Processing raw data into dictionaries")
    unique_dir = "./MillionSongSubset/AdditionalFiles/"
    data_dir = "./raw_data/"
    dump_dir = "./data/pickled_files/"
    if not os.path.exists(unique_dir):
        print("Directory %s does not exist" % unique_dir)
        print("Have you downloaded the MillionSongSubset?")
        raise FileNotFoundError

    if not os.path.exists(data_dir):
        print("Directory %s does not exists" % data_dir)
        raise FileNotFoundError

    if not os.path.exists(dump_dir):
        print("Directory %s does not exists" % dump_dir)
        raise FileNotFoundError

    unique_artist_fp = unique_dir + "subset_unique_artists.txt"
    unique_tracks_fp = unique_dir + "subset_unique_tracks.txt"

    all_files = os.listdir(data_dir)
    for i in range(len(all_files)):
        all_files[i] = data_dir + all_files[i]

    data = RawDataProcessor(all_files, unique_artist_fp, unique_tracks_fp)
    data.create_data(chunks=250, dump_dir=dump_dir)


def to_matrix():
    """
    Processes pickled dicts into (sparse) matrices
    """
    print("Processing pickled files into matrices")
    data_dir = "./data/pickled_files/"
    out_data_dir = "./data/matrix_files/"
    if not os.path.exists(data_dir):
        print("Directory %s does not exists" % data_dir)
        raise FileNotFoundError

    if not os.path.exists(out_data_dir):
        print("Directory %s does not exists" % out_data_dir)
        raise FileNotFoundError

    data = DictToMatrix()
    data.run(data_dir, out_data_dir)


def run_minhash():
    """
    Runs a minhash analysis (TODO)
    """
    print("Not yet defined")


if __name__ == '__main__':
    options = {'to_matrix': to_matrix,
               'process_raw': process_raw_data,
               'run_minhash': run_minhash}

    if len(sys.argv) == 1:
        print("Usage: Supply command arg to run a task")
        print("Available tasks: ")
        for key, function in options.items():
            print(key)
            print("\t" + function.__doc__)
    else:
        task_name = sys.argv[1]
        try:
            options[task_name]()
        except KeyError:
            print("'%s' task does not exist" % task_name)
