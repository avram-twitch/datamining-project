from src.Analyzer import Analyzer

if __name__=='__main__':

    ks = [3, 4, 5]
    ns = [4, 5, 6, 7, 8, 9]
    metadata_fp = "./data/matrix_files/metadata0.tsv"
    terms_fp = "./data/matrix_files/terms0.csv"

    files = []
    for k in ks:
        for n in ns:
            fp = "./results/clusterings_with_all_{}_{}.txt".format(k, n)
            curr = (fp, k, n)
            files.append(curr)

    analyzer = Analyzer(files, metadata_fp, terms_fp)
    term = 'rock'
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
