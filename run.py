import os
import sys
from src.RawDataProcessor import RawDataProcessor
from src.DictToMatrix import DictToMatrix
from src.LocalitySensitiveHash import LSH
# from src.Minhash import Minhash
import numpy as np


def process_raw_data():
    """
    Processes raw h5 files into lists of pickled dicts.
    """

    print("Processing raw data into dictionaries")
    data_dir = "./raw_data/"
    dump_dir = "./data/pickled_files/"

    if not os.path.exists(data_dir):
        print("Directory %s does not exists" % data_dir)
        raise FileNotFoundError

    if not os.path.exists(dump_dir):
        print("Directory %s does not exists" % dump_dir)
        raise FileNotFoundError

    all_files = os.listdir(data_dir)
    for i in range(len(all_files)):
        all_files[i] = data_dir + all_files[i]

    data = RawDataProcessor(all_files)
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


def run_lsh():
    """
    Runs Locality Sensitive Hash Analysis
    (For now just looking at a single Kings of leon song)
    """
    tau = 0.85
    lsh = LSH(tau=tau, t=160, r=5, b=32, euclidean=False)
    fp = "./data/matrix_files/pitches_matrix.csv"
    # fp = "./data/matrix_files/loudness_matrix.csv"
    data = np.loadtxt(fp, delimiter=",")
    lsh.hash_data(data)
    kings = data[1]
    out = lsh.query_all_similar(kings)

    with open("./data/matrix_files/metadata.tsv") as f:
        metadata = list(f)
        for item in out:
            print(metadata[item].replace("\n", ""))


if __name__ == '__main__':
    options = {'to_matrix': to_matrix,
               'process_raw': process_raw_data,
               'run_lsh': run_lsh}

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
