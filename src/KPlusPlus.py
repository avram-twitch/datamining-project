'''
    @author - Angel Dhungana
    K++ Class
'''
import random


class KPlusPlus:
    def __init__(self, ncenters):
        '''
            Set up K++ Clustering
                n_centers - Number of Centers
                indexes - Indexing each x E X
                N - Size of dataset
                centers - centers found
                inertia - Sum Squared Error Cost
        '''
        self.n_centers = ncenters
        self.indexes = None
        self.N = None
        self.centers = []
        self._inertia = 0

    def fit(self, X):
        '''
            Runs k++
        '''
        self.N = len(X)
        C = [random.randint(0, self.N - 1)]
        min_list = []
        while len(C) != self.n_centers:
            max_distance_index = self.calculate_distance(X, C, min_list)
            C.append(max_distance_index)
        self.centers = C

    def _centers(self):
        '''
            Return the found centers
        '''
        return self.centers

    def calculate_distance(self, X, C, min_list):
        d = []
        sum_squared_distance = 0
        for i in range(0, len(X)):
            data = X[i]
            closest_center_distance = self.find_closest_center(C, X, data)
            d.append([i, closest_center_distance**2])
            sum_squared_distance += (closest_center_distance**2)
        r = random.random()
        sum_squared_distance *= r
        i = 0
        for x in d:
            sum_squared_distance -= x[1]
            if sum_squared_distance < 0:
                break
        return x[0]

    def find_closest_center(self, C, X, data):
        '''
            Find closest center for each x E X while running K++
        '''
        clost_dist = None
        for i in range(0, len(C)):
            center = X[C[i]]
            distance = self.get_distance(center, data)
            if clost_dist == None or distance < clost_dist:
                clost_dist = distance
        return clost_dist

    def assign_centers_to_data(self, X, centers):
        closest_centers = []
        for x in X:
            c_center = self.find_closest_center_assign(centers, X, x)
            closest_centers.append(c_center)
        return closest_centers

    def find_closest_center_assign(self, C, X, data):
        clost_dist = None
        indx = -1
        for i in range(0, len(C)):
            center = X[C[i]]
            distance = self.get_distance(center, data)
            if clost_dist == None or distance < clost_dist:
                clost_dist = distance
                indx = i
        return indx

    def calculate_interia(self, X):
        '''
            Calculating Sum Squared Error
        '''
        assign_centers = self.assign_centers_to_data(X, self.centers)
        dist = 0
        i = 0
        for x in assign_centers:
            center = X[self.centers[x]]
            dist += (self.get_distance(X[i], center)**2)
            i += 1
        self._inertia = dist / len(X)
        return self._inertia

    def get_distance(self, S1, S2):
        dist = 0
        for i in range(len(S1)):
            dist += ((S2[i] - S1[i])**2)
        return dist