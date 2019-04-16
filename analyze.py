from src.Analyzer import Analyzer
from src.Plotter import Plotter

def print_all_cluster_term_counts(term, analyzer):
    runs = analyzer.get_all_cluster_counts('term', term, True)
    all_term_count = analyzer.counts['term'][term]
    size = len(analyzer.all_data)
    all_perc = float(all_term_count) / size

    print("Term {}: {} ({:.2f})".format(term, all_term_count, all_perc))
    for k in ks:
        for n in ns:
            run_key = analyzer._create_kn_key(k, n)
            i = 0
            print("Run {}".format(run_key))
            for cluster in runs[run_key]:
                i += 1
                f_count = cluster[0]
                a_count = cluster[1]
                perc = f_count / float(a_count)
                print("Cluster {}: {} ({:.2f})".format(i, f_count, perc))

            print()

def print_all_cluster_term_std_dev(fp, term, analyzer, ks, ns):
    runs = analyzer.get_all_cluster_counts('term', term, True)
    plotter = Plotter()
    plotter.plot_clustering_std_devs(fp, runs, ks, ns)

def generate_files(ks, ns):
    files = []
    for k in ks:
        for n in ns:
            fp = "./results/clusterings_with_all_{}_{}.txt".format(k, n)
            curr = (fp, k, n)
            files.append(curr)

    return files

def plot_sds_of_top_n_variables(fp, analyzer, var, values, ks, ns):
    plotter = Plotter()
    plotter.plot_sds_of_top_n_variables(fp, analyzer, var, values, ks, ns, False)

def plot_sds_away(fp, analyzer, var, values, ks, ns):
    plotter = Plotter()
    plotter.plot_sds_away(fp, analyzer, var, values, ks, ns, False)

def plot_percs_away(fp, analyzer, var, values, ks, ns):
    plotter = Plotter()
    plotter.plot_percs_away(fp, analyzer, var, values, ks, ns, False)

def plot_single_run(run, top_terms, top_artists, decades):
    plotter = Plotter()
    plotter.plot_single_run("./results/terms_cluster.png", run, 'term', top_terms)
    plotter.plot_single_run("./results/decades_cluster.png", run, 'decade', decades)
    plotter.plot_single_run("./results/artists_cluster.png", run, 'artist', top_artists)

def plot_counts(fp, counts, var, values):
    plotter = Plotter()
    plotter.plot_bar_all_counts(fp, counts, var, values)

if __name__=='__main__':

    ks = [3, 4, 5]
    ns = [4, 5, 6, 7, 8, 9]
    metadata_fp = "./data/matrix_files/metadata0.tsv"
    terms_fp = "./data/matrix_files/terms0.csv"

    files = generate_files(ks, ns)
    analyzer = Analyzer(files, metadata_fp, terms_fp)
    top_terms = analyzer.get_top_n('term', 10)
    top_terms = [x[0] for x in top_terms]
    top_artists = analyzer.get_top_n('artist', 10)
    top_artists = [x[0] for x in top_artists]
    decades = list(range(1920, 2020, 10))
    decades = [str(x) for x in decades]
    trunc_decades = list(range(1950, 2020, 10))
    trunc_decades = [str(x) for x in trunc_decades]
#    plot_sds_of_top_n_variables("./results/sd_terms.png", analyzer, 'term', top_terms, ks, ns)
#    plot_sds_of_top_n_variables("./results/sd_artists.png", analyzer, 'artist', top_artists, ks, ns)
#    plot_sds_of_top_n_variables("./results/sd_decades.png", analyzer, 'decade', decades, ks, ns)
#    plot_sds_away("./results/sd_away_terms.png", analyzer, 'term', top_terms, ks, ns)
#    plot_sds_away("./results/sd_away_artists.png", analyzer, 'artist', top_artists, ks, ns)
#    plot_sds_away("./results/sd_away_decades.png", analyzer, 'decade', decades, ks, ns)
#    plot_percs_away("./results/perc_away_terms.png", analyzer, 'term', top_terms, ks, ns)
#    plot_percs_away("./results/perc_away_artists.png", analyzer, 'artist', top_artists, ks, ns)
#    plot_percs_away("./results/perc_away_decades.png", analyzer, 'decade', decades, ks, ns)
#    plot_percs_away("./results/perc_away_trunc_decades.png", analyzer, 'decade', trunc_decades, ks, ns)

#    plot_single_run(analyzer.get_c_run(5, 4, large=False), top_terms, top_artists, decades)
    plot_counts("./results/decade_counts.png", analyzer.counts, 'decade', decades)
    plot_counts("./results/term_counts.png", analyzer.counts, 'term', top_terms)
    plot_counts("./results/artist_counts.png", analyzer.counts, 'artist', top_artists)

