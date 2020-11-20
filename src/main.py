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

datasets = ['MUTAG', 'PTC_FM', 'NCI1', 'DD', 'PROTEINS']

for ds_name in datasets:
    root = './tmp/{}'.format(ds_name)

    print_info('\n-----[BEGIN]-----\n', ds_name)
    dataset = TUDataset(root=ds_name, name=ds_name)
    print_info('Starting Tests with dataset: {}, containing {} Graphs'.format(ds_name, len(dataset)), ds_name)

    convert.dataset_to_datafile(dataset, ds_name)

    # create the run arguments for gSpan-python
    cwd = os.getcwd()
    f_name = '{}.data.txt'.format(ds_name)
    f_path = path.join(cwd, 'graphs', f_name)
    args_str = '--min_support {min} --directed TRUE --verbose FALSE {ds}'.format(ds = f_path, min=int(len(dataset) * 0.5))
    FLAGS, _ = parser.parse_known_args(args=args_str.split())

    # mine with gSpan
    print_info("Starting mining with gSpan-Algorithm", ds_name)
    gs = main(FLAGS)
    gs_report = gs._report_df

    freq_support = gs_report['support'].to_numpy()
    isomorph_graphs = gs_report['isomorph_graphs']
    num_vertices = gs_report['num_vert']

    pattern_count = len(gs_report)
    y = dataset.data.y.tolist() # graph classes

    print("\n")

    print_info("Finished mining. Found {} freq. subgraphs".format(pattern_count), ds_name)

    # Pattern language get random pattern
    kernel_idxs = pattern_chooser.random_pattern(ds_name, pattern_count, int(0.3 * pattern_count))
    # pattern language graphlet-select, graphs with nodes in a certain range
    # kernel = pattern_chooser.graphlets(nx_freq, 3)

    # get sample vectors
    print_info('Creating the binary vectors representing the Graphs in the Dataset', ds_name)
    X = []
    for gid in range(1, len(dataset)+1):
        bin_vec = []
        for idx in kernel_idxs:
            if gid in isomorph_graphs[idx]:
                bin_vec.append(1)
            else: bin_vec.append(0)

        X.append(bin_vec)

    # perform SVM accuracy testing
    print_info('Start training of our SVM', ds_name)
    accuracies, predictions = perform_SVM(X, y)
    print_info(accuracies, ds_name)
    print_info('\n-----[END]-----\n', ds_name)
