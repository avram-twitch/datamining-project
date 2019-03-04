import h5py
import pickle
import multiprocessing as mp
import os


class Data:
    """
    Data processing object.

    Processes raw h5 data files from Million Song Dataset (herafter MSD)
    """

    def __init__(self, h5_files, artist_file, track_file):
        self.h5_files = h5_files
        (self.track_to_id,
         self.artist_to_ids,
         self.id_to_artist_track) = self._read_unique_tracks(track_file)

    def create_data(self, chunks=250, dump_dir="./data/"):
        """
        Processes h5 files into pickled chunks.

        :param h5_files: list of paths to h5 files to be processed.
        :param artist_file: path to artist info csv file.
        :param track_file: path to track info csv file
        :param chunks: number of h5 files to be processed before
                they are downloaded as a pickled file
        :param dump_dir: folder path to directory where pickled files
                will be stored
        :return: None
        """

        if not self._check_dump_dir_exists(dump_dir):
            print("%s does not exist" % dump_dir)
            raise FileNotFoundError

        p_args = self._create_parallel_args(chunks, dump_dir)

        pool = mp.Pool(processes=mp.cpu_count())
        pool.starmap(self._process_chunk, p_args)

    def _check_dump_dir_exists(self, dump_dir):
        return os.path.isdir(dump_dir)

    def _process_chunk(self, files, chunk_start, dump_fp):
        counter = 0

        data = []
        for f in files:
            counter += 1
            print("Processing file %s" % str(counter + chunk_start))
            processed = self._process_file(f)
            data.append(processed)

        self._dump_data(dump_fp, data)
        del data

    def _create_parallel_args(self, chunks, dump_dir):
        # Creates a list of lists, each list being size chunks
        chunked_files = [self.h5_files[x:x + chunks]
                         for x in range(0, len(self.h5_files), chunks)]
        out_args = []
        chunk_start = 0
        file_counter = 0
        for files in chunked_files:
            file_counter += 1
            curr_dump_dir = self._generate_dump_filepath(dump_dir,
                                                         file_counter)
            args = (files, chunk_start, curr_dump_dir)
            out_args.append(args)
            chunk_start += chunks

        return out_args

    def _dump_data(self, dump_fp, data):
        """
        Helper function to dump data.

        :param dump_fp: Filepath to dump location.
        :param data: data to be dumped
        :return: None
        """
        with open(dump_fp, 'wb') as g:
            pickle.dump(data, g)

    def _generate_dump_filepath(self, dump_dir, file_count):
        """
        Helper function to create dump filepath

        :param dump_dir: directory to dump file.
        :param file_count: Number of files already dumped
        :return: string of filepath.
        """
        return dump_dir + "data_" + str(file_count) + ".pkl"

    def _process_file(self, fp):
        """
        Processes a single h5 file into a dictionary object.

        :param fp: Filepath to h5 file to be processed.
        :return: Dictionary with keys to each variable extracted.
        """

        track_id = self._scrub_filepath_for_id(fp)
        artist = self._get_artist(track_id)
        track = self._get_track(track_id)

        h5 = self._read_h5_file(fp)
        loudness = h5['analysis']['segments_loudness_max']
        loudness = self._process_array(loudness, 2, 0)
        pitches = h5['analysis']['segments_pitches']
        all_pitches = self._process_pitches(pitches, 2, 1)
        h5.close()

        out = {'artist': artist,
               'track': track,
               'id': track_id,
               'loudness': loudness,
               'pitches': all_pitches}

        return out

    def _process_array(self, array, k, rounding=1):
        rounded = self._round_array(array, rounding)
        k_grams = self._array_to_k_gram(rounded, k)
        return k_grams

    def _process_pitches(self, pitches, k, rounding=1):
        instrument_pitches = list(zip(*pitches))
        all_pitches = []
        for instrument in instrument_pitches:
            k_grams = self._process_array(instrument, k, rounding)
            all_pitches.extend(k_grams)

        return list(set(all_pitches))

    def _round_array(self, array, rounding):
        """
        Rounds values of an array to _rounding_ significant digits

        :param array: list to be rounded
        :param rounding: significant digits to round to
        :return: list of rounded numbers
        """
        return [round(x, rounding) for x in array]

    def _array_to_k_gram(self, array, k):
        """
        Converts an array into a list of k-grams

        :param array: list to process
        :param k: subsequent values to combine (k-grams)
        :return: list of k-grams
        """
        slices = [array[i:] for i in range(k)]
        return list(set(zip(*slices)))

    def _scrub_filepath_for_id(self, fp):
        """
        Extracts track id from filepath.
        (The MSD format has the track id in the filename)

        :param fp: Filepath of the h5 file to be processed.
        :return: Track ID
        """

        # TODO: Does the track id exist in each h5 file? May be more
        #       robust to get id there

        length = len(fp.split('/'))
        file_name = fp.split('/')[length - 1]
        return file_name.split('.h5')[0]  # Assumes filename is track id

    def _get_artist(self, id):
        """
        Given an id, returns the associated artist

        :param id: Track id
        :return: Name of artist
        """
        return self.id_to_artist_track[id]['artist']

    def _get_track(self, id):
        """
        Given an id, returns the associated track

        :param id: Track id
        :return: Name of track
        """
        return self.id_to_artist_track[id]['track']

    def _read_h5_file(self, fp):
        """
        Wrapper to read an h5 file

        :param fp: Filepath to h5 file
        :return: h5 File object (read only)
        """
        h5 = h5py.File(fp, 'r')
        return h5

    def _read_unique_artists(self, fp):
        """
        Extracts id-artists mappings from unique_artists file

        :param fp: Filepath to unique artists file
        :return: Two dictionaries, one with id as key, and the
                other with artist as key.
                Note that an artist may have multiple ids
        """

        artist_to_id = {}
        id_to_artist = {}
        with open(fp, 'r') as f:
            for row in f:
                id_1, id_2, id_3, artist = row.split("<SEP>")
                curr_item = artist_to_id.get(artist, [])
                curr_item.append(id_3)
                artist_to_id[artist] = curr_item
                id_to_artist[id_3] = artist

        return artist_to_id, id_to_artist

    def _read_unique_tracks(self, fp):
        """
        Extracts id-artists mappings from unique_tracks file

        :param fp: Filepath to unique tracks csv file
        :return: two dictionaries, one with id as key, and the
                other with track as key.
        """

        track_to_id = {}
        artist_to_ids = {}
        id_to_artist_track = {}
        with open(fp, 'r') as f:
            for row in f:
                id_1, id_2, artist, track = row.split("<SEP>")
                curr_item = artist_to_ids.get(artist, [])
                curr_item.append(id_1)
                artist_to_ids[artist] = curr_item
                track_to_id[track] = id_1
                id_to_artist_track[id_1] = {'artist': artist, 'track': track}

        return track_to_id, artist_to_ids, id_to_artist_track
