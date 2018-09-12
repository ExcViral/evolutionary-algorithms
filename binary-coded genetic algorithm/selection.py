# A proportion of the existing population is selected to bread a new bread of generation. Parents with better fitness
# have better chances to produce offspring.

# NOTE: Please define a fitness function in fitness.py or this module will not work

# import necessary libraries

import numpy as np
import math
from bitarray import bitarray

from fitness import fitness

# ======================================================================================================================
# ===== Helper Functions ===============================================================================================
# ======================================================================================================================


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
    while(len(r) != len(set(r))):
        r = np.random.randint(low, high, n)
    return r


def round_up_to_even(f):
    """
    This function rounds up a number to an even number.

    The function just divides the value by 2, rounds up to the nearest integer, then multiplies by 2 again

    :param f: (float) that is to be rounded up to an even number
    :return: (int) input number rounded up to next even number
    """
    return int(math.ceil(f / 2.) * 2)

# ======================================================================================================================
# ===== Selection Algorithms ===========================================================================================
# ======================================================================================================================


def tournament_selection(population, cp, k, mode):
    """
    This function is an implementation of tournament selection algorithm

    Runs a "tournament" among a few individuals chosen at random from the population and selects the winner (the one
    with the best fitness) for crossover

    Algorithm: Pick 'k' number of entities out of the pool, compare their fitness, and the best is permitted to
            reproduce.

    Selection pressure can be easily adjusted by changing the tournament size 'k'.
    Deterministic tournament selection selects the best individual in each tournament.

    :param population: (list of bitarray) containing chromosomes(bitarray) represented by genes(bits)
    :param cp: (float) crossover probability, typically should be between 0.8 and 1
    :param k: (int) number of members allowed to participate in each tournament that is held
    :param mode: (string) to set whether working on minimization(pass: "min") or maximization(pass: "max") problem
    :return: (list) containing indices of selected chromosomes from the population
    """

    # check whether to minimize or maximize
    if mode == "min":
        flag = False
    elif mode == "max":
        flag = True
    else:
        raise ValueError("Incorrect mode selected, please pass 'min' or 'max' as mode")

    # list that will keep track of selected indices, so that selection is done without replacement.
    selected_indices = []
    # number of parents to be selected
    n = round_up_to_even(len(population)*cp)
    # create a copy of original population alongwith their respective indices, because we will be removing winner of
    # tournament from this array, and we need to preserve original indices of population members.
    numbered_population = [[l, m] for l, m in zip(population, range(len(population)))]
    # start selecting parents for crossover
    for i in range(n):
        # Generate k unique random numbers
        if (k < len(numbered_population)):
            r = unique_rn_generator(0, len(numbered_population), k)
        # However, if the list is exhausted, i.e there are less than k unique members left, repetition is allowed
        elif (k >= len(numbered_population)):
            r = np.random.randint(0, len(numbered_population), k)
        # empty list to store fitnesses of tournament participator members
        fitnesses = []
        # calculate fitness of each tournament paticipator and append it to fitnesses list
        for a in r:
            fitnesses.append(fitness(numbered_population[a][0]))
        # Assume that index 0 is the fittest tournament participator, so set index = 0
        index = 0
        # Compare fitness of each tournament participator with fitness of participator on whom index is  currently
        # pointing, update index if fitness of non indexed participant is higher than indexed, else no change.
        # if problem is of maximization
        if flag:
            for j in range(len(r)):
                if fitnesses[index] < fitnesses[j]:
                    index = j
        # if problem is of minimization
        else:
            for j in range(len(r)):
                if fitnesses[index] > fitnesses[j]:
                    index = j

        # Copy the original position of winner, and update it to selected_indices list
        winner = numbered_population[r[index]][1]
        selected_indices.append(winner)
        # delete the winner from the numbered_population, i.e. ban it from further entering the tournament
        del numbered_population[r[index]]

    return selected_indices


def rank_selection(population, mode):
    """
    This function is an implementation of rank selection algorithm

    Rank selection first ranks the population and then every chromosome receives fitness from this ranking. Here,
    selection is based on this ranking rather than absolute differences in fitness.

    :param population: (list of bitarray) containing chromosomes(bitarray) represented by genes(bits)
    :param mode: (string) to set whether working on minimization(pass: "min") or maximization(pass: "max") problem
    :return: (list of bitarray) containing original chromosomes, but ranked in order according to their fitness
    """

    # calculate fitness of all population members and store it in a new list fitnesses
    fitnesses = [fitness(i) for i in population]

    # now we have fitness of each population member, rank them according to their fitness, i.e. sort the population list
    # according to the fitness values of population members, depending on whether it is minimization or maximization,
    # sort ascending or descending.

    # check whether to minimize or maximize
    if mode == "max":
        return [i for _, i in sorted(zip(fitnesses, population), reverse=True)]
    elif mode == "min":
        return [i for _, i in sorted(zip(fitnesses, population), reverse=False)]
    else:
        raise ValueError("Incorrect mode selected, please pass 'min' or 'max' as mode")
