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

name = 'MUTAG'
root = './tmp/{}'.format(name)

dataset = TUDataset(root=name, name=name)
#dataset = dataset.shuffle()
print_info('Starting Tests with dataset: {}, containing {} Graphs'.format(name, len(dataset)))

convert.dataset_to_datafile(dataset, name)

# create the run arguments for gSpan-python
cwd = os.getcwd()
f_name = '{}.data.txt'.format(name)
f_path = path.join(cwd, 'graphs', f_name)
args_str = '--min_support 100 -u 5 --directed TRUE --verbose False {ds}'.format(ds = f_path)
FLAGS, _ = parser.parse_known_args(args=args_str.split())

# mine with gSpan
print_info("Starting mining with gSpan-Algorithm")
gs = main(FLAGS)
gs_report = gs._report_df
freq_support = gs_report['support'].to_numpy()

y = dataset.data.y.tolist()
# the graph Respresentations in NetworkX
nx_freq = convert.dfscode_to_networkX(gs._frequent_subgraphs)
nx_dataset = convert.dataset_to_networkX(dataset)

print_info("Finished mining. Found {} freq. subgraphs".format(len(nx_freq)))

# Pattern language get random pattern
# kernel = pattern_chooser.random_pattern(nx_freq, 50)
# pattern language graphlet-select, graphs with nodes in a certain range
kernel = pattern_chooser.graphlets(nx_freq, 3)

# get sample vectors
print_info('Creating the binary vectors representing a graph')
X = []
for i in range(len(nx_dataset)):
    nx_graph = nx_dataset[i]

    binary_vec = []
    for kernel_graph in kernel:
        if iso_test.subgraph_isomorphism(nx_graph, kernel_graph):
            binary_vec.append(1)
        else: binary_vec.append(0)
    
    X.append(binary_vec)

# perform SVM accuracy testing
print_info('Start training of our SVM')
accuracies, predictions = perform_SVM(X, y)
print_info(accuracies)










# Maybe needed later

# # test our SVM with our testing data
# nx_testing = convert.dataset_to_networkX(testing_set)
# testing_class_labels = class_labels[trainig_size:]
# binary_vec = []
# sum_right_predictions = 0
# for i in range(len(nx_testing)):
#     nx_graph = nx_testing[i]
#     g_label = testing_class_labels[i]

#     binary_vec = []
#     for kernel_graph in kernel:
#         binary_vec.append(1) if iso_test.subgraph_isomorphism(nx_graph, kernel_graph) else binary_vec.append(0)
    
#     binary_vec = np.reshape(binary_vec, (1, -1))

#     prediction = lin_clf.predict(binary_vec)[0]
#     print_info('Prediction: {} Real label: {}'.format(prediction, g_label))
#     if g_label == prediction:
#         sum_right_predictions += 1

# print_info('Kernel Size: {}; Tested with {} graphs; Correct predictions made: {}'.format(len(kernel), len(nx_testing), sum_right_predictions))
