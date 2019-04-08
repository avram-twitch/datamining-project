import os
import sys
import numpy as np
import time
import csv

from src.RawDataProcessor import RawDataProcessor
from src.DictToMatrix import DictToMatrix
from src.LloydsClustering import LloydsClustering
from src.KPlusPlus import KPlusPlus
from src.Plotter import Plotter


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


def run_lloyds():
    """
    Runs alteration of Lloyds algorithm
    Performs lloyds normally, but new centers are
    average of _oldest_ songs in cluster.
    """
    k = 10
    fp = 'data/matrix_files/all.csv'
    meta_fp = 'data/matrix_files/years.txt'

    start = time.time()
    print("Loading data")
    data = np.genfromtxt(fp, delimiter=',')
    years = np.genfromtxt(meta_fp)
    end = time.time()
    print("Took {}".format(end - start))

    start = time.time()
    gc = KPlusPlus.KPlusPlus(k)
    print("Running K++")
    gc.fit(data)
    end = time.time()
    print("Took {}".format(end - start))

    # centers = data[:k,:]
    centers = gc._centers()
    centers = data[centers, :]
    ll = LloydsClustering.LloydsClustering(len(centers), centers)
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

    with open("results.txt", 'w') as f:

        for center in closest_centers:
            f.write("%s\n" % center)


def plot():
    """
    Simple plots of results.txt
    Plots each cluster in a separate plot.
    Plots all data, then creates plots for each decade
    """
    clustering_fp = "./results/clusterings.txt"
    metadata_fp = "./data/matrix_files/metadata.tsv"
    terms_fp = "./data/matrix_files/terms.txt"
    results_folder = "./results/"
    plotter = Plotter(clustering_fp, metadata_fp, terms_fp)
    args = [("all.png", "all"),
            ("1950.png", "1950"),
            ("1960.png", "1960"),
            ("1970.png", "1970"),
            ("1980.png", "1980"),
            ("1990.png", "1990"),
            ("2000.png", "2000"),
            ("2010.png", "2010")]
    for arg in args:
        fp = arg[0]
        decade = arg[1]
        plotter.filter_and_plot(results_folder + fp, decade, None, False)

def plot_terms():
    clustering_fp = "./results/clusterings.txt"
    metadata_fp = "./data/matrix_files/metadata.tsv"
    terms_fp = "./data/matrix_files/terms.txt"
    results_folder = "./results/"
    plotter = Plotter(clustering_fp, metadata_fp, terms_fp)
    plotter.filter_and_plot(results_folder + "rock.png", "all", "rock", False)

def summarize_top_terms():
    top_terms_fp = "./results/top_tags.txt"
    top_terms = []
    with open(top_terms_fp, 'r') as f:
        for line in f:
            curr = line.split("\n")[0]
            top_terms.append(curr)

    all_summaries = []
    clustering_fp = "./results/clusterings.txt"
    metadata_fp = "./data/matrix_files/metadata.tsv"
    terms_fp = "./data/matrix_files/terms.txt"
    results_folder = "./results/"
    plotter = Plotter(clustering_fp, metadata_fp, terms_fp)
    for term in top_terms:
        curr = []
        filtered = plotter.filter_data("all", term)
        summary = plotter.summarize_to_clusters(filtered)
        curr.append(term)
        curr.append(summary['mean'])
        curr.append(summary['stddev'])
        all_summaries.append(curr)

    with open("./results/all_summaries.csv", 'w') as f:
        wr = csv.writer(f)
        wr.writerows(all_summaries)
#        for line in all_summaries:
#            wr.writerow(line)


if __name__ == '__main__':
    options = {'to_matrix': to_matrix,
               'process_raw': process_raw_data,
               'run_lloyds': run_lloyds,
               'plot': plot,
               'plot_terms': plot_terms,
               'top_terms': summarize_top_terms}

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
