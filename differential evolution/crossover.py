# DE employs uniform crossover to build/generate trial vectors, by mixing the mutant vectors and target vectors
# according to a selected probability distribution

# Two types of crossovers:

# [1] Binomial/uniform crossover: Uniform crossover is a process in which independent random trials determine the source
#   for each trial parameter. Crossover is uniform in the sense that each parameter, regardless of its location in the
#   trial vector, has the same probability of inheriting its value from a given vector.
#   Method:  DE’s version of uniform crossover begins by taking a randomly chosen parameter from the mutant so that the
#   trial vector will not replicate the target vector. Then, comparing CR to random R determines the source for each
#   remaining trial parameter. If R ≤ Cr , then the parameter comes from the mutant, otherwise, the target is the source

# [2] Exponential crossover: DE’s exponential crossover works by choosing one parameter randomly and copying from the
#   mutant to the corresponding trial vector so that the trial vector will be different from the vector with which it
#   will be compared. The source of subsequent trial parameters is determined by comparing CR to a uniformly distributed
#   random number R that is generated anew for each parameter. As long as R ≤ CR , parameters continue to be taken from
#   the mutant vector, but the first time that R > Cr , the current and all remaining parameters are taken from the
#   target vector.

# import necessary libraries
import numpy as np


# import necessary modules

# ======================================================================================================================
# ===== Helper functions ===============================================================================================
# ======================================================================================================================


# ======================================================================================================================
# ===== Crossover operators ============================================================================================
# ======================================================================================================================


def binomial_crossover(target_vec, mutant_vec, CR):
    """
    This function is the implementation of binomial crossover algorithm of Differential Evolution

    DE’s version of uniform crossover begins by taking a randomly chosen parameter from the mutant so that the
    trial vector will not replicate the target vector. Then, comparing CR to random R determines the source for each
    remaining trial parameter. If R ≤ Cr , then the parameter comes from the mutant, otherwise, the target is the source

    :param target_vec: (list of list) containing all target vectors
    :param mutant_vec: (list of list) containing all mutant vectors
    :param CR: (float) Crossover rate, should be between (0, 1)
    :return: (list of list) containing all trial vectors
    """

    tv = target_vec
    mv = mutant_vec

    trial_vec = []

    for i in range(len(tv)):
        # randomly choose from the mutant so that the trial vector will not replicate the target vector.
        trial_vec_i = []
        r = np.random.randint(0, len(tv[i]))
        print(r, len(tv), len(tv[i]))
        trial_vec_i.append(mv[i].pop(r))
        del tv[i][r]
        # now select other trial vectors
        for j in range(len(tv[i])):
            r = np.random.uniform(0, 1)
            if r <= CR:
                trial_vec_i.append(mv[i][j])
            elif r > CR:
                trial_vec_i.append(tv[i][j])
        trial_vec.append(trial_vec_i)

    return trial_vec
