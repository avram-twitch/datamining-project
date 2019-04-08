import h5py
import operator


def get_metadata(fp):
    out = []
    with open(fp, 'r') as f:
        for line in f:
            curr = line.split("\n")[0]
            curr = curr.split("\t")
            _id = curr[2]
            out.append(_id)

    return out


def read_h5_file(fp):
    return h5py.File(fp, 'r')

def write_top_tags(fp, top_tags):
    with open(fp, 'w') as f:
        for tag in top_tags:
            f.write("{}\n".format(tag))

def to_string(x):
    return x.decode("UTF-8")

def write_tags(fp, tags):
    with open(fp, 'w') as f:
        for terms in tags:
            curr = map(to_string, terms)
            out = ",".join(curr)
            f.write("{}\n".format(out))

if __name__=='__main__':
    metadata_fp = "./data/matrix_files/metadata.tsv"
    rawdata_folder = "./raw_data/"
    ids = get_metadata(metadata_fp)

    genres = {}
    all_terms = []
    for _id in ids:
        with read_h5_file(rawdata_folder + _id + ".h5") as h5:
            terms = list(h5['metadata']['artist_terms'])
            all_terms.append(terms)
            for term in terms:
                curr_term = str(term)
                genres[curr_term] = genres.get(curr_term, 0) + 1

    write_tags("./data/matrix_files/terms.txt", all_terms)
    sorted_genres = sorted(genres.items(), key=operator.itemgetter(1))
    top_tags = []

    for genre, count in sorted_genres:
        print("{}: {}".format(genre, count))
        if count >= 1000:
            top_tags.append(genre)

    write_top_tags("./results/top_tags.txt", top_tags)
