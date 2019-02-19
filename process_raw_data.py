from src.Data import Data
import os

if __name__ == '__main__':
    data = Data()

    unique_dir = "./MillionSongSubset/AdditionalFiles/"
    unique_artist_fp = unique_dir + "subset_unique_artists.txt"
    unique_tracks_fp = unique_dir + "subset_unique_tracks.txt"

    data_dir = "./raw_data/"
    all_files = os.listdir(data_dir)
    for i in range(len(all_files)):
        all_files[i] = data_dir + all_files[i]

    out_data = data.create_data(all_files, unique_artist_fp, unique_tracks_fp)
