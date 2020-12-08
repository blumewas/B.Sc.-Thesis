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
            num_vert, num_edges = self._freq[idx]
            if num_vert >= self._min and num_vert <= self._max:
                pattern.append(idx)

        print_info('Found {} pattern matching the criterium'.format(len(pattern)))
        return pattern

class CORK:
    def __init__(self, freq_pattern, isomorph_graphs, graph_classes, descriptions=None):
        self._freq = freq_pattern
        self._isomorphic = isomorph_graphs
        self._ds_classes = graph_classes
        # self._desc = descriptions
        vecs = []
        for i in graph_classes:
            vecs.append([])
        self._vecs = vecs
        self._ds = convert.dataset_to_vectors(isomorph_graphs, graph_classes)

    def get_equivalences(self, vectors=[]):
        # calc
        equivalenz_classes = {}
        _vecs = vectors
        _clss = self._ds_classes
        if len(_vecs) == 0:
            _vecs = self._vecs

        for gid in range(len(_vecs)):
            g_vec = _vecs[gid]
            g_cls = _clss[gid]
            str_vec = ','.join([str(d) for d in g_vec])
            if str_vec in equivalenz_classes:
                cls_0, cls_1 = equivalenz_classes[str_vec]
                if g_cls == 0:
                    equivalenz_classes[str_vec] = (cls_0 + 1, cls_1)
                if g_cls == 1:
                    equivalenz_classes[str_vec] = (cls_0, cls_1 + 1)
            else:
                if g_cls == 0:
                    equivalenz_classes[str_vec] = (1, 0)
                if g_cls == 1:
                    equivalenz_classes[str_vec] = (0, 1)
        return equivalenz_classes

    def get_hits_misses(self, idx):
        hits_0 = misses_0 = hits_1 = misses_1 = 0
        _vecs = self._ds['vector']
        for (i, graph) in enumerate(_vecs):
            _cls = self._ds['class'][i]
            if _cls == 1:
                if graph[idx] == 1:
                    hits_1 += 1
                elif graph[idx] == 0:
                    misses_1 += 1
            elif _cls == 0:
                if graph[idx] == 1:
                    hits_0 += 1
                elif graph[idx] == 0:
                    misses_0 += 1

        return (hits_0, misses_0, hits_1, misses_1)

    def get_pattern(self):
        print_info('Using CORK to mine discriminative freq. subgraphs.')

        # init siblings_map
        freq_count = len(self._freq)
        siblings_map = [0] * freq_count
        for i in range(len(siblings_map)):
            curr_nodes, curr_edges = self._freq[i]
            for j in range(i+1, freq_count):
                _num_nodes, _num_edges = self._freq[j]
                if _num_edges <= curr_edges:
                    siblings_map[i] = j
                    break
            if siblings_map[i] == 0:
                siblings_map[i] = freq_count
        
        idxs = []
        con = True
        while(con):
            next_idx = -1
            i = 0
            while i < len(self._freq):
                if self.calc_cork(i) > self.calc_cork(next_idx, initial=(len(idxs) == 0)):
                    next_idx = i
                
                if self.max_cork(i) <= self.calc_cork(next_idx):
                    i = siblings_map[i]
                else:
                    i += 1

            if self.calc_cork(next_idx) > self.calc_cork():
                idxs.append(next_idx)
                self.extend_ds(next_idx, True)
                print_info("selected {}".format(next_idx))
            else:
                con = False
        
        return idxs

    def extend_ds(self, idx, save=False):
        if idx == -1:
            return (self._vecs, self._ds['class'])
        size = len(self._ds_classes)
        vec_data = []
        
        for gid in range(size):
            bin_vec = self._vecs[gid].copy()
            
            if gid in self._isomorphic[idx]:
                bin_vec.append(1)
            else: bin_vec.append(0)

            vec_data.append(bin_vec)

        if save:
            self._vecs = vec_data
        return (vec_data, self._ds_classes)

    def max_cork(self, g_idx):
        _vecs, _clss = self.extend_ds(g_idx)

        max_cork = self.calc_cork(g_idx)
        equivalenz_classes = self.get_equivalences(_vecs)
        
        hits_0, miss_0, hits_1, miss_1 = self.get_hits_misses(g_idx)
        for key in equivalenz_classes:
            cls_0, cls_1 = equivalenz_classes[key]

            cls_hits_0 = cls_0 + hits_0
            cls_miss_0 = cls_0 + miss_0
            cls_hits_1 = cls_1 + hits_1
            cls_miss_1 = cls_1 + miss_1

            max_cork += max(cls_hits_0 * (cls_hits_1 - cls_miss_1), (cls_hits_0 - cls_miss_0) * cls_hits_1, 0)
        return max_cork

    def calc_cork(self, added_idx=-1, initial=False):
        if initial:
            if added_idx == -1:
                return float('-inf')

        # calc        
        _vecs, _clss = self.extend_ds(added_idx)
        equivalenz_classes = self.get_equivalences(_vecs)
        cork = 0
        for key in equivalenz_classes:
            cls_0, cls_1 = equivalenz_classes[key]
            cork += cls_0  * cls_1
        return cork * -1
