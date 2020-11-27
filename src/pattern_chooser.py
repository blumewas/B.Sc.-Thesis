import random
import convert
import numpy
from helper import print_info

class Random:
    def __init__(self, freq_pattern, kernel_size):
        self._freq = freq_pattern
        self._kernel_size = kernel_size

    def get_pattern(self):
        freq_size = len(self._freq)
        print_info('Using pattern language "random". Selecting {} random pattern from our freq. subgraphs'.format(self._kernel_size))
        if self._kernel_size >= freq_size:
            print_info("Warning: Trying to select to more freq. subgraphs then present. Returning all subgraphs instead...")
            return range(freq_size)
        return sorted(random.sample(range(freq_size), self._kernel_size))

class Graphlets:
    def __init__(self, freq_pattern, maximum, minimum=2):
        self._max = maximum
        self._min = minimum
        self._freq = freq_pattern

    def get_pattern(self):
        freq_size = len(self._freq)
        print_info('Using pattern language "graphlet-select". Searching subgraphs with min.inc. {} and max.inc. {} vertices'.format(self._min, self._max))
        pattern = []
        for idx in range(freq_size):
            num_vert = self._freq[idx].get_num_vertices()
            if num_vert >= self._min and num_vert <= self._max:
                pattern.append(idx)

        print_info('Found {} pattern matching the criterium'.format(len(pattern)))
        return pattern

# TODO work on cork
class CORK:
    def __init__(self, freq_pattern, isomorph_graphs, graph_classes):
        self._freq = freq_pattern
        self._isomorphic = isomorph_graphs
        self._ds_classes = graph_classes

    def get_pattern(self):
        print_info('Using CORK to mine discriminative freq. subgraphs.')

        sorted_dfs_codes = sorted(self._freq)
        # init siblings_map
        siblings_map = [0] * len(self._freq)
        for i in range(len(siblings_map)):
            curr_code = sorted_dfs_codes[i]
            for j in range(i+1, len(sorted_dfs_codes)):
                if len(sorted_dfs_codes[j]) <= len(curr_code):
                    siblings_map[i] = j
                    break
            if siblings_map[i] == 0:
                siblings_map[i] = len(self._freq)
        
        idxs = []
        con = True
        while(con):
            next_idx = -1
            i = 0
            while i < len(self._freq):
                if self.calc_cork(idxs, i) > self.calc_cork(idxs, next_idx):
                    next_idx = i

                if self.max_cork(idxs, i) <= self.calc_cork(idxs, next_idx):
                    i = siblings_map[i]
                else:
                    i += 1
                
            if self.calc_cork(idxs, next_idx) > self.calc_cork(idxs):
                idxs.append(next_idx)
            else:
                con = False
        
        return idxs

    def max_cork(self, curr_pattern, g_idx):
        selected = curr_pattern.copy()
        selected.append(g_idx)

        equivalenz_classes = {}
        _ds = convert.dataset_to_vectors(self._isomorphic, self._ds_classes, selected)
        _vecs = _ds['vector']
        _clss = _ds['class']
        for gid in range(len(_vecs)):
            g_vec = _vecs[gid]
            g_cls = _clss[gid]
            str_vec = ','.join([str(d) for d in g_vec])
            if str_vec in equivalenz_classes:
                equivalenz_classes[str_vec].append((g_cls, g_vec[-1]))
            else:
                equivalenz_classes[str_vec] = [(g_cls, g_vec[-1])]
        
        max_cork = self.calc_cork(selected)

        for key in equivalenz_classes:
            # print(equivalenz_classes[key])
            a_hits = 0 # all hits with class 0
            a_misses = 0 # all misses with class 0
            b_hits = 0 # all hits with class 1
            b_misses = 0 # all misses with class 1
            for g_cls, hit in equivalenz_classes[key]:
                if g_cls == 0:
                    if hit == 1:
                        a_hits += 1
                    else:
                        a_misses += 1
                else:
                    if hit == 1:
                        b_hits += 1
                    else:
                        b_misses += 1
            max_cork += max(a_hits * (b_hits - b_misses), (a_hits - a_misses) * b_hits, 0)

        return max_cork

    def calc_cork(self, curr_pattern, added_idx=-1):
        if len(curr_pattern) == 0:
            if added_idx == -1:
                return float('-inf')

        selected = curr_pattern.copy()
        if added_idx != -1:
            selected.append(added_idx)
        # calc
        equivalenz_classes = {}
        _ds = convert.dataset_to_vectors(self._isomorphic, self._ds_classes, selected)
        _vecs = _ds['vector']
        _clss = _ds['class']
        for gid in range(len(_vecs)):
            g_vec = _vecs[gid]
            g_cls = _clss[gid]
            str_vec = ','.join([str(d) for d in g_vec])
            if str_vec in equivalenz_classes:
                equivalenz_classes[str_vec].append(g_cls)
            else:
                equivalenz_classes[str_vec] = [g_cls]
        
        cork = 0
        for key in equivalenz_classes:
            _cls, instances = numpy.unique(equivalenz_classes[key], return_counts=True)
            a_instances = 0 # all with class 0
            b_instances = 0 # all with class 1
            if len(_cls) == 2:
                cork += instances[0]  * instances[1] # if two classes are found in E_c here is the count for class 1

        return cork * -1
