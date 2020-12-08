import os
import re
from os import path
# implementations of TU Dortmund datasets
from torch_geometric.datasets import TUDataset

# our helper classes
import tests
import convert
import helper
import config
from helper import print_info

# gSpan Implementation
from gspan_mining.config import parser
from gspan_mining.main import main

# Try to surpress warnings
from sklearn.exceptions import ConvergenceWarning
import warnings

warnings.filterwarnings('ignore', 'ConvergenceWarning: Solver terminated early.*')
warnings.filterwarnings('ignore', 'Solver terminated early.*')
warnings.filterwarnings('ignore', category = ConvergenceWarning)


def test(ds_name, minSup, params='', random=False, graphlet=False, cork=False):
    if len(helper.tests_run) == 0:
        if random:
            helper.tests_run += "random"
        if graphlet:
            helper.tests_run += "graphlet"
        if cork:
            helper.tests_run += "cork"
    
    print_info('\n-----[BEGIN]-----\n')
    cwd = os.getcwd()
    freq_f_name = '{}.gspan.txt'.format(ds_name)
    freq_f_path = path.join(cwd, 'freq', freq_f_name)
    
    # if no run log is there, start a mining process
    dataset = TUDataset(root='./tmp/{}'.format(ds_name), name=ds_name)
    ds_graph_classes = dataset.data.y.tolist() # graph classes
    print_info('Starting Tests with dataset: {}, containing {} Graphs'.format(ds_name, len(dataset)))
    if not path.exists(freq_f_path):
        is_directed = dataset[0].is_directed()
        # create the run arguments for gSpan-python
        
        f_name = '{}.data.txt'.format(ds_name)
        f_path = path.join(cwd, 'graphs', f_name)
        args_str = '--min_support {min} --directed {directed} {params} --verbose FALSE --where TRUE {ds}'.format(ds = f_path, min=int(len(dataset) * minSup), directed=is_directed, params=params)
        print_info('Running with params: {}'.format(args_str))
        FLAGS, _ = parser.parse_known_args(args=args_str.split())
    
        # mine with gSpan
        print_info("Starting mining with gSpan-Algorithm and minSup sigma = {}%".format(minSup * 100))
        gs = main(FLAGS)
        _report = gs._report_df

        print_info("\nFinished mining. Found {} freq. subgraphs.".format(len(_report)))

        _freq = []
        sum_edges = 0
        sum_vertices = 0
        for dfs in _report['dfs']:
            _freq.append((dfs.get_num_vertices(), len(dfs)))
            sum_edges += len(dfs)
            sum_vertices += dfs.get_num_vertices()
        print_info("Durchschnitt Knoten: {}, Durchschnitt Kanten: {}\n".format( sum_vertices/len(_freq), sum_edges/len(_freq) ))

        # _desc = [desc for desc in _report['description']]

        # get info needed for testing
        isomorph_graphs = [gids for gids in _report['isomorph_graphs']]
    else:
        _freq = []
        sum_edges = 0
        sum_vertices = 0
        # _desc = []
        isomorph_graphs = []

        fil = open(freq_f_path, 'r') 
        count = 0
        
        curr_edges_c = 0
        curr_nodes_c = 0
        last_graph = 0
        while True:
            # Get next line from file 
            line = fil.readline() 
            # if line is empty 
            # end of file is reached 
            if not line: 
                break

            graph = re.match(r"(?P<graph>t # (?P<idx>[0-9]+))", line)
            node = re.match(r"(?P<node>v (?P<idx>[0-9]+) (?P<label>[0-9]+))", line)
            edge = re.match(r"(?P<edge>e (?P<from>[0-9]+) (?P<to>[0-9]+) (?P<label>[0-9]+))", line)
            isos = re.match(r"where: \[(?P<arr>([0-9]+, )+[0-9]+)\]", line)

            if graph:
                idx = int(graph.group('idx'))
                if idx != last_graph:
                    _freq.append((curr_nodes_c, curr_edges_c))
                    last_graph = idx
                    curr_edges_c = 0
                    curr_nodes_c = 0
            elif node:
                sum_vertices += 1
                curr_nodes_c += 1
            elif edge:
                sum_edges += 1
                curr_edges_c += 1
            elif isos:
                ds_idxs = isos.group('arr').split(',')
                iso_arr = []
                for ds_idx in ds_idxs:
                    iso_arr.append(int(ds_idx))
                isomorph_graphs.append(iso_arr)
        
        print_info("\nFinished parsing. of {} freq. subgraphs.".format(len(_freq)))
        fil.close()
        print_info("Durchschnitt Knoten: {}, Durchschnitt Kanten: {}\n".format( sum_vertices/len(_freq), sum_edges/len(_freq) ))
    # perform test
    _tests = tests.Tests(_freq, isomorph_graphs, ds_graph_classes)
    _tests.run(random, graphlet, cork)
    
    print_info('\n-----[END]-----\n')

args = config.parser.parse_args()
config.ds_name = args.dataset_name
config.minSup = args.support
config.params = args.params

test(config.ds_name, config.minSup, config.params, random=args.random, graphlet=args.graphlet, cork=args.cork) 
