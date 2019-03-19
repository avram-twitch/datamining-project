'''
    @author - Angel Dhungana
    LLyods Class
'''
import random
import numpy as np


class LlyodsClustering:
    '''
            Set up Llyods Clustering
                n_centers - Number of Centers
                indexes - Indexing each x E X
                N - Size of dataset
                centroids - initial centers
                inertia - Sum Squared Error Cost
        '''

    def __init__(self, ncenters, _centroids):
        self.n_centers = ncenters
        self.indexes = None
        self.N = None
        self.centroids = _centroids
        self.MAX_ITERATIONS = 300

    def fit(self, X):
        '''
            Runs the LLyod's algorithm
        '''
        prev_cen = [[] for i in range(self.n_centers)]
        iterations = 0
        while not (self._converged(prev_cen, iterations)):
            iterations += 1
            clusters = [[] for i in range(self.n_centers)]
            clusters = self.calculate_dist(X, clusters)
            index = 0
            for cluster in clusters:
                prev_cen[index] = self.centroids[index]
                self.centroids[index] = np.mean(cluster, axis=0).tolist()
                index += 1

    def _centroids(self):
        return self.centroids

    def _converged(self, centroids, iterations):
        if iterations > self.MAX_ITERATIONS: return True
        return centroids == self.centroids

    def calculate_dist(self, data, clusters):
        for dat in data:
            mu_index = self.norm_min(dat)
            if mu_index in clusters: clusters[mu_index].append(dat)
            else: clusters[mu_index] = [dat]
        for cluster in clusters:
            if not cluster:
                cluster.append(data[np.random.randint(
                    0, len(data), size=1)].flatten().tolist())

        return clusters

    def norm_min(self, dat):
        return min([(i[0], np.linalg.norm(dat-self.centroids[i[0]])) \
                                for i in enumerate(self.centroids)], key=lambda t:t[1])[0]

    def assign_centers_to_data(self, X, centers):
        closest_centers = []
        for x in X:
            c_center = self.find_closest_center(centers, x)
            closest_centers.append(c_center)
        return closest_centers

    def find_closest_center(self, C, data):
        clost_dist = None
        indx = -1
        for i in range(0, len(C)):
            distance = self.get_distance(C[i], data)
            if clost_dist == None or distance < clost_dist:
                clost_dist = distance
                indx = i
        return indx

    def get_distance(self, S1, S2):
        dist = 0
        for i in range(len(S1)):
            dist += ((S2[i] - S1[i])**2)
        return dist