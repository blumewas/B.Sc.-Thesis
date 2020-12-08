from svm import perform_SVM
import convert
from pattern_chooser import Random, Graphlets, CORK
from helper import print_info
from timers import take_time, InlineTimer

def test_SVM(data):
    # perform SVM accuracy testing
    print_info('Start training of our SVM')
    accuracies, predictions = perform_SVM(data['vector'], data['class'])
    print_info(accuracies)

class Tests:
    def __init__(self, freq_pattern, isomorph_graphs, ds_graph_classes, descriptions=None):
        self._freq = freq_pattern
        self._ds_clss = ds_graph_classes
        self._iso_map = isomorph_graphs
        self._ds_size = len(ds_graph_classes)
        # self._desc = descriptions

    def run(self, random=False, graphlet=False, cork=False):
        if random:
            self.random()
        if graphlet:
            self.graphlet_select()
        if cork:
            self.cork()

    @take_time('tests')
    def graphlet_select(self):
        # pattern language graphlet-select, graphs with nodes in a certain range
        _it = InlineTimer('Select pattern')
        
        _it.time()
        _idxs = Graphlets(self._freq, 5, 3).get_pattern()
        _it.time()
        
        _it = InlineTimer('Training SVM graphlets')
        
        _it.time()
        _ds = convert.dataset_to_vectors(self._iso_map, self._ds_clss, _idxs)
        test_SVM(_ds)
        _it.time()
        
        print_info('\n-----[End Test]-----\n')
    
    @take_time('tests')
    def random(self):
        for percent in [0.2, 0.3, 0.5]:
            print_info('Testing Random Selection with {}%'.format(percent*100))
            _select = int(percent * len(self._freq))
            if _select > self._ds_size:
                _select = self._ds_size
                print_info('Would select too many graphs. Limiting it to Dataset-Size ({} graphs)'.format(_select))
            # Pattern language get random pattern
            _it = InlineTimer('Selecting pattern')
            _it.time()
            _idxs = Random(self._freq, ).get_pattern()
            _it.time()
            
            _it = InlineTimer('Training SVM random')
            _it.time()
            _ds = convert.dataset_to_vectors(self._iso_map, self._ds_clss, _idxs)
            test_SVM(_ds)
            _it.time()

            print_info('\n-----[End Test]-----\n')

    @take_time('tests')
    def cork(self):
        _it = InlineTimer('Select pattern')
        
        _it.time() 
        _idxs = CORK(self._freq, self._iso_map, self._ds_clss).get_pattern()
        _it.time() 

        print_info("Selected {} pattern using CORK".format(len(_idxs)))
        print_info(_idxs)

        _it = InlineTimer('Training SVM cork')

        _it.time()
        _ds = convert.dataset_to_vectors(self._iso_map, self._ds_clss, _idxs)
        test_SVM(_ds)
        _it.time()

        print_info('\n-----[End Test]-----\n')
