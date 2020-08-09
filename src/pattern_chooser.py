import random

def random_pattern(freq_pattern, pattern_count):
    print('Using pattern language Random: Selecting {} random pattern from our freq. subgraphs'.format(pattern_count))
    if pattern_count >= len(freq_pattern):
        print("Warning: Trying to select to more freq. subgraphs then present. Returning all subgraphs instead...")
        return freq_pattern
    sample_indezes = random.sample(range(len(freq_pattern)), pattern_count)
    pattern = []
    for si in sample_indezes:
        pattern.append(freq_pattern[si])
    return pattern

def graphlets(freq_pattern, minimum, maximum):
    print('Using pattern language Graphlets: Searching subgraphs with min.inc. {} and max.inc. {} vertices'.format(minimum, maximum))
    pattern = []
    for fq in freq_pattern:
        if fq.number_of_nodes() >= minimum and fq.number_of_nodes() <= maximum:
            pattern.append(fq)

    print('Found {} pattern matching the criterium'.format(len(pattern)))
    return pattern
