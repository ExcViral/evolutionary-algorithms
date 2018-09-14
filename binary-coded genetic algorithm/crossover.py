# Crossover is a genetic operator that combines(mates) two individuals(parents) to produce two new individuals(Childs).

# The idea behind crossover is that the new chromosome may be better than both of the parents if it takes the best
# characteristics from each of the parents.

# import necessary libraries

import numpy as np
from bitarray import bitarray

# =====================================================================================================================
# ===== Helper functions ==============================================================================================
# =====================================================================================================================


def unique_rn_generator(low, high, n):
    """
    Function to generate a list of unique random integers

    This function uses numpy's random number generator to generate a list of random numbers, checks if all the numbers
    in the list are unique, if they are unique, the list is returned. If they are not unique, then the list is generated
    repeatedly until a list with unique numbers is generated.

    :param low: (int) lowest (inclusive) acceptable random number
    :param high: (int) highest (not inclusive) acceptable random number
    :param n: (int) number of random numbers to be generated
    :return: (list) containing 'n' unique random numbers
    """
    r = np.random.randint(low, high, n)
    while len(r) != len(set(r)):
        r = np.random.randint(low, high, n)
    return r

# =====================================================================================================================
# ===== Crossover Operators ===========================================================================================
# =====================================================================================================================


def kp_crossover(parent1, parent2, k):
    """
    This function is implementation of "k-point crossover" of genetic algorithm

    Algorithm:
    --[1] Generate k unique random numbers between 0 and n, where n is the number of genes in parents.
    --[2] Perform crossover with the following strategy:
            Single-point crossover (k = 1):
                A point on both parents' chromosomes is picked randomly, and designated a 'crossover point'. Bits to the
                right of that point are swapped between the two parent chromosomes. This results in two offspring, each
                carrying some genetic information from both parents.
            Two-point and k-point crossover (k = 2):
                n two-point crossover, two crossover points are picked randomly from the parent chromosomes. The bits in
                between the two points are swapped between the parent organisms. Two-point crossover is equivalent to
                performing two single-point crossovers with different crossover points.
          This strategy can be generalized to k-point crossover for any positive integer k, picking k crossover points.

    :param parent1: (list of bitarray) containing chromosomes of parent 1
    :param parent2: (list of bitarray) containing chromosomes of parent 2
    :param k: (int) number of points for crossover
    :return: (list of list of bitarray) containing 2 children of parent 1 and parent 2
    """

    c1 = []
    c2 = []
    for j in range(len(parent1)):
        r = unique_rn_generator(1, len(parent1[j]), k)
        switch = False
        c1m = bitarray()
        c2m = bitarray()
        for i in range(len(parent1[j])):
            if i in r:
                switch = not switch
            if not switch:
                c1m.append(parent1[j][i])
                c2m.append(parent2[j][i])
            elif switch:
                c1m.append(parent2[j][i])
                c2m.append(parent1[j][i])
        c1.append(c1m)
        c2.append(c2m)
    return [c1, c2]


def uniform_crossover(parent1, parent2):
    """
    This function is implementation of "uniform crossover" operator of genetic algorithm

    In uniform crossover, bits are randomly copied from the first or from the second parent, and two children are
    generated.

    Algorithm:
    --[1] Generate a mask of length same as number of genes in parents, mask will contain 0 or 1 at random positions
    --[2] Swap the gene values of parents for positions where there are 1's in mask, and do nothing where there are 0's
          in the mask.

    :param parent1: (list of bitarray) containing genes of parent 1
    :param parent2: (list of bitarray) containing genes of parent 2
    :return: (list of list of bitarrays) containing 2 children of parent 1 and parent 2
    """
    c1 = []
    c2 = []
    mask = np.random.randint(0, 2, len(parent1[0]))
    for j in range(len(parent1)):
        c1m = bitarray()
        c2m = bitarray()
        for i in range(len(mask)):
            if mask[i] == 1:
                c1m.append(parent2[j][i])
                c2m.append(parent1[j][i])
            else:
                c1m.append(parent1[j][i])
                c2m.append(parent2[j][i])
        c1.append(c1m)
        c2.append(c2m)
    return [c1, c2]