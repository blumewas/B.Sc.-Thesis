import random
from helper import print_info

def random_pattern(ds_name, freq_pattern_count, kernel_size):
    print_info('Using pattern language "random". Selecting {} random pattern from our freq. subgraphs'.format(kernel_size), ds_name)
    if kernel_size >= freq_pattern_count:
        print_info("Warning: Trying to select to more freq. subgraphs then present. Returning all subgraphs instead...", ds_name)
        return freq_pattern_count
    return sorted(random.sample(range(1, freq_pattern_count+1), kernel_size))

def graphlets(ds_name, freq_pattern, maximum, minimum=2):
    print_info('Using pattern language "graphlet-select". Searching subgraphs with min.inc. {} and max.inc. {} vertices'.format(minimum, maximum), ds_name)
    pattern = []
    for fq in freq_pattern:
        if fq.number_of_nodes() >= minimum and fq.number_of_nodes() <= maximum:
            pattern.append(fq)

    print_info('Found {} pattern matching the criterium'.format(len(pattern)), ds_name)
    return pattern
