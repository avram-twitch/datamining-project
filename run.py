import os
import sys
import numpy as np
import time
import csv
import operator

from src.RawDataProcessor import RawDataProcessor
from src.DictToMatrix import DictToMatrix
from src.LloydsClustering import LloydsClustering
from src.KPlusPlus import KPlusPlus
from src.Plotter import Plotter
from src.Analyzer import Analyzer


def process_raw_data(k=4):
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

    data = RawDataProcessor(all_files,
                            pitches_k=k,
                            loudness_k=k,
                            timbre_k=k)
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


def run_lloyds(fp, n=10):
    """
    Runs alteration of Lloyds algorithm
    Performs lloyds normally, but new centers are
    average of _oldest_ songs in cluster.
    """
    meta_fp = 'data/matrix_files/metadata0.tsv'

    start = time.time()
    print("Loading data")
    data = np.genfromtxt(fp, delimiter=',')
    years = []
    with open(meta_fp, 'r') as f:
        for line in f:
            curr = line.split("\n")[0]
            curr = curr.split("\t")
            year = curr[3]
            years.append(year)

    years = np.array(years)
    end = time.time()
    print("Took {}".format(end - start))

    start = time.time()
    gc = KPlusPlus(n)
    print("Running K++")
    gc.fit(data)
    end = time.time()
    print("Took {}".format(end - start))

    centers = gc._centers()
    centers = data[centers, :]
    ll = LloydsClustering(len(centers), centers)
    start = time.time()
    print("Running Lloyds")
    ll.fit(data, years)
    end = time.time()
    print("Took {}".format(end - start))

    print("Assigning clusters...")
    start = time.time()
    centroids = ll._centroids()
    closest_centers = ll.assign_centers_to_data(data, centroids)
    end = time.time()
    print("Took {}".format(end - start))
    return closest_centers


def plot_all():
    """
    Plots using all data
    """
    plot_cluster()


def plot_timbre():
    """
    Plots using timbre data
    """
    clustering_fp = "./results/clusterings_with_timbre.txt"
    out_fp = "./results/timbre_summaries.csv"
    plot(clustering_fp, out_fp)


def plot_cluster_instances():
    """
    Plots data counts of top 5 terms across decades
    """

    clustering_fp = "./results/clusterings_with_all.txt"
    out_fp = "./results/all_summaries.csv"

    ks = [3, 4, 5]
    ns = [4, 5, 6, 7, 8, 9]
    metadata_fp = "./data/matrix_files/metadata0.tsv"
    terms_fp = "./data/matrix_files/terms0.csv"
    results_folder = "./results/"

    files = []
    for k in ks:
        for n in ns:
            fp = "./results/clusterings_with_all_{}_{}.txt".format(k, n)
            curr = (fp, k, n)
            files.append(curr)

    analyzer = Analyzer(files, metadata_fp, terms_fp)
    top_terms = analyzer.get_top_n('term', 10)
    top_terms = [x[0] for x in top_terms]
    top_terms.append(None)

    decades = [str(x) for x in range(1950, 2020, 10)]
    decades.append(None)

    all_summaries = []
    plotter = Plotter()
    for term in top_terms:
        for decade in decades:
            fp = "{}{}-{}-plot.png".format(results_folder, decade, term)
            term_filter = ('term', term)
            decade_filter = ('decade', decade)
            filters = [term_filter, decade_filter]
            c_data = analyzer.get_c_run(4, 9, True)
            plotter.plot_instances(fp, c_data, filters, False)


def cluster_all(n=10, postfix=""):
    """
    Clusters data using all data
    """
    data_fp = "data/matrix_files/all.csv"
    closest_centers = run_lloyds(data_fp, n)
    out_fp = "./results/clusterings_with_all" + postfix + ".txt"

    with open(out_fp, 'w') as f:
        for center in closest_centers:
            f.write("%s\n" % center)

def cluster_timbre(n=10):
    """
    Clusters data using only timbre data
    """

    data_fp = "data/matrix_files/timbre_matrix0.csv"
    closest_centers = run_lloyds(data_fp, n)
    out_fp = "./results/clusterings_with_timbre.txt"

    with open(out_fp, 'w') as f:
        for center in closest_centers:
            f.write("%s\n" % center)

def run(*args):
    """
    Does entire run: processes raw data, runs clustering
    and generates summary results
    Usage: python3 run.py run k [ns...]
    """
    k = int(args[0])
    ns = args[1:]
    ns = [int(n) for n in ns]
    print("Running with k={} and n={}".format(k, ns))

    process_raw_data(k)
    to_matrix()
    to_all()
    for n in ns_cluster:
        print("Clustering with n={}".format(n))
        postfix = "_{}_{}".format(k, n)
        out_fp = "./results/all_summaries" + postfix + ".txt"
        cluster_all(n, postfix)

def to_all():
    folder = "./data/matrix_files/"
    loudness_fp = folder + "loudness_matrix0.csv"
    pitches_fp = folder + "pitches_matrix0.csv"
    timbres_fp = folder + "timbre_matrix0.csv"

    loudness = np.loadtxt(loudness_fp, delimiter=",", dtype=int)
    pitches = np.loadtxt(pitches_fp, delimiter=",", dtype=int)
    timbre = np.loadtxt(timbres_fp, delimiter=",", dtype=int)
    all_data = np.concatenate((loudness, pitches, timbre), axis=1)
    np.savetxt(folder + "all.csv", all_data, fmt="%d", delimiter=",")


if __name__ == '__main__':
    options = {'to_matrix': to_matrix,
               'process_raw': process_raw_data,
               'cluster_all': cluster_all,
               'cluster_timbre': cluster_timbre,
               'plot_cluster': plot_cluster,
               'run': run,
               'plot_all': plot_all,
               'plot_timbre': plot_timbre}

    if len(sys.argv) == 1:
        print("Usage: Supply command arg to run a task")
        print("Available tasks: ")
        for key, function in options.items():
            print(key)
            print("\t" + function.__doc__)
    else:
        task_name = sys.argv[1]
        args = []
        if len(sys.argv) > 2:
            args = sys.argv[2:]

        try:
            options[task_name](*args)
        except KeyError:
            print("'%s' task does not exist" % task_name)
