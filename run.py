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
    clustering_fp = "./results/clusterings_with_all.txt"
    out_fp = "./results/all_summaries.csv"
    plot(clustering_fp, out_fp)


def plot_timbre():
    clustering_fp = "./results/clusterings_with_timbre.txt"
    out_fp = "./results/timbre_summaries.csv"
    plot(clustering_fp, out_fp)


def plot(clustering_fp, out_fp):

    top_terms_fp = "./results/top_tags.txt"
    metadata_fp = "./data/matrix_files/metadata0.tsv"
    terms_fp = "./data/matrix_files/terms0.csv"
    results_folder = "./results/"

    top_terms = []
    with open(top_terms_fp, 'r') as f:
        for line in f:
            curr = line.split("\n")[0]
            top_terms.append(curr)

    top_terms.append(None)
    decades = [str(x) for x in range(1950, 2020, 10)]
    decades.append("all")

    all_summaries = []
    plotter = Plotter(clustering_fp, metadata_fp, terms_fp)
    for term in top_terms:
        for decade in decades:
            curr = []
            filtered = plotter.filter_data(decade, term)
            summary = plotter.summarize_to_clusters(filtered)
            curr.append(decade)
            curr.append(term)
            curr.append(summary['mean'])
            curr.append(summary['stddev'])
            all_summaries.append(curr)

    sorted_summaries = sorted(all_summaries,
                              key=operator.itemgetter(3),
                              reverse=True)
    for i in range(10):
        decade = sorted_summaries[i][0]
        term = sorted_summaries[i][1]
        fp = "{}{}-{}-plot.png".format(results_folder, decade, term)
        plotter.filter_and_plot(fp, decade, term, False)

    with open(out_fp, 'w') as f:
        wr = csv.writer(f)
        wr.writerows(all_summaries)


def cluster_all(n=10, postfix=""):
    data_fp = "data/matrix_files/all.csv"
    closest_centers = run_lloyds(data_fp, n)
    out_fp = "./results/clusterings_with_all" + postfix + ".txt"

    with open(out_fp, 'w') as f:
        for center in closest_centers:
            f.write("%s\n" % center)

def cluster_timbre(n=10):

    data_fp = "data/matrix_files/timbre_matrix0.csv"
    closest_centers = run_lloyds(data_fp, n)
    out_fp = "./results/clusterings_with_timbre.txt"

    with open(out_fp, 'w') as f:
        for center in closest_centers:
            f.write("%s\n" % center)

def run(k, n):
    k = int(k)
    n = int(n)
    postfix = "_{}_{}".format(k, n)
    clustering_fp = "./results/clusterings_with_all" + postfix + ".txt"
    out_fp = "./results/all_summaries" + postfix + ".txt"
    # data_fp = "data/matrix_files/all.csv"
    print("Running with k={} and n={}".format(k, n))

    #process_raw_data(k)
    to_matrix()
    to_all()
    cluster_all(n, postfix)
    plot(clustering_fp, out_fp)

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
               'plot': plot,
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
