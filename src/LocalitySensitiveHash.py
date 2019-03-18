import numpy as np
import math
import copy


class LSH:

    def __init__(self, tau, t, r, b, euclidean=False):
        self.tau = tau
        self.t = t
        self.r = r
        self.b = b
        self.euclidean = euclidean

    def hash_data(self, data):
        """
        Creates LSH hashes for provided data

        :param data: a numpy array with 2 dimensions
        :return: The hashed representation of the data
        """
        all_hashes = []
        d = data.shape[1]
        self._generate_jaccard_hashes(self.t, d)

        for obs in data:
            hashes = [0 for i in range(self.t)]
            for i in range(self.t):
                dot = np.dot(obs, self.vectors[i])
                if self.euclidean:
                    curr = math.ceil(dot + self.offsets[i])
                else:
                    if dot > 0:
                        curr = 1
                    else:
                        curr = -1

                hashes[i] = curr

            all_hashes.append(copy.deepcopy(hashes))

        self._all_hashes = all_hashes

        return all_hashes

    def query_all_similar(self, query):
        """
        Returns all observations that have estimated similarity
        with provided query above the threshold tau

        :param query: numpy vector to be compared with
        :return: list of indices of observations with similarity > tau
        """

        counter = 0
        out = []
        query_hash = [0 for i in range(self.t)]
        for i in range(self.t):
            dot = np.dot(query, self.vectors[i])
            if self.euclidean:
                curr = math.ceil(dot + self.offsets[i])
            else:
                if dot > 0:
                    curr = 1
                else:
                    curr = -1

            query_hash[i] = curr

        for hash_ in self._all_hashes:
            curr_sim = self._query(query_hash, hash_)
            if curr_sim > self.tau:
                print(counter)
                out.append(counter)
            counter += 1

        return out

    def query_similarity(self, q1, q2):
        """
        Gets the estimated similarity between two observations
        (observations that have already been run and have hashes
         stored in the LSH object)

        :param q1: index of observation 1
        :param q2: index of observation 2
        """
        h1 = self._all_hashes[q1]
        h2 = self._all_hashes[q2]
        return self._query(h1, h2)

    def _query(self, h1, h2):
        """
        Estimates similarity between two hashes

        :param h1: hashes of observation 1
        :param h2: hashes of observation 2
        :return: Float of estimated similarity
        """

        curr_r = 0
        curr_b = 0
        count = 0
        i = 0

        while i < len(h1):

            curr_r += 1
            hash_match = (h1[i] == h2[i])

            if not hash_match:
                curr_b += 1
                curr_r = 0
                i = curr_b * self.r
                continue

            if curr_r == self.r:
                count += 1
                curr_r = 0
                curr_b += 1
                i = curr_b * self.r
                continue

            i += 1

        return float(count / self.b)

    def convert_all_data_to_unit(self, data):
        """
        Converts each row in data to a unit vector

        :param data: Two-dimensional numpy array
        :return: Two-dimensional numpy array with each row a unit vector
        """
        return np.apply_along_axis(self._convert_to_unit, 1, data)

    def _generate_jaccard_hashes(self, t, d):
        """
        Generates unit vectors and offsets used for hashing data

        :param t: int number of hash functions needed
        :param d: int dimensions of data
        """
        self.vectors = self._generate_t_unit_vectors(t, d)
        self.offsets = self._generate_t_offsets(t)

#    def _project_vector(self, a):
#
#        d = a.shape[0]
#        u = self._generate_unit_vector(d)
#        return np.dot(a, u)

    def _generate_t_unit_vectors(self, t, d):
        """
        Generates t unit vectors to be used for hashing

        :param t: int number of hash functions needed
        :param d: int dimensions of data
        :return: numpy array of unit vectors (dim[t,d])
        """

        output = []
        for i in range(t):
            vector = self._generate_unit_vector(d)
            vector = self._convert_to_unit(vector)
            output.append(vector)

        return np.array(output)

    def _convert_to_unit(self, a):
        """
        Normalizes provided vector into a unit vector

        :param a: a numpy vector to be converted
        :return: a numpy unit vector
        """
        out = np.copy(a)
        norm = np.linalg.norm(out, ord=2)
        return out / norm

    def _generate_t_offsets(self, t):
        """
        Generates t offsets (used for euclidean distance hashing)

        :param t: int Number of hashes
        :return: numpy array of offsets
        """
        output = []
        for i in range(t):
            output.append(self._generate_uniform(high=self.tau))

        return np.array(output)

    def _generate_unit_vector(self, d):
        """
        Generates a gaussian distribution unit vector with d dimensions.
        Numbers are generated from random uniform numbers.

        :param d: int number of dimensions in the data
        :return: list unit vector following a gaussian distribution
        """
        # Generates a unit vector with d dimensions

        unif_nums = d if d % 2 == 0 else d + 1
        counter = 0
        output = []
        pairs = int(unif_nums / 2)

        for n in range(pairs):
            u1 = self._generate_uniform()
            u2 = self._generate_uniform()
            g1, g2 = self._get_gs(u1, u2)

            output.append(g1)
            counter += 1

            if counter != d:
                output.append(g2)
                counter += 1
            else:
                continue

        return output

    def _generate_uniform(self, high=1.0):
        """
        Generates a single uniformly random number

        :param high: float high cutoff for uniform number
        :return: float randomly uniform number
        """
        return np.random.uniform(low=0.0, high=high)

    def _get_gs(self, u1, u2):
        """
        Transforms two uniformly random numbers into
        two guassian distributed numbers

        :param u1/u2: Random uniform numbers
        :return: 2-tuple of gaussian distributed random numbers
        """
        sqrt = (-2 * math.log(u1)) ** 0.5
        cos = math.cos(2 * math.pi * u2)
        sin = math.sin(2 * math.pi * u2)
        g1 = sqrt * cos
        g2 = sqrt * sin
        return (g1, g2)
