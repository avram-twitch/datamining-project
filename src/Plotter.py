import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class Plotter:

    def __init__(self):
        self.xlims = [-1.1, 1.1]
        self.ylims = [-1.1, 1.1]

    def plot_sds_of_top_n_variables(self, plot_fp, analyzer, var, values, ks, ns, show=False):
        data = np.zeros((len(ks) * len(ns), len(values)))
        i = 0
        for v in values:
            sds = self._get_sds(analyzer, var, v, ks, ns)
            j = 0
            for sd in sds:
                data[j][i] = sd
                j += 1
            i += 1

        keys = []
        for k in ks:
            for n in ns:
                key = self._create_kn_key(k, n)
                keys.append(key)

        ax = sns.heatmap(data, xticklabels=values, yticklabels=keys)
        plt.savefig(plot_fp)
        if show:
            plt.show()
        plt.clf()


    def _get_sds(self, analyzer, var, val, ks, ns):
        out = []
        runs = analyzer.get_all_cluster_counts(var, val, True)
        for k in ks:
            for n in ns:
                run_key = self._create_kn_key(k, n)
                run = runs[run_key]
                sd = self._get_std_dev_from_counts(run)
                out.append(sd)

        return out

    def plot_clustering_std_devs(self, plot_fp, runs, ks, ns, show=False):
        i = 0
        results = np.zeros((len(ks), len(ns)))
        k_count = 0
        n_count = 0
        min_n = min(ns)
        max_n = max(ns)
        min_k = min(ks)
        max_k = max(ks)

        for k in ks:
            for n in ns:
                run_key = self._create_kn_key(k, n)
                run = runs[run_key]
                sd = self._get_std_dev_from_counts(run)
                results[k_count, n_count] = sd
                n_count += 1
            n_count = 0
            k_count += 1

        extent = (min_n, max_n, min_k, max_k)
        # plt.imshow(results, cmap='hot', interpolation='nearest', extent=extent)
        ax = sns.heatmap(results, xticklabels=ns, yticklabels=ks)

        plt.savefig(plot_fp)
        if show:
            plt.show()
        plt.clf()

    def plot_instances(self, plot_fp, plot_data, filters, show):

        all_count = sum([len(x) for x in plot_data])
        i = 0
        for cluster in plot_data:
            unfiltered_count = len(cluster)
            f_cluster = cluster
            for _filter in filters:
                f_cluster = self._filter_by(f_cluster, _filter)

            count = len(f_cluster)
            perc = float(count) / unfiltered_count * 100

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
            i += 1

        plt.savefig(plot_fp)
        if show:
            plt.show()
        plt.clf()

    def _filter_by(self, data, f_tuple):
        key, value = f_tuple
        if value is None:
            return data

        if key == 'term':
            return [x for x in data if value in x[key]]
        else:
            return [x for x in data if x[key] == value]

    def _create_kn_key(self, k, n):
        return "{}_{}".format(k, n)

    def _get_std_dev_from_counts(self, run):
        values = []
        for count, total in run:
            values.append(float(count) / total)

        return np.std(values)
