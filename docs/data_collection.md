---
geometry: margin=2cm
header-includes:
    - \usepackage{setspace}
    - \singlespacing
---


**Data: Source, Size, and Processing**

The Million Song Dataset is freely available online ([link](https://labrosa.ee.columbia.edu/millionsong/musixmatch#getting)).
We will combine a couple of the datasets available, but we won't be engaged in much data cleaning or scraping.

The data in total is 280 GB, although a 1% subset is provided that is only 1.8 GB.
We plan on only using a few variables,
so we anticipate that the final dataset that we use will be much smaller.

For testing purposes, we are using the subset, 
but for the final analysis we plan on using the entire dataset.

The original data is in hdf5 file format, 
with some metadata contained in csv files and SQL databases.
We greatly cut down and simplified the data, 
and for now are storing the data as pickled lists of dictionaries 
(with each dictionary representing a song).
However, moving forward we anticipate using other formats to represent our final data.

**Abstract Data Type**

We plan on pursuing two approaches to mine this data:
Minhashing, and
Clustering.

For each of these tasks, we will need to use different data structures.
However, the variables themselves will be similar.

Our data is a mix of different data types, 
including arrays representing song attributes at different points of time,
and simple bag-of-word word counts.

For the arrays, we plan on preprocessing them by rounding each element to
some cutoff, and then creating k-grams of the arrays.
Each k-gram will be a unique variable in a set.

Since we only have word counts, we cannot construct k-grams from the lyrics.
So, we will just use the words themselves as the variable.

**Minhashing**

For minhashing, we only need a set of each song's unique "variables",
rather than their counts or magnitudes.
Because of this, we plan on representing each song 
as a set of each variable it contains,
and the entire dataset will be a list of these sets.

**Clustering**

We will also perform clustering on the dataset to see what groups emerge.
The end goal will be to see if the clusters that arise correspond with
artists, genres, or over time.

For clustering, we plan on using a matrix (more specifically, a numpy array),
with every row representing a track, and each column representing an audio feature.
The values themselves will be the _counts_ of each variable.

If time permits, we will attempt to use multiple forms of clustering
(e.g. heirarchical, assignment) and see if there are any differences.
Because we will be using variables that are not in like terms (such as tempo vs loudness),
we will have to run separate clusters for each variables.
This is not ideal, especially if different variables yield significantly different clusters.

**How would you simulate similar data?**

On a naive approach, simulating the data could be relatively simple.
We could simply observe the averages and variance of each variable mentioned above,
such as word counts or k-grams across variables like loudness, 
and generate a new track that follows the overall dataset distribution.
For example, if we know that a certain word occurs, on average, 5 times in a song,
with variance 2, the generated new track could have this word following
a normal distribution with a mean of 5 and variance of 2.

We would also have to take into account the length of the song,
which determines the length of the arrays for variables like loudness.
We hope to find a relationship between tracks in similar genres, years, and artists.

Another approach that may be more in line with our investigation is to
use the same process above, except we create subsets of the data by genre or
by year, and then generate tracks that follow the distributions of these subsets.
This could be a useful way of seeing if our end results are valid:
we could generate many tracks following this process, and see if they tend
to be clustered with the subsets from which they were generated.
