import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import copy


class Plotter:

    def __init__(self):
        self.xlims = [-1.1, 1.1]
        self.ylims = [-1.1, 1.1]

    def plot_single_run(self, plot_fp, run, var, values, diff=True):
        n_clusters = len(run)
        data = np.zeros((n_clusters + 1, len(values)))
        cluster_labels = ['all']
        i = 0
        for cluster in run:
            cluster_labels.append("C{}\nn={}".format(i+1, len(cluster)))
            i += 1

        i = 0
        for val in values:
            j = 1
            all_count = 0
            all_filt = 0
            for cluster in run:
                curr = self._filter_by(cluster, (var, val))
                data[j, i] = float(len(curr)) / len(cluster) * 100
                all_count += len(cluster)
                all_filt += len(curr)
                j += 1

            data[0, i] = float(all_filt) / all_count * 100

            i += 1

        if diff:
            percs = copy.deepcopy(data)
            labels = np.empty((n_clusters + 1, len(values)), dtype="<U15")
            for i in range(len(values)):
                curr_pop = data[0, i]
                for j in range(len(run) + 1):
                    data[j, i] = data[j, i] - curr_pop
                    labels[j, i] = "{:.1f}\n({:.1f}%)".format(data[j, i], percs[j, i])


        ax = sns.heatmap(data, xticklabels=values, yticklabels=cluster_labels, annot=labels, linewidths=.5, fmt="")
        ax.set(xlabel=var, ylabel="run (K_N)")
        plt.title("Variable Representation Differences from Population ({}s)".format(var))
        fig = plt.gcf()
        fig.set_size_inches(16, 10)
        plt.savefig(plot_fp)
        plt.clf()

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

        ax = sns.heatmap(data, xticklabels=values, yticklabels=keys, annot=True, fmt='.0f',linewidths=.5)
        ax.set(xlabel=var, ylabel="run (K_N)")
        plt.title("Std. Dev. of Cluster Percentages ({}s)".format(var))
        fig = plt.gcf()
        fig.set_size_inches(16, 10)
        plt.savefig(plot_fp)
        if show:
            plt.show()
        plt.clf()

    def plot_sds_away(self, plot_fp, analyzer, var, values, ks, ns, show=False):
        data = np.zeros((len(ks) * len(ns), len(values)))
        i = 0
        for v in values:
            sds = self._get_max_sds_away(analyzer, var, v, ks, ns)
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

        ax = sns.heatmap(data, xticklabels=values, yticklabels=keys, annot=True, fmt='.0f',linewidths=.5)
        ax.set(xlabel=var, ylabel="run (K_N)")
        plt.title("Max Cluster Std. Dev. away from Population mean ({}s)".format(var))
        fig = plt.gcf()
        fig.set_size_inches(16, 10)
        plt.savefig(plot_fp)
        if show:
            plt.show()
        plt.clf()

    def plot_percs_away(self, plot_fp, analyzer, var, values, ks, ns, show=False):
        data = np.zeros((len(ks) * len(ns), len(values)))
        i = 0
        for v in values:
            percs = self._get_max_percs_away(analyzer, var, v, ks, ns)
            j = 0
            for perc in percs:
                data[j][i] = perc
                j += 1
            i += 1

        keys = []
        for k in ks:
            for n in ns:
                key = self._create_kn_key(k, n)
                keys.append(key)

        ax = sns.heatmap(data, xticklabels=values, yticklabels=keys, annot=True, fmt='.0f',linewidths=.5)
        ax.set(xlabel=var, ylabel="run (K_N)")
        plt.title("Max Perc. away from Population mean ({}s)".format(var))
        fig = plt.gcf()
        fig.set_size_inches(16, 10)
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

    def _get_max_sds_away(self, analyzer, var, val, ks, ns):
        out = []
        runs = analyzer.get_all_cluster_counts(var, val, True)
        for k in ks:
            for n in ns:
                run_key = self._create_kn_key(k, n)
                run = runs[run_key]
                sd = self._get_std_dev_from_counts(run)
                sds_away = self._get_sds_away(run, sd)
                out.append(max(sds_away))

        return out

    def _get_max_percs_away(self, analyzer, var, val, ks, ns):
        out = []
        runs = analyzer.get_all_cluster_counts(var, val, True)
        for k in ks:
            for n in ns:
                run_key = self._create_kn_key(k, n)
                run = runs[run_key]
                percs_away = self._get_perc_away(run)
                out.append(max(percs_away) * 100)

        return out

    def _get_perc_away(self, run):
        all_count = 0
        all_total = 0
        out = []
        for count, total in run:
            all_count += count
            all_total += total
            out.append(float(count) / total)

        all_perc = float(all_count) / all_total

        i = 0
        for count, total in run:
            out[i] = abs(out[i] - all_perc)
            out[i] = out[i] / all_perc
            i += 1

        return out

    def _get_sds_away(self, run, sd):
        all_count = 0
        all_total = 0
        out = []
        for count, total in run:
            all_count += count
            all_total += total
            out.append(float(count) / total)

        all_perc = float(all_count) / all_total

        i = 0
        for count, total in run:
            out[i] = abs(out[i] - all_perc) / sd
            i += 1

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
        ax = sns.heatmap(results, xticklabels=ns, yticklabels=ks, annot=True)

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
