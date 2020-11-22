import random
import convert
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
        self._ds_classes = graph_classes

    def print_info(self, pstr):
        print_info(pstr, self.ds_name)

    def get_pattern(self):
        self.print_info('Using CORK to mine discriminative freq. subgraphs.')

        sorted_dfs_codes = sorted(self._freq)
        # init siblings_map
        siblings_map = [0] * len(self._freq)
        for i in range(len(siblings_map)):
            curr_code = sorted_dfs_codes[i]
            for j in range(i+1, len(sorted_dfs_codes)):
                if siblings_map[i] == 0:
                    siblings_map[i] = j
                if len(sorted_dfs_codes[j]) <= len(curr_code):
                    siblings_map[i] = j
                    break

        idxs = []
        while 1:
            next_idx = -1
            i = 0
            while i <= len(self._freq):
                if i == len(self._freq):
                    break
                if self.calc_cork(idxs, i) > self.calc_cork(idxs, next_idx):
                    next_idx = i
                if self.max_cork(idxs, i) <= self.calc_cork(idxs, next_idx):
                    i = siblings_map[i]
                    if i == 0: # abort at end of siblings_map
                        break
                else:
                    i += 1
            
            if self.calc_cork(idxs, next_idx) <= self.calc_cork(idxs):
                return idxs
                # self.print_info(idxs)
            
            idxs.append(next_idx)
        
        return idxs

    def max_cork(self, curr_pattern, g_idx):
        selected = curr_pattern.copy()
        selected.append(g_idx)

        equivalenz_classes = {}
        # self.print_info(selected)
        _ind_vecs = convert.dataset_to_vectors_freq(self._isomorphic, self._ds_classes, selected)
        for g_cls, g_vec in _ind_vecs:
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
        selected = curr_pattern.copy()
        if added_idx != -1:
            selected.append(added_idx)
        # calc
        equivalenz_classes = {}
        _ind_vecs = convert.dataset_to_vectors_freq(self._isomorphic, self._ds_classes, selected)
        for g_cls, g_vec in _ind_vecs:
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
            if len(_cls) == 1:
                if _cls[0] == 0:
                    a_instances = instances[0]
                else:
                    b_instances = instances[0]
            else:
                a_instances = instances[0] 
                b_instances = instances[1] # if two classes are found in E_c here is the count for class 1
            cork += a_instances * b_instances
        return cork * -1
