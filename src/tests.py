from svm import perform_SVM
import convert
from pattern_chooser import Random, Graphlets, CORK
from helper import print_info

def test_SVM(data):
    # perform SVM accuracy testing
    print_info('Start training of our SVM')
    accuracies, predictions = perform_SVM(data['vector'], data['class'])
    print_info(accuracies)

class Tests:
    def __init__(self, freq_pattern, isomorph_graphs, ds_graph_classes):
        self._freq = freq_pattern
        self._ds_clss = ds_graph_classes
        self._iso_map = isomorph_graphs
        self._ds_size = len(ds_graph_classes)

    def graphlet_select(self):
        # pattern language graphlet-select, graphs with nodes in a certain range
        _idxs = Graphlets(self._freq, 5, 3).get_pattern()
        _ds = convert.dataset_to_vectors(self._iso_map, self._ds_clss, _idxs)
        test_SVM(_ds)
        print_info('\n-----[End Test]-----\n')

    def random(self):
        for percent in [0.2, 0.3, 0.5]:
            print_info('Testing Random Selection with {}%'.format(percent*100))
            # Pattern language get random pattern
            _idxs = Random(self._freq, int(percent * len(self._freq))).get_pattern()
            _ds = convert.dataset_to_vectors(self._iso_map, self._ds_clss, _idxs)
            test_SVM(_ds)
            print_info('\n-----[End Test]-----\n')

    def cork(self):    
        _idxs = CORK(self._freq, self._iso_map, self._ds_clss).get_pattern()
        print_info(_idxs)
        _ds = convert.dataset_to_vectors(self._iso_map, self._ds_clss, _idxs)
        test_SVM(_ds)
        print_info('\n-----[End Test]-----\n')
