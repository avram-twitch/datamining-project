'''
    @author - Angel Dhungana

'''
import numpy as np
from matplotlib import pyplot as plt
import csv
import src.GonzalezClustering
import src.KPlusPlus
import src.LlyodsClustering
import matplotlib.patches as mpatches


def plot_graphs(colors, pca_main_data, closest_centers, centroids, text_list,
                type_text, plot_name):
    '''
        Plot Graphs
            colors : list of colors
            pca_main_data : Reduced Dimension Data, in this case 2D
            closest_centers : closest_centers indexes
            centroids : list of centers
            text_list : list of texts for labels
            type_text : title text
            plot_name : plot name text
    '''
    i = 0
    for clst_ce in closest_centers:
        plt.scatter(
            pca_main_data[i][0].real,
            pca_main_data[i][1].real,
            color=colors[clst_ce])
        i += 1
    hndls = []
    for j in range(len(centroids)):
        patch = mpatches.Patch(
            hatch='o', color=colors[j], label=text_list[j][:2])
        hndls.append(patch)
    plt.xlabel("Dim1 (PCA 1)")
    plt.ylabel("Dim2 (PCA 2)")
    plt.title(type_text)
    plt.legend(handles=hndls)
    plt.savefig(plot_name)


def main():
    '''
        Run the algorithm and plot
    '''
    loudness_file_path = 'data/matrix_files/loudness_matrix.csv'
    pitches_file_path = 'data/matrix_files/pitches_matrix.csv'
    metadata_file_path = 'data/matrix_files/metadata.tsv'

    loudness = np.genfromtxt(loudness_file_path, delimiter=',')
    pitches = np.genfromtxt(pitches_file_path, delimiter=',')
    pca_loud = PCA_(loudness, n_components=2)
    pca_pitch = PCA_(pitches, n_components=2)
    #sum_squared_error(loudness)
    #sum_squared_error(pitches)

    llyods_with_kpp(loudness, "Llyods with K++ - Loudness - ", 4,
                    metadata_file_path, pca_loud)

    llyods_with_kpp(pitches, "Llyods with K++ - Pitches - ", 3,
                    metadata_file_path, pca_pitch)

    llyods_with_gonzalez(loudness, "Llyods with Gonzalez - Loudness - ", 4,
                         metadata_file_path, pca_loud)

    llyods_with_gonzalez(pitches, "Llyods with Gonzalez - Pitches - ", 3,
                         metadata_file_path, pca_pitch)


def llyods_with_kpp(dataset, type_text, k, metadata_file_path, pca_d):
    '''
        Runs LLyods Algorithm with initial centroids computed with K++
        Plots Graphs based on Artist and Dates Slices
            dataset - dataset to cluster on
            type_text - string, which dataset is this, loudness or pitches
            k - cluster size
            metadata_file_path - file path to metadata tsv file
    '''
    gc = KPlusPlus.KPlusPlus(k)
    gc.fit(dataset)
    ll = LlyodsClustering.LlyodsClustering(len(gc._centers()), gc._centers())
    ll.fit(dataset)
    print("Llyod's Finished")
    centroids = ll._centroids()
    closest_centers = ll.assign_centers_to_data(dataset, centroids)
    artists, years = get_years_artist_for_each_cluster(closest_centers,
                                                       len(centroids), 10,
                                                       metadata_file_path)
    colors_artist = ["blue", "red", "green", "yellow", "black"]
    colors_years = ["red", "orange", "beige", "turquoise", "pink"]
    plot_graphs(colors_artist, pca_d, closest_centers, centroids, artists,
                type_text + "Artist Name", type_text + "Artist Name" + ".pdf")
    plot_graphs(colors_years, pca_d, closest_centers, centroids, years,
                type_text + "Years", type_text + "Years" + ".pdf")


def llyods_with_gonzalez(dataset, type_text, k, metadata_file_path, pca_d):
    '''
        Runs LLyods Algorithm with initial centroids computed with Gongalez Algorithm
        Plots Graphs based on Artist and Dates Slices
            dataset - dataset to cluster on
            type_text - string, which dataset is this, loudness or pitches
            k - cluster size
            metadata_file_path - file path to metadata tsv file
    '''
    gc = GonzalezClustering.GonzalezClustering(k)
    gc.fit(dataset)
    ll = LlyodsClustering.LlyodsClustering(len(gc._centers()), gc._centers())
    ll.fit(dataset)
    print("Llyod's Finished")
    centroids = ll._centroids()
    closest_centers = ll.assign_centers_to_data(dataset, centroids)
    artists, years = get_years_artist_for_each_cluster(closest_centers,
                                                       len(centroids), 10,
                                                       metadata_file_path)
    colors_artist = ["blue", "red", "green", "yellow", "black"]
    colors_years = ["red", "orange", "beige", "turquoise", "pink"]
    plot_graphs(colors_artist, pca_d, closest_centers, centroids, artists,
                type_text + "Artist Name", type_text + "Artist Name" + ".pdf")
    plot_graphs(colors_years, pca_d, closest_centers, centroids, years,
                type_text + "Years", type_text + "Years" + ".pdf")


def get_years_artist_for_each_cluster(closest_centers, centers_size, max_num,
                                      metadata_file_path):
    '''
        Read Metadata and get the artist name and year the song was released, add it to dictionary
        Returns the most common years or artist names for each cluster
            closest_centers - list containing closest centers for each songs
            centers_size - how many centers are there
            max_num - how many most common item to return for each cluster
            metadata_file_path - file path to metadata tsv file
    '''
    centers_dictionary = {}
    for i in range(centers_size):
        centers_dictionary[i] = []
    center_counter = 0
    dataCount = 0
    with open(metadata_file_path) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for line in tsvreader:
            centers_dictionary[closest_centers[center_counter]].append(
                [line[0], line[3]])
            center_counter += 1
            if int(line[3]) == 0:
                dataCount += 1
    return find_max_years_artist_in_clusters(centers_dictionary, max_num)


def find_max_years_artist_in_clusters(centers_dict, max_num):
    '''
        Find the most common years and artist names in each cluster
            centers_dict - Dictionary containing centers with artist name and year
            max_num - Maximum number of most common to generate
    '''
    artists_max = []
    year_max = []
    for center_keys in centers_dict:
        value_array = centers_dict[center_keys]
        temp_year = {}
        temp_artist = {}
        for artist_year in value_array:
            helper_dict_adder(temp_year, artist_year[1])
            helper_dict_adder(temp_artist, artist_year[0])
        year_max.append(sorted(temp_year, key=temp_year.get)[:max_num])
        artists_max.append(sorted(temp_artist, key=temp_artist.get)[:max_num])
    return artists_max, year_max


def helper_dict_adder(temp_dict, value):
    '''
        Simple helper function that tracks the counts of values
            temp_dict - dictionary to look for value and put counter
            value - value to look for in dictionary
    '''
    if value in temp_dict: temp_dict[value] += 1
    else: temp_dict[value] = 1


def PCA_(X, n_components):
    '''
        Projects high dimensional data into a low dimensional sub-space
            - Only For Visualization
        Most likely n_components will be 2 for better visualization.
            - normalize to zero mean
            - eigenvectors of covariance matrix
        The 2d components will be:
            1st Principal component (PC1)
                – Direction along which there is greatest variation
            2nd Principal component (PC2)
                - Direction with maximum variation left in data, orthogonal to PC1 
    '''
    # Empirical Mean
    mu = X.mean(axis=0)
    # Deviation from mean
    X = X - mu
    # Covariance
    sigma = X.T @ X
    # Eigenvalues and eigen vectors
    eigvals, eigvecs = np.linalg.eig(sigma)
    # Rearrange the values
    order = np.argsort(eigvals)[::-1]
    # Select subset, in this case 2 dimension
    components = eigvecs[:, order[:n_components]]
    # Project Z-scores on new basis
    Z = X @ components
    return Z


def sum_squared_error(B):
    '''
        Getting the inertia, sum of squared errors for each k
        Plotting a line chart of the SSE for each value of k. 
        If the line chart looks like an arm, 
            then the "elbow" on the arm is the value of k that is the best.
    '''
    max_k = 10
    k = 1
    distortions = []
    K = [kk + 1 for kk in range(max_k)]
    while k <= max_k:
        gc = KPlusPlus.KPlusPlus(k)
        gc.fit(B)
        distortions.append(gc.calculate_interia(B))
        print("Finished " + str(k))
        k += 1
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k')
    plt.show()


if __name__ == "__main__":
    main()