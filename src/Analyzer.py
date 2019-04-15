import numpy as np


class Analyzer:

    def __init__(self, cluster_files, metadata_fp, terms_fp):
        self.keys = ['term', 'year', 'decade', 'artist']
        self.LARGE = 100
        years, artists = self._load_metadata(metadata_fp)
        decades = self._years_to_decades(years)
        terms = self._load_terms(terms_fp)
        c_runs = self._load_clusters(cluster_files)
        self._combine_all(years, artists, decades, terms, c_runs)
        self.counts = self._generate_counts(self.all_data)
        self.ord_counts = self._generate_ordered_counts(self.counts)

    def get_c_run(self, k, n, large=True):
        run_key = self._create_kn_key(k, n)
        out = []
        for i in range(n):
            cluster = str(i)
            c_data = self._filter_by(self.all_data, (run_key, cluster))
            c_size = len(c_data)
            if large and c_size < self.LARGE:
                continue
            out.append(c_data)

        return out

    def get_top_n(self, key, n=5):
        return self.ord_counts[key][:n]

    def print_top_n(self, key, n=5):

        for item in self.get_top_n(key, n):
            k, v = item
            print("{}: {}".format(k, v))

    def get_all_cluster_counts(self, key, value, large=True):
        c_counts = {}
        for n in self.ns:
            for k in self.ks:
                run_key = self._create_kn_key(k, n)
                curr = self._get_cluster_count(key, value, k, n, large)
                c_counts[run_key] = curr
        return c_counts

    def _get_cluster_count(self, key, value, k, n, large=True):

        run_key = self._create_kn_key(k, n)
        out = []
        for i in range(n):
            cluster = str(i)
            c_data = self._filter_by(self.all_data, (run_key, cluster))
            c_size = len(c_data)
            if large and c_size < self.LARGE:
                continue
            filtered_data = self._filter_by(c_data, (key, value))
            f_size = len(filtered_data)
            out.append((f_size, c_size))

        return out

    def _filter_by(self, data, f_tuple):
        key, value = f_tuple
        if key == 'term':
            return [x for x in data if value in x[key]]
        else:
            return [x for x in data if x[key] == value]

    def _generate_counts(self, data):

        counts = {}
        for key in self.keys:
            counts[key] = {}

        for item in data:
            for key in self.keys:
                val = item[key]
                if key == 'term':
                    for term in val:
                        self._inc_key(counts[key], term)
                else:
                    self._inc_key(counts[key], val) 

        return counts

    def _generate_ordered_counts(self, counts):
        ord_counts = {}
        for key in self.keys:
            ord_counts[key] = self._order_counts(counts[key])

        return ord_counts

    def _order_counts(self, counts):
        out = []
        for k, v in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            out.append((k, v))

        return out

    def _inc_key(self, d, key):
        d[key] = d.get(key, 0) + 1

    def _combine_all(self, years, artists, decades, terms, c_runs):

        self.all_data = []
        for i in range(len(years)):
            curr = {}
            curr['year'] = years[i]
            curr['term'] = terms[i]
            curr['decade'] = decades[i]
            curr['artist'] = artists[i]
            for key, value in c_runs.items():
                curr[key] = value[i]

            self.all_data.append(curr)

    def _load_metadata(self, fp):
        years = []
        artists = []
        with open(fp, 'r') as f:
            for line in f:
                curr = line.split("\n")[0]
                curr = curr.split("\t")
                year = curr[3]
                artist = curr[0]
                years.append(year)
                artists.append(artist)

        return years, artists

    def _load_terms(self, fp):
        terms = []
        with open(fp, 'r') as f:
            for line in f:
                curr_terms = line.split("\n")[0]
                curr_terms = curr_terms.split(",")
                terms.append(curr_terms)

        return terms

    def _load_clusters(self, files):

        c_runs = {}
        self.ks = []
        self.ns = []

        for fp, k, n in files:
            key = self._create_kn_key(k, n)
            self.ks.append(k)
            self.ns.append(n)
            curr_data = self._extract_clusters(fp)
            c_runs[key] = curr_data

        return c_runs

    def _extract_clusters(self, fp):
        data = []
        with open(fp, 'r') as f:
            for line in f:
                curr = line.split("\n")[0]
                data.append(curr)

        return data

    def _years_to_decades(self, years):
        decades = []
        for year in years:
            year = int(year)
            decade = year - (year % 10)
            decade = str(decade)
            decades.append(decade)

        return decades

    def _create_kn_key(self, k, n):
        return "{}_{}".format(k, n)
