# B.Sc. Thesis

Repository for the coding part of my Bachelor Thesis written in Summer Term 2020(if Covid-19 lets me).

## Subject

The Thesis focuses pattern approaches to classify graphs in Datasets. To do this we mine for frequent patterns inside Datasets of Graphs using gSpan.
After the discovery of frequent patterns with a certain support we select features that match certain criteria. These criteria are defined and described in pattern languages.

The goal is to compare these pattern languages using criteria listed below.

## Explanation

### Our Test-Suite

* works on Datasets using the ones provided by the TU Dortmund, using PyTorch-Geometric
* mines for freq. sub-graphs using this gSpan implementation
* selects pattern matching certain criteria
* trains and evaluates a machine learning model with the resulting kernels using scikit-learn's machine learning- and evaluation methods

### Pattern languages

* Random: select a certain number of random sub-graphs from the mining result
* Graphlet-like: select sub-graphs with nodes in a certain range e.g. 3 to 5 nodes

### Compairing criteria

### Graph formats used
