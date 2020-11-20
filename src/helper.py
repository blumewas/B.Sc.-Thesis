import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from termcolor import colored
import os
from os import path

cwd = os.getcwd()

def plot(graph):
    vlbs = {v: vlb for v, vlb in graph.nodes.data('label')}
    elbs = {(u, v): elb for (u, v, elb) in graph.edges.data('label')}

    fsize = (min(16, graph.number_of_nodes()), min(16, graph.number_of_nodes()))
    plt.figure(3, figsize=fsize)

    pos = nx.layout.spring_layout(graph)
    nx.draw_networkx(graph, pos, arrows=True, with_labels=True, labels=vlbs)
    nx.draw_networkx_edges(graph, pos, arrowstyle='->', arrowsize=10)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=elbs)
    plt.show()

def sort_freq_by_support(freq_pattern, support):
    freq_np = numpy.array(freq_pattern)
    support_np = numpy.array(support)
    sorted_inds = support_np.argsort()
    return freq_np[sorted_inds]

def print_info(info, ds_name):
    prefix = colored('Test-Suite:', 'blue')
    print_str = '{} {}'.format(prefix, info)
    print(print_str)

    p = path.join(cwd, 'runs')
    if not os.path.exists(p):
        os.mkdir(p)

    run_count = sum(path.isdir(i) for i in os.listdir(p))
    run_folder = path.join(p, 'run_{}'.format(run_count))
    if not os.path.exists(run_folder):
        os.mkdir(run_folder)
    
    f_name = '{}.log'.format(ds_name)
    f_path = path.join(run_folder, f_name)

    fil = open(f_path,"a+")
    fil.write('{}{}'.format(info, '\n'))
    fil.close()
