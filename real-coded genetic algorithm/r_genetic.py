# This script is a template for main file of genetic algorithm, build and adapt it according to your application
# requirements

# import necessary libraries
import time
s = time.time()

import numpy as np

# import all modules
from crossover import kp_crossover
from fitness import fitness
from mutation import rv_mutation
from selection import tournament_selection, rank_selection


# ======================================================================================================================
# ===== Helper functions ===============================================================================================
# ======================================================================================================================


def init_population(size, n_of_chromosomes, search_domain_bounds):
    """
    Function to initialize random population

    :param size: (int) size of the population
    :param n_of_chromosomes: (int) number of chromosomes for each population member
    :param search_domain_bounds: (list) [lower bound, upper bound] within which solution is to be searched
    :return: (list) containing random population
    """
    population = []
    for i in range(size):
        chromosome = list(np.random.uniform(search_domain_bounds[0], search_domain_bounds[1], n_of_chromosomes))
        population.append(chromosome)
    return population


def terminator(best_pop):
    """
    This function will check if the stopping criteria has been met

    This function will help to check if there is a convergence to a solution, with the help of
    specified stopping criterias: Terminate if the best population has not changed over few hundred generations

    :param best_pop: (list) containing the best population of each generation over many generations
    :return: True, if stopping criteria is met, else False.
    """

    # Check if best population has not changed over past iterations
    c1 = all(x == best_pop[0] for x in best_pop)
    if c1:
        print("Stopping... best population has not changed from few iterations")
    return c1

# Add your helper functions here (if any)


# ======================================================================================================================
# ===== Genetic algorithm ==============================================================================================
# ======================================================================================================================


# Define parameters
cp = 0.8
mp = 0.2
mu = 20
eta = 15

# Step 1: Initialize the population

# Repeat from step 2 to 5 until termination criteria is not met

# Step 2: Select the members for mating

# Step 3: Perform crossover, i.e. mate the selected members to produce children

# Step 4: Perform mutation over the population: first select population, and then perform mutation

# Step 5: Evaluate fitness the new population, and select the top members and trim the size

# Check for terminating condition

# Print elapsed time
e = time.time() - s
print("Elapsed Time: ", e)
