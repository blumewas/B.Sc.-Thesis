import os
from os import path
# implementations of TU Dortmund datasets
from torch_geometric.datasets import TUDataset

# our helper classes
import tests
import convert
import helper
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
    if len(params) > 0:
        print_info('Running with extra params: {}'.format(params))
    convert.dataset_to_datafile(dataset, ds_name)

    # create the run arguments for gSpan-python
    cwd = os.getcwd()
    f_name = '{}.data.txt'.format(ds_name)
    f_path = path.join(cwd, 'graphs', f_name)
    args_str = '--min_support {min} --directed TRUE {params} --verbose FALSE --where TRUE {ds}'.format(ds = f_path, min=int(len(dataset) * minSup), params=params)
    FLAGS, _ = parser.parse_known_args(args=args_str.split())
 
    # mine with gSpan
    print_info("Starting mining with gSpan-Algorithm and minSup sigma = {}%".format(minSup * 100))
    gs = main(FLAGS)
    _report = gs._report_df
    _freq = [dfs for dfs in _report['dfs']]

    # get info needed for testing
    ds_graph_classes = dataset.data.y.tolist() # graph classes
    isomorph_graphs = [gids for gids in _report['isomorph_graphs']]

    print_info("\nFinished mining. Found {} freq. subgraphs\n".format(len(_report)))
    # perform test
    _tests = tests.Tests(_freq, isomorph_graphs, ds_graph_classes)
    _tests.run(random, graphlet, cork)
    
    print_info('\n-----[END]-----\n')

datasets = ['NCI1'] #, 'MUTAG', 'PTC_FM', 'DD', 'PROTEINS']
extra_params = {
    'MUTAG': '-u 8 -mm 100',
    'PTC_FM': '-mm 100',
    'NCI1': '-u 12 -mm 100',
    'DD': '-mm 100',
    'PROTEINS': '-mm 100' 
}
min_supps = [0.1] #, 0.3, 0.5]
for ds_name in datasets:
    helper.ds_name = ds_name
    for min_sup in min_supps:
        params = extra_params[ds_name]
        test(ds_name, min_sup, params, random=False, graphlet=False, cork=True)
