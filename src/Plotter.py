import matplotlib.pyplot as plt
import numpy as np


class Plotter:

    def __init__(self, results_fp, metadata_fp):
        self.data, self.counts = self.extract_clusters(results_fp)
        self.years, year_counts = self.extract_years(metadata_fp)
        self.decades, self.decade_counts = self.years_to_decades(self.years)
        self.all_data = self.combine_clusters_and_decades(self.data,
                                                          self.decades)
        self.n_clusters = len(self.counts.keys())
        self.xlims = (-1.1, 1.1)
        self.ylims = (-1.1, 1.1)

    def plot(self, plot_fp, decade="all", show=True):

        if decade == "all":
            plot_data = self.all_data
        else:
            plot_data = [x for x in self.all_data if x['decade'] == decade]

        for i in range(self.n_clusters):
            curr_data = [x for x in plot_data if x['cluster'] == str(i)]
            count = len(curr_data)

            # Is there a smart, automatic way to determine a good layout?
            ax = plt.subplot(5, 2, i + 1)
            ax.set_xlim(*self.xlims)
            ax.set_ylim(*self.ylims)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            if count != 0:
                X = np.random.uniform(-1, 1, (count, 1))
                Y = np.random.uniform(-1, 1, (count, 1))
                plt.scatter(X, Y, alpha=0.25)

        plt.savefig(plot_fp)
        if show:
            plt.show()
        plt.clf()

    def print_decade_counts(self):

        for i in range(1900, 2016, 1):
            key = str(i)
            try:
                value = self.decade_counts[key]
                print("{}: {}".format(key, value))
            except KeyError:
                pass

    def print_year_counts(self):
        for i in range(1900, 2016, 1):
            key = str(i)
            try:
                value = self.year_counts[key]
                print("{}: {}".format(key, value))
            except KeyError:
                pass

    def print_cluster_counts(self):

        for i in range(10):
            key = str(i)
            value = self.counts[key]
            print("{}: {}".format(key, value))

    def extract_clusters(self, fp):
        data = []
        counts = {}
        with open(fp, 'r') as f:
            for line in f:
                curr = line.split("\n")[0]
                data.append(curr)
                counts[curr] = counts.get(curr, 0) + 1

        return data, counts

    def extract_years(self, fp):
        years = []
        year_counts = {}

        with open(fp, 'r') as f:
            for line in f:
                curr = line.split("\n")[0]
                curr = curr.split("\t")
                year = curr[3]
                years.append(year)
                year_counts[year] = year_counts.get(year, 0) + 1

        return years, year_counts

    def years_to_decades(self, years):
        decades = []
        decade_counts = {}
        for year in years:
            year = int(year)
            decade = year - (year % 10)
            decade = str(decade)
            decades.append(decade)
            decade_counts[decade] = decade_counts.get(decade, 0) + 1

        return decades, decade_counts

    def combine_clusters_and_decades(self, data, decades):

        all_data = []
        for i in range(len(data)):
            curr = {}
            curr['cluster'] = data[i]
            curr['decade'] = decades[i]
            all_data.append(curr)

        return all_data
