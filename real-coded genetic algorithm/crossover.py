# Crossover is a genetic operator that combines(mates) two individuals(parents) to produce two new individuals(Childs).

# The idea behind crossover is that the new chromosome may be better than both of the parents if it takes the best
# characteristics from each of the parents.

# import necessary libraries
import numpy as np

# =====================================================================================================================
# ===== Crossover Operators ===========================================================================================
# =====================================================================================================================


def rv_crossover(parent1, parent2, mu):
    """
    This function is an implementation of real valued crossover operation

    NOTE: If you have any bounds for chromosome, check if the newly generated children satisfy the requirements, if
          not, discard the children, and introduce a new random chromosome satisfying the bounds.

    :param parent1: (list of float) carrying chromosomes of parent1
    :param parent2: (list of float) carrying chromosomes of parent2
    :param mu: (int) crossover operator, should be between 10 and 20, take 20
    :return: (list of list) containing children produced as a result of crossover
    """

    # calculate p
    p = 1/(mu + 1)
    # initialize empty lists to store children
    c1 = []
    c2 = []
    # iterate over the parents' chromosomes, and compute childrens' chromosomes and store them in lists
    for i in range(len(parent1)):
        # generate a random number between 0 and 1
        r = np.random.uniform(0, 1, 1)
        # compute value of b according to value of r
        if r > 0.5:
            b = pow(1 / (2 * (1 - r)), p)
        elif r <= 0.5:
            b = pow(2 * r, p)
        # compute childrens' chromosome value
        c1m = (1 / 2) * ((1 + b) * parent1[i] + (1 - b) * parent2[i])
        c2m = (1 / 2) * ((1 - b) * parent1[i] + (1 + b) * parent2[i])

        # NOTE: If you need to check for bounds, do it here

        # append chromosome to the lists
        c1.append(c1m)
        c2.append(c2m)
    return [c1, c2]
