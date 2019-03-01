'''
    @author - Angel Dhungana
    Implementation of Hierarchical Clustering
    Linkage 
        1 - Single-Link
        2 - Complete-Link
        3 - Mean-Link
    
    Also, has the functionality to plot the dendograms, but make sure n_clusters is 1

    - Users need to make object providing max number of clusters to make and linkage method
    - Users Method
        - fit(), makes cluster
        - label_(), returns clusters as an array
        - plot_dendogram(), plots dendogram of the cluster, for this to work, nclusters should be 1

    Example:
        hierarchichalCluster = HierarchicalClustering(1 , "single")
        hierarchichalCluster.fit(dataSet,len(dataSet))
        print(hierarchichalCluster.labels_())
                    or 
        hierarchichalCluster.plot_dendogram(dataSetLabels)

'''
import sys
from scipy.cluster.hierarchy import dendrogram
from matplotlib import pyplot as plt


class HierarchicalClustering:
    def __init__(self, ncluster, linkage_name):
        '''
            ncluster - Max number of cluster to build
            linkageName - Which linkage method to use
        '''
        self.dataset = None
        self.n_clusters = ncluster
        self.linkage = self.set_linkage_by_name(linkage_name)
        self.final_cluster = None
        self.indexes = None
        self.N = None
        self.linkage_matrix = []
        self.linkage_counter = []
        self.distance_matrix = None

    def set_linkage_by_name(self, linkage_name):
        '''
            Sets the Linkage, Changes the linkage name to Integer Value
                single - 0
                complete - 1
                mean - 2
        '''
        linkage_num = {'single': 0, 'complete': 1, 'mean': 2}
        if linkage_name in linkage_num: return linkage_num[linkage_name]
        else:
            print("Need a correct linkage method name")
            sys.exit(0)

    def fit(self, data_set, data_size):
        '''
            Set the datasets and its size and runs cluster
            You call this method to build the clusters
             
                data_set - Set of data to build cluster of 
                data_size - Size of Data
        '''
        self.dataset = data_set
        self.N = data_size
        self.indexes = [[x] for x in range(data_size)]
        self.cluster()

    def labels_(self):
        '''
            Returns Final Clusters
        '''
        return self.final_cluster

    def cluster(self):
        '''
            Calculates distance, and until n_clusters are made, we merge two closest data
        '''
        self.distance_matrix = self.find_distances()
        sets = set(tuple(row) for row in self.indexes)
        while len(sets) > self.n_clusters:
            closests = self.find_closests()
            closestsKey = closests[0].split(",")
            first = self.indexes[int(closestsKey[0])]
            second = self.indexes[int(closestsKey[1])]
            self.update_linkage_matrix(first, second, closests[1])
            new_cluster = first + second
            self.set_all_indexes(new_cluster, self.indexes)
            sets = set(tuple(row) for row in self.indexes)
        self.final_cluster = sets

    def find_closests(self):
        '''
            Find the closests Points, and update Distance Matrix
        '''
        key = min(self.distance_matrix, key=self.distance_matrix.get)
        dist = self.distance_matrix[key]
        self.update_distance_matrix(key)
        return key, dist

    def update_distance_matrix(self, key):
        '''
            Update Distance Matrix as needed
                key - contains row and column that needs to be updated
        '''
        first_ind = int(key.split(",")[0])
        second_ind = int(key.split(",")[1])
        if second_ind < first_ind:
            first_ind, second_ind = second_ind, first_ind
        if self.linkage == 0:
            self.single_linkage(first_ind, second_ind)
        elif self.linkage == 1:
            self.complete_linkage(first_ind, second_ind)
        else:
            self.mean_linkage(first_ind, second_ind)
        self.distance_matrix[str(first_ind) + "," +
                             str(first_ind)] = float("inf")
        for i in range(0, self.N):
            index = str(second_ind) + "," + str(i)
            self.distance_matrix[index] = float("inf")
        for i in range(0, self.N):
            index = str(i) + "," + str(second_ind)
            self.distance_matrix[index] = float("inf")

    def single_linkage(self, first_ind, second_ind):
        '''
            Update cluster distance to the smallest distance
                firstInd - row 
        '''
        for i in range(0, self.N):
            index2 = str(second_ind) + "," + str(i)
            index1 = str(first_ind) + "," + str(i)
            if self.distance_matrix[index2] < self.distance_matrix[index1]:
                self.distance_matrix[index1] = self.distance_matrix[index2]

    def complete_linkage(self, first_ind, second_ind):
        '''
            Update cluster distance to the longest distance
        '''
        for i in range(0, self.N):
            index2 = str(second_ind) + "," + str(i)
            index1 = str(first_ind) + "," + str(i)
            if self.distance_matrix[index2] > self.distance_matrix[index1]:
                self.distance_matrix[index1] = self.distance_matrix[index2]

    def mean_linkage(self, first_ind, second_ind):
        '''
            Update cluster distance to the average of distance
        '''
        for i in range(0, self.N):
            index2 = str(second_ind) + "," + str(i)
            index1 = str(first_ind) + "," + str(i)
            self.distance_matrix[index1] = (self.distance_matrix[index2] +
                                            self.distance_matrix[index1]) / 2

    def set_all_indexes(self, newCluster, indexes):
        '''
            Just sets same clusters in each indexes values
        '''
        for x in newCluster:
            indexes[x] = newCluster

    def update_linkage_matrix(self, first_p, second_p, dist):
        '''
            Update and Building the Linkage matrix
            This Linkage matrix will be only used if we needed to plot

            This matrix will be later used to plot dendograms
                first_p - cluster number 1
                second_p - cluster number 2
        '''
        if len(first_p) == 1 and len(second_p) == 1:
            cluster = first_p + second_p
            self.linkage_counter.append(cluster)
            first_indx = self.indexes.index(first_p)
            second_indx = self.indexes.index(second_p)
            self.linkage_matrix.append(
                [float(first_indx),
                 float(second_indx), dist, 2.0])
        elif len(first_p) > 1 and len(second_p) > 1:
            cluster = first_p + second_p
            first_indx = self.linkage_counter.index(first_p)
            second_indx = self.linkage_counter.index(second_p)
            self.linkage_counter[first_indx] = [None]
            self.linkage_counter[second_indx] = [None]
            self.linkage_counter.append(cluster)
            self.linkage_matrix.append([
                float(self.N + first_indx),
                float(self.N + second_indx), dist,
                float(len(first_p) + len(second_p))
            ])
        elif len(first_p) == 1:
            cluster = first_p + second_p
            first_indx = self.indexes.index(first_p)
            second_indx = self.linkage_counter.index(second_p)
            self.linkage_counter[second_indx] = [None]
            self.linkage_counter.append(cluster)
            self.linkage_matrix.append([
                float(first_indx),
                float(self.N + second_indx), dist,
                float(len(first_p) + len(second_p))
            ])
        else:
            cluster = first_p + second_p
            second_indx = self.indexes.index(second_p)
            first_indx = self.linkage_counter.index(first_p)
            self.linkage_counter[first_indx] = [None]
            self.linkage_counter.append(cluster)
            self.linkage_matrix.append([
                float(self.N + first_indx),
                float(second_indx), dist,
                float(len(first_p) + len(second_p))
            ])

    def plot_dendogram(self, labels):
        '''
            Plots the dendogram based on the linkage matrix
        '''
        linkage_num = {
            0: 'Single Linkage',
            1: 'Complete Linkage',
            2: 'Mean Linkage'
        }
        plt.title("Dendrogram - Hierarchical Clustering - " +
                  linkage_num[self.linkage])
        dendrogram(
            self.linkage_matrix,
            show_leaf_counts=True,
            show_contracted=True,
            labels=labels)
        plt.show()

    def find_distances(self):
        '''
            Calculate Distance between each and every data points
        '''
        distance_matrix = {}
        for row in range(0, self.N):
            for col in range(0, self.N):
                indx = str(row) + "," + str(col)
                if row == col: distance_matrix[indx] = float("inf")
                else: distance_matrix[indx] = self.calculate_distance(row, col)
        return distance_matrix

    def calculate_distance(self, row, col):
        '''
            Calculate distance between two points. Not taking square root because it can be expensive
        '''
        S1 = self.dataset[row]
        S2 = self.dataset[col]
        distance = 0
        for i in range(len(S1)):
            distance += ((S2[i] - S1[i])**2)
        return distance