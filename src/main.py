import os
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

warnings.filterwarnings('once', 'ConvergenceWarning: Solver terminated early.*')
warnings.filterwarnings('once', 'Solver terminated early.*')
warnings.filterwarnings('once', category = ConvergenceWarning)


def test(ds_name, minSup, params='', random=False, graphlet=False, cork=False):
    if len(helper.tests_run) == 0:
        if random:
            helper.tests_run += "random"
        if graphlet:
            helper.tests_run += "graphlet"
        if cork:
            helper.tests_run += "cork"
    
    print_info('\n-----[BEGIN]-----\n')
    dataset = TUDataset(root='./tmp/{}'.format(ds_name), name=ds_name)
    print_info('Starting Tests with dataset: {}, containing {} Graphs'.format(ds_name, len(dataset)))
        
    is_directed = dataset[0].is_directed()
    # create the run arguments for gSpan-python
    cwd = os.getcwd()
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
        _freq.append(dfs)
        sum_edges += len(dfs)
        sum_vertices += dfs.get_num_vertices()
    print_info("Durchschnitt Knoten: {}, Durchschnitt Kanten: {}\n".format( sum_vertices/len(_freq), sum_edges/len(_freq) ))

    _desc = [desc for desc in _report['description']]

    # get info needed for testing
    ds_graph_classes = dataset.data.y.tolist() # graph classes
    isomorph_graphs = [gids for gids in _report['isomorph_graphs']]

    
    # perform test
    _tests = tests.Tests(_freq, isomorph_graphs, ds_graph_classes, _desc)
    _tests.run(random, graphlet, cork)
    
    print_info('\n-----[END]-----\n')

args = config.parser.parse_args()
config.ds_name = args.dataset_name
config.minSup = args.support
config.params = args.params

test(config.ds_name, config.minSup, config.params, random=args.random, graphlet=args.graphlet, cork=args.cork) 
