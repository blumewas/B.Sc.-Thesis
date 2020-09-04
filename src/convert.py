import os
from os import path
import networkx as nx

cwd = os.getcwd()

def dataset_to_datafile(dataset, name):
    p = path.join(cwd, 'graphs')
    if not os.path.exists(p):
        os.mkdir(p)

    f_name = '{}.data.txt'.format(name)
    f_path = path.join(p, f_name)

    if os.path.exists(f_path):
        return

    f = open(f_path,"w+")

    # get the feature count
    num_node_features = dataset.num_node_features
    num_edge_features = dataset.num_edge_features
    
    for (index, graph_data) in enumerate(dataset):
        
        f.write('t # {}\n'.format(index))
        num_nodes = graph_data.num_nodes
        # Add nodes
        if 'x' in graph_data:
            # Node labels matrix, with shape [node_count,label_count], to indicate that the node x has the label y, value 1 is found at [x, y]
            x = graph_data['x']
            for v in range(num_nodes):
                for i in range(num_node_features):
                    if x[v][i] == 1: # vertex has label i
                        f.write('v {} {}\n'.format(v, i))
                        break
        else:
            for v in range(num_nodes):
                f.write('v {} 1\n'.format(v))

        num_edges = graph_data.num_edges
        edge_index = graph_data['edge_index']
        # Add edges to file
        if 'edge_attr' in graph_data:
            edge_attr = graph_data['edge_attr'] # Same as node_labels, for edge_labels respectively
            for e in range(num_edges):
                u = edge_index[0][e]
                v = edge_index[1][e]
                for i in range(num_edge_features):
                    if edge_attr[e][i] == 1:
                        f.write('e {} {} {}\n'.format(u, v, i))
                        break
        else:
            for e in range(num_edges):
                u = edge_index[0][e]
                v = edge_index[1][e]
                f.write('e {} {} 1\n'.format(u, v))
    f.write('t # -1')
    f.close()
    return


def dataset_to_networkX(dataset):
    
    nx_dataset = []
    # get the feature count
    num_node_features = dataset.num_node_features
    num_edge_features = dataset.num_edge_features
    
    for (index, graph_data) in enumerate(dataset):
        G = nx.DiGraph()
        num_nodes = graph_data.num_nodes
        # Add nodes to nxDiGraph
        if 'x' in graph_data:
            # Node labels matrix, with shape [node_count,label_count], to indicate that the node x has the label y, value 1 is found at [x, y]
            x = graph_data['x']
            for v in range(num_nodes):
                for i in range(num_node_features):
                    if x[v][i] == 1: # vertex has label i
                        G.add_node(v, label=i)
                        break
        else:
            for v in range(num_nodes):
                G.add_node(v)

        num_edges = graph_data.num_edges
        edge_index = graph_data['edge_index'].numpy()
        # Add edges to nxDiGraph
        if 'edge_attr' in graph_data:
            edge_attr = graph_data['edge_attr'] # Same as node_labels, for edge_labels respectively
            for e in range(num_edges):
                u = edge_index[0][e]
                v = edge_index[1][e]
                for i in range(num_edge_features):
                    if edge_attr[e][i] == 1: # edge has label i
                        G.add_edge(u, v, label=i)
                        break
        else:
            for e in range(num_edges):
                u = edge_index[0][e]
                v = edge_index[1][e]
                G.add_edge(u, v)

        nx_dataset.append(G)
    return nx_dataset

def dfscode_to_networkX(freq_dfs):
    nx_freq = []
    for dfs_code in freq_dfs:
        G = nx.DiGraph()
        for edge in dfs_code:
            u = edge.frm
            v = edge.to
            ulbl, elbl, vlbl = edge.vevlb
            if ulbl != -1:
                G.add_node(u, label=int(ulbl))
            if vlbl != -1:
                G.add_node(v, label=int(vlbl))

            G.add_edge(u, v, label=int(elbl))
        
        nx_freq.append(G)

    return nx_freq
