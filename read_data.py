import h5py
import os


def read_file(fp):
    """
    Wrapper to read an h5 file
    """
    h5 = h5py.File(fp, 'r')
    return h5


def get_unique_artists(fp):
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


def get_unique_tracks(fp):
    """
    Extracts id-artists mappings from unique_tracks file

    returns two dictionaries, one with id as key, and the
        other with track as key.
    """

    track_to_id = {}
    id_to_track = {}
    with open(fp, 'r') as f:
        for row in f:
            id_1, id_2, artist, track = row.split("<SEP>")
            track_to_id[track] = id_1
            id_to_track[id_1] = (track, artist)

    return track_to_id, id_to_track


def main():

    unique_dir = "./MillionSongSubset/AdditionalFiles/"

    unique_artist_fp = unique_dir + "subset_unique_artists.txt"
    unique_tracks_fp = unique_dir + "subset_unique_tracks.txt"

    track_to_id, id_to_track = get_unique_tracks(unique_tracks_fp)
    artist_to_id, id_to_artist = get_unique_artists(unique_artist_fp)

    data_dir = "./data/"
    all_files = os.listdir(data_dir)

    artist_count = {}

    for f in all_files:
        track_id = f.split(".h5")[0]
        track, artist = id_to_track[track_id]
        artist_count[artist] = artist_count.get(artist, 0) + 1

    sorted_list = [(artist, count) for artist, count in artist_count.items()]
    sorted_list.sort(key=lambda tup: tup[1])

    for item in sorted_list:
        print("%s: %s" % (item[0], item[1]))


if __name__ == '__main__':
    main()
