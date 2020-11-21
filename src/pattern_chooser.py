import random
import numpy
from helper import print_info

def random_pattern(ds_name, freq_pattern_count, kernel_size):
    print_info('Using pattern language "random". Selecting {} random pattern from our freq. subgraphs'.format(kernel_size), ds_name)
    if kernel_size >= freq_pattern_count:
        print_info("Warning: Trying to select to more freq. subgraphs then present. Returning all subgraphs instead...", ds_name)
        return freq_pattern_count
    return sorted(random.sample(range(1, freq_pattern_count+1), kernel_size))

def graphlets(ds_name, vertice_map, maximum, minimum=2):
    print_info('Using pattern language "graphlet-select". Searching subgraphs with min.inc. {} and max.inc. {} vertices'.format(minimum, maximum), ds_name)
    pattern = []
    for (idx, num_vert) in enumerate(vertice_map):
        if num_vert >= minimum and num_vert <= maximum:
            pattern.append(idx + 1)

    print_info('Found {} pattern matching the criterium'.format(len(pattern)), ds_name)
    return pattern

class CORK:
    def __init__(self, ds_name, freq_pattern, isomorph_graphs, graph_classes): 
        self.ds_name = ds_name
        self._freq = freq_pattern
        self._isomorphic = isomorph_graphs
        self._g_classes = graph_classes

    def print_info(self, pstr):
        print_info(pstr, self.ds_name)

    def get_pattern(self):
        self.print_info('Using CORK to mine discriminative freq. subgraphs.')
        sorted_dfs_codes = sorted(self._freq)
        # siblings_map = [0] * len(freq_pattern)
        # # # init siblings_map

        idxs = []
        while 1:
            next_idx = -1
            i = 0
            while i < len(freq_pattern):
                if calc_cork(idxs, i) > calc_cork(idxs, next_idx):
                    next_graph = freq_pattern[i]
                if true:
                    i = siblings_map[i]
                else:
                    i += 1
            
            if calc_cork(idxs, next_idx) > calc_cork(idxs):
                idxs.append(idx)
            else:
                break
        return idxs

    def calc_cork(self, curr_pattern, added_idx=-1):
        selected = curr_pattern.copy()
        if added_idx != -1:
            selected.append(added_idx)
        # calc 
