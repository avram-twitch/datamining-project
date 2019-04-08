import matplotlib.pyplot as plt
import numpy as np


class Plotter:

    def __init__(self, results_fp, metadata_fp, terms_fp):
        self.data, self.counts = self.extract_clusters(results_fp)
        self.years, self.year_counts = self.extract_years(metadata_fp)
        self.terms, self.term_counts = self.extract_terms(terms_fp)
        self.decades, self.decade_counts = self.years_to_decades(self.years)
        self.all_data = self.combine_data(self.data,
                                          self.decades,
                                          self.terms)
        self.n_clusters = len(self.counts.keys())
        self.xlims = (-1.1, 1.1)
        self.ylims = (-1.1, 1.1)
        self.unfiltered_counts = []
        for i in range(self.n_clusters):
            count = len([x for x in self.all_data if x['cluster'] == str(i)])
            self.unfiltered_counts.append(count)

    def filter_data(self, decade="all", term=None):
        if decade == "all":
            data = self.all_data
        else:
            data = [x for x in self.all_data if x['decade'] == decade]

        if term is not None:
            data = [x for x in data if term in x['terms']]

        return data

    def plot(self, plot_fp, decade="all", show=True, term=None):

        if decade == "all":
            plot_data = self.all_data
        else:
            plot_data = [x for x in self.all_data if x['decade'] == decade]

        if term is not None:
            plot_data = [x for x in plot_data if term in x['terms']]

        for i in range(self.n_clusters):
            curr_data = [x for x in plot_data if x['cluster'] == str(i)]
            count = len(curr_data)
            unfiltered_count = self.unfiltered_counts[i]

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
            plt.text(0, 0, "{}/{}\n{:.0f}%".format(count, unfiltered_count, count / unfiltered_count * 100))

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

    def extract_terms(self, fp):
        all_terms = []
        term_counts = {}

        with open(fp, 'r') as f:
            for line in f:
                curr_terms = line.split("\n")[0]
                curr_terms = curr_terms.split(",")
                all_terms.append(curr_terms)
                for term in curr_terms:
                    term_counts[term] = term_counts.get(term, 0) + 1
        return all_terms, term_counts

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

    def combine_data(self, data, decades, terms):

        all_data = []
        for i in range(len(data)):
            curr = {}
            curr['cluster'] = data[i]
            curr['decade'] = decades[i]
            curr['terms'] = terms[i]
            all_data.append(curr)

        return all_data
