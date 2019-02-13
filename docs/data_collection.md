
# How you obtained your data?

The Million Song Dataset is freely available online ([link](https://labrosa.ee.columbia.edu/millionsong/musixmatch#getting))

# How large is your data?

The data in total is 280 GB, although a subset is provided that is only 1.8 GB.
However, we plan on only using a few variables,
so, we anticipate that the final dataset that we use will be much smaller.

For testing purposes, we are using the subset, 
but for the final analysis we plan on using the entire dataset.

# Abstract Data Type

We plan on pursuing two approaches to mine this data:

* Minhashing and LSH
* Clustering

For each of these tasks, we will need to use different data structures.

## Minhashing

For minhashing, we only need a set of their unique "variables",
rather than their counts or magnitudes.
Because of this, we plan on representing each song 
as a set of each variable it contains,
and the entire dataset will be a list of these sets.

Our data is a mix of different data types, 
including arrays representing song attributes at different points of time,
and simple bag-of-word word counts.

For the arrays, we plan on preprocessing them by rounding each element to
some cutoff, and then creating k-grams of the arrays.
Each k-gram will be a unique variable in a set.

Unfortunately, due to copyright issues, the Million Song Dataset 
does not have the raw lyrics to each song.
But they do have word counts,
so for the bag of words, we will just use the words themselves as the variable.

Each song will therefore be a set of k-grams for different variables,
and words that the song contains.

## Clustering

We will be performing clustering in a hope of finding the similarities among music. We want to see if there exists a relationship between artists, genres and the year. 

We will be using various audio features including tempo, loudness, key etc. to cluster the songs into labels defined using Hierarchical Clustering. We will be able to see cross-genre similarities and influences of one song/artists into other. 

Our data which includes the songs and their audio features will be stored as a matrix. Every track/genre/year/ would be a row, and their audio features will be represented as columns. 

# Did you process the original data?

The original data is in hdf5 file format, 
with some metadata contained in csv files and SQL databases.
We greatly cut down and simplified the data, 
and for now are storing the data as pickled lists of dictionaries 
(with each dictionary representing a song).
However, moving forward we anticipate using other formats to represent our final data.
Our data is sparse, so we want to be careful that 
the format we use avoids taking up too much space, 
but is still easy to use across our various analyses

# How would you simulate similar data?
We hope to find a structure underlying the data. Not only that, we will be identifying a distribution function of the data from the underlying structure. 

Then, we will be using the "random generation" model to generate a sample from the assumed distribution.This acquired model will be utilized to predict future data patterns and to validate how well our technique actually worked. 

For tracks dataset, we might model the data over ranges of audio features like loudness, key etc. And for the lyrics dataset, we might model the data over most common words. 
