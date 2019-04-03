import pickle as pkl
import numpy as np
import os


class DictToMatrix:
    """
    Converts the pickled files that RawDataProcessor produces
    into a numpy array
    """

    def __init__(self):
        self.max_features = {}
        # self.max_feature = 0

    def run(self, data_dir, out_data_dir):
        p_files = os.listdir(data_dir)

        all_meta = []
        all_loudness = []
        all_pitches = []
        all_timbre = []
        chunk = 5
        count = 0
        file_count = 0
        for f in p_files:
            pf_data = self.open_pickle_file(data_dir + f)
            for row in pf_data:
                meta_data, loudness, pitches, timbre = self.process_file(row)
                all_meta.append(meta_data)
                all_loudness.append(loudness)
                all_pitches.append(pitches)
                all_timbre.append(timbre)

            count += 1
            if count % chunk == 0:
                self.save_files(all_loudness, all_pitches, all_timbre, all_meta, out_data_dir, file_count)
                file_count += 1
                del all_meta
                del all_loudness
                del all_pitches
                del all_timbre
                all_meta = []
                all_loudness = []
                all_pitches = []
                all_timbre = []

        self.save_files(all_loudness, all_pitches, all_timbre, all_meta, out_data_dir, file_count)

    def save_files(self, all_loudness, all_pitches, all_timbre, all_meta, out_data_dir, count):
        print("Saving file {}".format(count))
        out_loudness = self.unequal_lists_to_np_array(all_loudness, 'loudness')
        out_pitches = self.unequal_lists_to_np_array(all_pitches, 'pitches')
        out_timbre = self.unequal_lists_to_np_array(all_timbre, 'timbre')
        out_meta = np.array(all_meta)

        np.savetxt(
            out_data_dir + "loudness_matrix" + str(count) + ".csv",
            out_loudness,
            delimiter=',',
            fmt="%d")
        np.savetxt(
            out_data_dir + "pitches_matrix" + str(count) + ".csv",
            out_pitches,
            delimiter=',',
            fmt="%d")
        np.savetxt(
            out_data_dir + "timbre_matrix" + str(count) + ".csv",
            out_timbre,
            delimiter=',',
            fmt="%d")
        np.savetxt(
            out_data_dir + "metadata" + str(count) + ".tsv", out_meta, delimiter='\t', fmt="%s")


    def open_pickle_file(self, fp):
        with open(fp, 'rb') as f:
            out = pkl.load(f)

        return out

    def process_file(self, data):

        artist = data['artist']
        track = data['track'].split("\n")[0]
        id_ = data['id']
        year = data['year']
        meta_data = [artist, track, id_, year]
        loudness_data = self.expand_libsvm_to_list(data['loudness'],
                                                   'loudness')
        pitches_data = self.expand_libsvm_to_list(data['pitches'], 'pitches')
        timbre_data = self.expand_libsvm_to_list(data['timbre'], 'timbre')
        return meta_data, loudness_data, pitches_data, timbre_data

    def expand_libsvm_to_list(self, array, feature):

        self.max_features[feature] = self.max_features.get(feature, 0)
        int_keys = [int(key) for key in array.keys()]
        max_key = max(int_keys)
        if max_key + 1 > self.max_features[feature]:
            self.max_features[feature] = max_key + 1

        out_list = [0 for i in range(self.max_features[feature])]
        for key, item in array.items():
            out_list[int(key)] = int(item)

        return out_list

    def unequal_lists_to_np_array(self, lists, feature):
        out_array = np.zeros([len(lists),
                             self.max_features[feature]],
                             dtype=int)
        for n, data in enumerate(lists):
            out_array[n][0:len(data)] = data

        return out_array
