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
    plot_sds_of_top_n_variables("./results/terms.png", analyzer, 'term', top_terms, ks, ns)
    plot_sds_of_top_n_variables("./results/artists.png", analyzer, 'artist', top_artists, ks, ns)
    plot_sds_of_top_n_variables("./results/decades.png", analyzer, 'decade', decades, ks, ns)
