'''
    @author - Angel Dhungana
    LLoyds Class
'''
import numpy as np
import copy


class LloydsClustering:
    '''
            Set up Lloyds Clustering
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

    def fit(self, X, years):
        '''
            Runs the LLyod's algorithm
        '''
        prev_cen = [[] for i in range(self.n_centers)]
        iterations = 0
        while not (self._converged(prev_cen, iterations)):
            iterations += 1
            clusters, year_clusters = self.calculate_dist(X, years)
            index = 0
            for cluster in clusters:
                prev_cen[index] = copy.deepcopy(self.centroids[index])
                # self.centroids[index] = np.mean(cluster, axis=0).tolist()
                oldest = self._get_oldest(clusters[index],
                                          year_clusters[index])
                self.centroids[index] = np.mean(oldest, axis=0).tolist()
                index += 1

    def _centroids(self):
        return self.centroids

    def _converged(self, centroids, iterations):
        if iterations > self.MAX_ITERATIONS:
            return True

        for i in range(len(centroids)):
            if type(centroids[i]) != list:
                first = centroids[i].tolist()
            else:
                first = centroids[i]

            if type(self.centroids[i]) != list:
                second = self.centroids[i].tolist()
            else:
                second = self.centroids[i]

            if first != second:
                return False

        return True

    def _get_oldest(self, cluster, year_cluster):
        # Gets all oldest data points

        non_zero_years = [x for x in year_cluster if x != 0]
        if len(non_zero_years) > 0:
            min_year = min(non_zero_years)
        else:
            min_year = 0
        oldest = [cluster[x] for x in range(len(cluster))
                  if year_cluster[x] == min_year]
        return oldest

    def calculate_dist(self, data, years):
        clusters = [[] for i in range(self.n_centers)]
        year_clusters = [[] for i in range(self.n_centers)]
        year_index = 0
        for dat in data:
            mu_index = self.norm_min(dat)
            clusters[mu_index].append(dat)
            year_clusters[mu_index].append(years[year_index])

            year_index += 1

        for cluster in clusters:
            if not cluster:
                cluster.append(data[np.random.randint(
                    0, len(data), size=1)].flatten().tolist())

        return clusters, year_clusters

    def norm_min(self, dat):

        all_values = []
        for i in enumerate(self.centroids):
            first = i[0]
            second = np.linalg.norm(dat - self.centroids[i[0]])
            curr = (first, second)
            all_values.append(curr)

        return min(all_values, key=lambda t: t[1])[0]

#        return min([(i[0],
#                     np.linalg.norm(dat-self.centroids[i[0]]))
#                     for i in enumerate(self.centroids)],
#                                        key=lambda t: t[1])[0]

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
            if clost_dist is None or distance < clost_dist:
                clost_dist = distance
                indx = i
        return indx

    def get_distance(self, S1, S2):
        dist = 0
        for i in range(len(S1)):
            dist += ((S2[i] - S1[i])**2)
        return dist
