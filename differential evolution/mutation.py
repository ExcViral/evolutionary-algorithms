# DE generates new parameter vectors by adding the weighted difference between two parameter vectors to a third vector.
# Several different schemes of DE exist, according to target vector selection and difference vector creation.

# Here we will be implementing five different types de mutation algorithms:
#
#   V_(i,G) :: ith Mutant vector of generation G
#   X_(i,G) :: ith Target vector of generation G
#   F :: Scaling factor
#   r :: random selection
#
#   Type1 :: DE/rand/1       V_(i,G) = X_(r1,G) + F*(X_(r2,G) - X_(r3,G))
#   Type2 :: DE/best/2       V_(i,G) = X_(best,G) + F*(X_(r1,G) - X_(r2,G))
#   Type3 :: DE/current-to-best/1       V_(i,G) = X_(i,G) + F*(X_(best,G) - X_(i,G)) + F*(X_(r1,G) - X_(r2,G))
#   Type4 :: DE/rand/2       V_(i,G) = X_(r1,G) + F*(X_(r2,G) - X_(r3,G) + X_(r4,G) - X_(r5,G))
#   Type5 :: DE/best/2       V_(i,G) = X_(best,G) + F*(X_(r1,G) - X_(r2,G) + X_(r3,G) - X_(r4,G))

# import necessary libraries
import numpy as np

# import necessary modules
from fitness import fitness

# ======================================================================================================================
# ===== Helper functions ===============================================================================================
# ======================================================================================================================


def unique_rn_generator(low, high, n, excludee):
    """
    Function to generate a list of unique random integers

    This function uses numpy's random number generator to generate a list of random numbers, checks if all the numbers
    in the list are unique, if they are unique, the list is returned. If they are not unique, then the list is generated
    repeatedly until a list with unique numbers is generated.

    :param low: (int) lowest (inclusive) acceptable random number
    :param high: (int) highest (exclusive) acceptable random number
    :param n: (int) number of random numbers to be generated
    :param excludee: (int) number to be excluded from generated list of random numbers
    :return: (list) containing 'n' unique random numbers
    """
    r = np.random.randint(low, high, n)
    while (len(r) != len(set(r))) or (excludee in r):
        r = np.random.randint(low, high, n)
    return r


def add_lists(a, b):
    """
    Function to perform addition of two lists

    :param a: (list) first variable list of addition operation
    :param b: (list) first variable list of addition operation
    :return: (list) addition of a and b
    """
    return [i+j for i, j in zip(a, b)]


def sub_lists(a, b):
    """
    Function to perform subtraction of two lists

    :param a: (list) first variable list of subtraction operation
    :param b: (list) first variable list of subtraction operation
    :return: (list) subtraction of a and b
    """
    return [i-j for i, j in zip(a, b)]


def scalar_mul_list(s, a):
    """
    Function to multiply a scalar 's' to each element in list 'a'

    :param s: (float) scalar value to be multiplied
    :param a: (list) to which the scalar value is to be multiplied
    :return: (list) result after performing s*a
    """
    return [s*i for i in a]

# ======================================================================================================================
# ===== Mutation operators =============================================================================================
# ======================================================================================================================


def mutate_vectors_type1(population, F):
    """
    This function will implement the type 1 mutation vector (refer the comments above)

    Method and formulation:
        for each vector in target vector T, We have to select three unique and random vectors from the population in the
        target vector space. Then compute the mutated vector for T using the formula:
        V_(i,G) = X_(r1,G) + F*(X_(r2,G) - X_(r3,G))

    :param population: (list) of population containing (list) of candidate solution vectors
    :param F: (float) Scaling factor, a real and constant factor between [0, 2] which controls the amplification of the
              differential variation
    :return: (list) of mutated population containing (list) of mutated solution vectors
    """
    mutated_vectors = []
    for i in range(len(population)):
        # Select 3 unique random vectors from population, different from current vector
        r = unique_rn_generator(0, len(population), 3, i)
        X_r1 = population[r[0]]
        X_r2 = population[r[1]]
        X_r3 = population[r[2]]
        V_i = add_lists(X_r1, scalar_mul_list(F, sub_lists(X_r2, X_r3)))

        # NOTE: If you need to check if V_i satisfies the domain upper and lowerbounds, do it here.

        mutated_vectors.append(V_i)

    return mutated_vectors


def mutate_vectors_type2(population, F, mode):
    """
    This function will implement the type 2 mutation vector (refer the comments above)

    Method and formulation:
        first find the best vector from the population (choose according to best fitness value), then
        for each vector in target vector T, We have to select two unique and random vectors from the population in the
        target vector space. Then compute the mutated vector for T using the formula:
        V_(i,G) = X_(best,G) + F*(X_(r1,G) - X_(r2,G))

    :param population: (list) of population containing (list) of candidate solution vectors
    :param F: (float) Scaling factor, a real and constant factor between [0, 2] which controls the amplification of the
              differential variation
    :param mode: (string) to set whether working on minimization(pass: "min") or maximization(pass: "max") problem
    :return: (list) of mutated population containing (list) of mutated solution vectors
    """
    mutated_vectors = []

    # find the best(fittest) vector
    X_best = population[0]
    X_best_fitness = fitness(X_best)
    if mode == "max":
        for i in population:
            current_fitness = fitness(i)
            if current_fitness > X_best_fitness:
                X_best = i
                X_best_fitness = current_fitness
    elif mode == "min":
        for i in population:
            current_fitness = fitness(i)
            if current_fitness < X_best_fitness:
                X_best = i
                X_best_fitness = current_fitness

    for i in range(len(population)):
        # Select 2 unique random vectors from population, different from current vector
        r = unique_rn_generator(0, len(population), 2, i)
        X_r1 = population[r[0]]
        X_r2 = population[r[1]]
        V_i = add_lists(X_best, scalar_mul_list(F, sub_lists(X_r1, X_r2)))

        # NOTE: If you need to check if V_i satisfies the domain upper and lowerbounds, do it here.

        mutated_vectors.append(V_i)

    return mutated_vectors


def mutate_vectors_type3(population, F, mode):
    """
    This function will implement the type 3 mutation vector (refer the comments above)

    Method and formulation:
        first find the best vector from the population (choose according to best fitness value), then
        for each vector in target vector T, We have to select two unique and random vectors from the population in the
        target vector space. Then compute the mutated vector for T using the formula:
        V_(i,G) = X_(i,G) + F*(X_(best,G) - X_(i,G)) + F*(X_(r1,G) - X_(r2,G))

    :param population: (list) of population containing (list) of candidate solution vectors
    :param F: (float) Scaling factor, a real and constant factor between [0, 2] which controls the amplification of the
              differential variation
    :param mode: (string) to set whether working on minimization(pass: "min") or maximization(pass: "max") problem
    :return: (list) of mutated population containing (list) of mutated solution vectors
    """
    mutated_vectors = []

    # find the best(fittest) vector
    X_best = population[0]
    X_best_fitness = fitness(X_best)
    if mode == "max":
        for i in population:
            current_fitness = fitness(i)
            if current_fitness > X_best_fitness:
                X_best = i
                X_best_fitness = current_fitness
    elif mode == "min":
        for i in population:
            current_fitness = fitness(i)
            if current_fitness < X_best_fitness:
                X_best = i
                X_best_fitness = current_fitness

    for i in range(len(population)):
        # Select 2 unique random vectors from population, different from current vector
        r = unique_rn_generator(0, len(population), 2, i)
        X_r1 = population[r[0]]
        X_r2 = population[r[1]]
        V_i = add_lists(population[i], add_lists(scalar_mul_list(F, sub_lists(X_best, X_r1)),\
                                                 scalar_mul_list(F, sub_lists(X_r1, X_r2))))

        # NOTE: If you need to check if V_i satisfies the domain upper and lowerbounds, do it here.

        mutated_vectors.append(V_i)

    return mutated_vectors


def mutate_vectors_type4(population, F):
    """
    This function will implement the type 4 mutation vector (refer the comments above)

    Method and formulation:
        for each vector in target vector T, We have to select five unique and random vectors from the population in the
        target vector space. Then compute the mutated vector for T using the formula:
        V_(i,G) = X_(r1,G) + F*(X_(r2,G) - X_(r3,G) + X_(r4,G) - X_(r5,G))

    :param population: (list) of population containing (list) of candidate solution vectors
    :param F: (float) Scaling factor, a real and constant factor between [0, 2] which controls the amplification of the
              differential variation
    :return: (list) of mutated population containing (list) of mutated solution vectors
    """
    mutated_vectors = []
    for i in range(len(population)):
        # Select 5 unique random vectors from population, different from current vector
        r = unique_rn_generator(0, len(population), 5, i)
        X_r1 = population[r[0]]
        X_r2 = population[r[1]]
        X_r3 = population[r[2]]
        X_r4 = population[r[3]]
        X_r5 = population[r[4]]
        V_i = add_lists(X_r1, add_lists(scalar_mul_list(F, sub_lists(X_r2, X_r3)),\
                                                 scalar_mul_list(F, sub_lists(X_r4, X_r5))))

        # NOTE: If you need to check if V_i satisfies the domain upper and lowerbounds, do it here.

        mutated_vectors.append(V_i)

    return mutated_vectors


def mutate_vectors_type5(population, F, mode):
    """
    This function will implement the type 5 mutation vector (refer the comments above)

    Method and formulation:
        first find the best vector from the population (choose according to best fitness value), then
        for each vector in target vector T, We have to select four unique and random vectors from the population in the
        target vector space. Then compute the mutated vector for T using the formula:
        V_(i,G) = X_(best,G) + F*(X_(r1,G) - X_(r2,G) + X_(r3,G) - X_(r4,G))

    :param population: (list) of population containing (list) of candidate solution vectors
    :param F: (float) Scaling factor, a real and constant factor between [0, 2] which controls the amplification of the
              differential variation
    :param mode: (string) to set whether working on minimization(pass: "min") or maximization(pass: "max") problem
    :return: (list) of mutated population containing (list) of mutated solution vectors
    """
    mutated_vectors = []

    # find the best(fittest) vector
    X_best = population[0]
    X_best_fitness = fitness(X_best)
    if mode == "max":
        for i in population:
            current_fitness = fitness(i)
            if current_fitness > X_best_fitness:
                X_best = i
                X_best_fitness = current_fitness
    elif mode == "min":
        for i in population:
            current_fitness = fitness(i)
            if current_fitness < X_best_fitness:
                X_best = i
                X_best_fitness = current_fitness

    for i in range(len(population)):
        # Select 3 unique random vectors from population, different from current vector
        r = unique_rn_generator(0, len(population), 4, i)
        X_r1 = population[r[0]]
        X_r2 = population[r[1]]
        X_r3 = population[r[2]]
        X_r4 = population[r[3]]
        V_i = add_lists(X_best, add_lists(scalar_mul_list(F, sub_lists(X_r1, X_r2)),\
                                                 scalar_mul_list(F, sub_lists(X_r3, X_r4))))

        # NOTE: If you need to check if V_i satisfies the domain upper and lowerbounds, do it here.

        mutated_vectors.append(V_i)

    return mutated_vectors
