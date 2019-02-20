import hashlib


class Minhash:
    """
    Minhash calculator.

    Takes a list of observations (already in the form of sets) and
    calculates k minhashes for each observation.

    """

    def __init__(self, k, m):
        """
        :param k: Number of hash functions to use
        :param m: Range of the output of the hash function (0 to m - 1)
        """
        self.k = k
        self.m = m
        self.hashes = []
        self.salts = []
        self._initialize_salts()

    def run(self, data):
        """
        Calculates k minhashes for each observation in provided data.

        :param data: a list of sets representing the data
        :return: a list of lists. Each list is the minhashes of
            the corresponding observation. (in the same order as provided)
        """
        self.hashes = []
        for row in data:
            min_hashes = self._hash_row(row)
            self.hashes.append(min_hashes)

        return self.hashes

    def get_similarity(self, first, second):
        """
        Calculates an estimate for Jaccard similarity between two observations

        :param first: Index of first observation to compare
        :param second: Index of second observation to compare
        :return: Float value of the estimated Jaccard similarity.
        """

        count = 0
        for (a, b) in zip(self.hashes[first], self.hashes[second]):
            if a == b:
                count += 1

        return count / float(self.k)

    def _initialize_salts(self):
        """
        Initializes salt values.
        Simply a list from 0 to k-1.
        """
        # TODO: Better way to represent salts?
        self.salts = [salt for salt in range(self.k)]

    def _hash_row(self, row):
        """
        Generates list of minhashes from single observation

        :param row: list/set representing one observation
        :return: a list of the minhashes for the provided row
        """
        out_hashes = []
        for salt in self.salts:
            min_hash = self._get_min_hash(row, salt)
            out_hashes.append(min_hash)

        return out_hashes

    def _get_min_hash(self, row, salt):
        """
        Calculates k hashes and returns the minimum value

        :param row: list/set representing one observation
        :param salt: integer that 'salts' hash function
        :return: Minimum hash value from hash functions
        """
        hashes = [self._hash(x, salt) for x in row]
        return min(hashes)

    def _hash(self, value, salt):
        """
        Calculates a single hash value.

        :param value: Value to be hashed
        :param salt: Integer that 'salts' hash function
        :return: hash value in decimal format, in range 0 to m-1
        """
        raw = hashlib.md5((str(value) + str(salt)).encode())
        return int(raw.hexdigest(), 16) % self.m
