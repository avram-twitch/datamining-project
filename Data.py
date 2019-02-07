import h5py

class Data:

    def __init__(self):
        pass

    def create_data(self, h5_files, artist_file, track_file):

        self.track_to_id, \
        self.artist_to_ids, \
        self.id_to_artist_track = self._read_unique_tracks(track_file)

        data = []

        for f in h5_files:
            processed = self._process_file(f)
            data.append(processed)

        self.data = data
        return data

    def _process_file(self, fp):

        track_id = self._scrub_filepath_for_id(fp)
        artist = self._get_artist(track_id)
        track = self._get_track(track_id)

        h5 = self._read_h5_file(fp)
        # Do stuff!
        h5.close()

        return {'artist':artist, 'track':track, 'id':track_id}

    def _scrub_filepath_for_id(self, fp):
        length = len(fp.split('/'))
        file_name = fp.split('/')[length - 1] 
        return file_name.split('.h5')[0] # Assumes filename is track id


    def _get_artist(self, id):
        return self.id_to_artist_track[id]['artist']

    def _get_track(self, id):
        return self.id_to_artist_track[id]['track']

    def _read_h5_file(self, fp):
        """
        Wrapper to read an h5 file
        """
        h5 = h5py.File(fp, 'r')
        return h5

    def _read_unique_artists(self, fp):
        """
        Extracts id-artists mappings from unique_artists file

        returns two dictionaries, one with id as key, and the
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

        returns two dictionaries, one with id as key, and the
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
                id_to_artist_track[id_1] = {'artist':artist, 'track':track}

        return track_to_id, artist_to_ids, id_to_artist_track


