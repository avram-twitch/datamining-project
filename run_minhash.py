import src.Minhash as Minhash
import os
import pickle as pkl

global_minhash = Minhash.Minhash(k=100, m=1000)


def get_all_pickle_files(data_dir):

    pickle_files = os.listdir(data_dir)
    return [data_dir + f for f in pickle_files]


def iterate_over_pickle_files(pickle_files):

    num_files = len(pickle_files)

    for i in range(num_files):
        curr_file = pickle_files[i]
        rest_of_files = pickle_files[i + 1:]
        curr_pf = open_pickle_file(curr_file)
        compare_pickle_files(curr_pf, rest_of_files)


def compare_pickle_files(curr_pf, rest_of_files):

    compare_to_self(curr_pf)


def compare_to_self(curr_pf):

    pf_size = len(curr_pf)

    for i in range(pf_size - 1):
        for j in range(i + 1, pf_size):
            first = curr_pf[i]['loudness']
            second = curr_pf[j]['loudness']
            sim = global_minhash.get_arb_similarity(first, second)
            print("%s--%s: %s" % (str(i), str(j), str(sim)))


def open_pickle_file(pf):
    with open(pf, 'rb') as f:
        out = pkl.load(f)
    return out


if __name__ == '__main__':

    data_dir = "./data/"
    pickle_files = get_all_pickle_files(data_dir)
    iterate_over_pickle_files(pickle_files)
