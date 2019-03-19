'''
    @author - Angel Dhungana
    Gonzalez Clustering Class
'''
import random


class GonzalezClustering():
    def __init__(self, ncenters):
        '''
            Set up Gonzalez Clustering
                n_centers - Number of Centers
                indexes - Indexing each x E X
                N - Size of dataset
                centers - centers found
        '''
        self.n_centers = ncenters
        self.indexes = None
        self.N = None
        self.centers = []

    def fit(self, X):
        '''
            Call this method to run the Gonzalez Clustering
        '''
        self.N = len(X)
        C = [random.randint(0, self.N - 1)]
        min_list = []
        while len(C) != self.n_centers:
            sub_c = C[len(C) - 1]
            max_distance_index = self.calculate_distance(X, X[sub_c], min_list)
            C.append(max_distance_index)
        self.centers = C

    def _centers(self):
        return self.centers

    def calculate_distance(self, X, C, min_list):
        counter = 0
        for y in X:
            distance = self.get_distance(C, y)
            if len(min_list) < len(X):
                min_list.append(distance)
            else:
                if min_list[counter] > distance:
                    min_list[counter] = distance
            counter += 1
        return min_list.index(max(min_list))

    def get_distance(self, S1, S2):
        dist = 0
        for i in range(len(S1)):
            dist += ((S2[i] - S1[i])**2)
        return dist

    def assign_centers_to_data(self, X, centers):
        closest_centers = []
        for x in X:
            c_center = self.find_closest_center(centers, X, x)
            closest_centers.append(c_center)
        return closest_centers

    def find_closest_center(self, C, X, data):
        clost_dist = None
        indx = -1
        for i in range(0, len(C)):
            center = X[C[i]]
            distance = self.get_distance(center, data)
            if clost_dist == None or distance < clost_dist:
                clost_dist = distance
                indx = i
        return indx