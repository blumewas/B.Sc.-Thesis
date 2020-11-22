import os
from os import path
# implementations of TU Dortmund datasets
from torch_geometric.datasets import TUDataset
import torch
# our helper classes
import convert
import iso_test
from helper import plot, print_info
import pattern_chooser
# gSpan Implementation 
from gspan_mining.config import parser
from gspan_mining.main import main
import pandas as pd
# Support Vector Machine
from svm import perform_SVM
from sklearn.exceptions import ConvergenceWarning

import warnings


warnings.filterwarnings('once', 'ConvergenceWarning: Solver terminated early.*')
warnings.filterwarnings('once', 'Solver terminated early.*')
warnings.filterwarnings('once', category = ConvergenceWarning)

def get_sample_vectors(kernel_idxs, ds_size, isomorph_graphs, ds_name):
    # get sample vectors
    print_info('Creating the binary vectors representing the Graphs in the Dataset', ds_name)
    X = []
    for gid in range(ds_size):
        bin_vec = []
        for idx in kernel_idxs:
            if gid in isomorph_graphs[idx]:
                bin_vec.append(1)
            else: bin_vec.append(0)

        X.append(bin_vec)

    return X

def train_SVM(X, y, ds_name):
    # perform SVM accuracy testing
    print_info('Start training of our SVM', ds_name)
    accuracies, predictions = perform_SVM(X, y)
    print_info(accuracies, ds_name)

def test_graphlet_select(ds_name, num_vertices, ds_graph_classes, isomorph_graphs):
    # pattern language graphlet-select, graphs with nodes in a certain range
    kernel_idxs = pattern_chooser.graphlets(ds_name, num_vertices, 5, 3)
    X = get_sample_vectors(kernel_idxs, len(ds_graph_classes), isomorph_graphs, ds_name)
    train_SVM(X, ds_graph_classes, ds_name)
    print_info('\n-----[End Test]-----\n', ds_name)


def test_random(ds_name, pattern_count, ds_graph_classes, isomorph_graphs):
    for f in [0.2, 0.3, 0.5]:
        print_info('Testing Random Selection with {}%'.format(f*100), ds_name)
        # Pattern language get random pattern
        kernel_idxs = pattern_chooser.random_pattern(ds_name, pattern_count, int(f * pattern_count))
        X = get_sample_vectors(kernel_idxs, len(ds_graph_classes), isomorph_graphs, ds_name)
        train_SVM(X, ds_graph_classes, ds_name)
        print_info('\n-----[End Test]-----\n', ds_name)

def test_cork(ds_name, freq_pattern, isomorph_graphs, ds_graph_classes):    
    cork = pattern_chooser.CORK(ds_name, freq_pattern, isomorph_graphs, ds_graph_classes)
    kernel_idxs = cork.get_pattern()
    # print_info(kernel_idxs, ds_name)
    X = get_sample_vectors([x+1 for x in kernel_idxs], len(ds_graph_classes), isomorph_graphs, ds_name)
    train_SVM(X, ds_graph_classes, ds_name)
    print_info('\n-----[End Test]-----\n', ds_name)

def test(ds_name, minSup, params=''):
    root = './tmp/{}'.format(ds_name)

    print_info('\n-----[BEGIN]-----\n', ds_name)
    dataset = TUDataset(root=ds_name, name=ds_name)
    print_info('Starting Tests with dataset: {}, containing {} Graphs'.format(ds_name, len(dataset)), ds_name)

    convert.dataset_to_datafile(dataset, ds_name)

    # create the run arguments for gSpan-python
    cwd = os.getcwd()
    f_name = '{}.data.txt'.format(ds_name)
    f_path = path.join(cwd, 'graphs', f_name)
    args_str = '--min_support {min} --directed TRUE {params} --verbose FALSE {ds}'.format(ds = f_path, min=int(len(dataset) * minSup), params=params)
    FLAGS, _ = parser.parse_known_args(args=args_str.split())
    print(FLAGS)
    # mine with gSpan
    print_info("Starting mining with gSpan-Algorithm and minSup sigma = {}%".format(minSup * 100), ds_name)
    gs = main(FLAGS)
    gs_report = gs._report_df
    # get info needed for testing
    freq_support = gs_report['support'].to_numpy()
    isomorph_graphs = gs_report['isomorph_graphs']
    num_vertices = gs_report['num_vert'].to_numpy()

    pattern_count = len(gs_report)
    y = dataset.data.y.tolist() # graph classes

    print("\n")

    print_info("Finished mining. Found {} freq. subgraphs\n".format(pattern_count), ds_name)
    # perform test
    # test_random(ds_name, pattern_count, y, isomorph_graphs)
    # test_graphlet_select(ds_name, num_vertices, y, isomorph_graphs)
    test_cork(ds_name, gs._frequent_subgraphs, isomorph_graphs, y)
    
    print_info('\n-----[END]-----\n', ds_name)

datasets = ['MUTAG', 'PTC_FM', 'NCI1', 'DD', 'PROTEINS']
extra_params = {
    'MUTAG': '-u 8 -mm 10000',
    'PTC_FM': '',
    'NCI1': '-mm 10000',
    'DD': '',
    'PROTEINS': '' 
}
min_supps = [0.1, 0.3, 0.5]
for ds_name in datasets:
    for min_sup in min_supps:
        params = extra_params[ds_name]
        test(ds_name, min_sup, params)
