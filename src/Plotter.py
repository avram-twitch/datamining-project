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
        self.unfiltered_counts = {}
        for i in range(self.n_clusters):
            count = len([x for x in self.all_data if x['cluster'] == str(i)])
            cluster = str(i)
            self.unfiltered_counts[cluster] = count

        self.LARGE = 100

    def filter_data(self, decade="all", term=None):
        if decade == "all":
            data = self.all_data
        else:
            data = [x for x in self.all_data if x['decade'] == decade]

        if term is not None:
            data = [x for x in data if term in x['terms']]

        return data

    def summarize_to_clusters(self, data):
        out_data = {}
        all_percentages = []
        for i in range(self.n_clusters):
            cluster = str(i)
            curr_data = [x for x in data if x['cluster'] == cluster]
            count = len(curr_data)
            percentage = float(count) / self.unfiltered_counts[cluster]
            all_percentages.append(percentage)
            curr = {}
            curr['count'] = count
            curr['total_count'] = self.unfiltered_counts[cluster]
            curr['percentage'] = percentage
            curr['cluster'] = cluster
            out_data[cluster] = curr

        mean_p = np.mean(all_percentages)
        std_dev_p = np.std(all_percentages)
        out_data['mean'] = mean_p
        out_data['stddev'] = std_dev_p
        return out_data

    def plot(self, plot_fp, plot_data, show):

        for i in range(self.n_clusters):
            cluster = str(i)
            curr_data = plot_data[cluster]
            count = curr_data['count']
            unfiltered_count = curr_data['total_count']
            perc = curr_data['percentage'] * 100

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
            plt.text(0, 0, "{}/{}\n{:.0f}%".format(count,
                                                   unfiltered_count,
                                                   perc))

        plt.savefig(plot_fp)
        if show:
            plt.show()
        plt.clf()

    def filter_and_plot(self, plot_fp, decade="all", term=None, show=True):
        filtered = self.filter_data(decade, term)
        plot_data = self.summarize_to_clusters(filtered)
        self.plot(plot_fp, plot_data, show)

    def get_top_n_genres(self, n=5):

        genres = self.get_genre_counts(self.all_data)
        length = len(self.all_data)
        out = {}
        for key, value in sorted(genres.items(), key=lambda item: item[1], reverse=True):
            if j == n:
                break
            out[key] = {}
            out[key]['count'] = value
            out[key]['perc'] = float(value) / length
            j += 1

        return out

    def get_top_n_genres_per_cluster(self, n=5, large=True):

        for i in range(self.n_clusters):
            cluster = str(i)
            c_data = [x for x in self.all_data if x['cluster'] == cluster]
            data_length = len(c_data)
            if large and data_length < self.LARGE:
                continue
            genres = self.get_genre_counts(c_data)
            print("Cluster {}".format(cluster))
            j = 0
            for key, value in sorted(genres.items(), key=lambda item: item[1], reverse=True):
                if j == n:
                    break
                print("{}. {}: {} ({})".format(j + 1, key, value, float(value)/data_length))
                j += 1

            print()

    def get_top_n_genres_all_data(self, n=5, large=True):

        genres = self.get_genre_counts(self.all_data)

        j = 0
        for key, value in sorted(genres.items(), key=lambda item: item[1], reverse=True):
            if j == n:
                break

            all_perc = float(value) / len(self.all_data)
            print("Term {}. {}: {}--{:.2f}".format(j, key, value, all_perc))
            for i in range(self.n_clusters):
                cluster = str(i)
                c_data = [x for x in self.all_data if x['cluster'] == cluster]
                cluster_len = len(c_data)
                cluster_genres = self.get_genre_counts(c_data)
                cluster_count = cluster_genres.get(key, 0)
                cluster_perc = float(cluster_count) / cluster_len
                diff = all_perc - cluster_perc
                if large and cluster_len < self.LARGE:
                    continue
                print("Cluster {}: {}--{:.2f} ({:.2f})".format(cluster, cluster_count, cluster_perc, diff))

            j += 1
            print()


    def get_genre_counts(self, data):
        genres = {}
        data_length = len(data)
        for item in data:
            for term in item['terms']:
                genres[term] = genres.get(term, 0) + 1

        for key, value in genres.items():
            genres[key] = value
        return genres


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
