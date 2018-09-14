# Mutation is a genetic operator used to maintain genetic diversity from one generation of a population of chromosomes
# to the next. It is analogous to biological mutation.

# import necessary libraries
import numpy as np


def rv_mutate(chromosome, eta):
    """
    This function is an implementation of real value mutation

    NOTE: If you have any bounds for chromosome, check if the newly generated children satisfy the requirements, if
          not, discard the children, and introduce a new random chromosome satisfying the bounds.

    :param chromosome: (list of float) containing
    :param eta: (int) mutation operator, typically between 15 to 20, take 15
    :return: ()
    """
    # calculate p
    p = 1 / (eta + 1)
    # generate a random number r between 0 and 1, and calculate d accordingly
    r = np.random.uniform(0, 1, 1)
    if r > 0.5:
        d = 1 - pow((2 * (1 - r)), p)
    elif r <= 0.5:
        d = pow(2 * r, p) - 1

    mutated_chromosome = [i + d for i in chromosome]

    # NOTE: If you need to check for bounds, do it here before returning

    return mutated_chromosome