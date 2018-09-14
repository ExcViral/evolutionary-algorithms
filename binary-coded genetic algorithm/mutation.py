# Mutation is a genetic operator used to maintain genetic diversity from one generation of a population of chromosomes
# to the next. It is analogous to biological mutation.

# import necessary libraries

from bitarray import bitarray
import numpy as np

# Bit reversal mutation
# Generate a random number between 0 and 1, multiply it with number of genes in the chromosome, take integer part of it
# and select that index in the chromosome, and flip the bit value at that index.


def br_mutation(chromosome):
    """
    Function to perform bit reversal mutation in a given chromosome

    Algorithm:
    --[1] Generate a uniform random number 'r' between 0 and 1
    --[2] Multiply 'r' with number of genes in the chromosome, and take the integer part of it, i.e. drop the decimal
          part of it.
    --[3] Select 'rth' gene from chromosome, and flip/invert its value

    :param chromosome: (list of bitarray) of bits containing some number of genes, representing a chromosome
    :return: (bitarray) containing mutated chromosome
    """
    r = np.random.randint(0,len(chromosome[0]),40)
    for i in chromosome:
        for k in r:
            i[k] = not(i[k])
    return chromosome