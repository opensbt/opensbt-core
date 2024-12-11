import numpy as np
from opensbt.evaluation.fitness import *
import logging as log
import sys
import random
from os.path import join
from pathlib import Path
# For Python 3.6 we use the base keras
from mnist.digit_mutator import DigitMutator
# local imports
from mnist import vectorization_tools
from mnist.digit_input import Digit
from mnist.exploration import Exploration
from opensbt.model_ga.population import PopulationExtended
from mnist.config import NGEN, \
    POPSIZE, EXPECTED_LABEL, INITIALPOP, \
    ORIGINAL_SEEDS, BITMAP_THRESHOLD, FEATURES
from math import ceil
import string
from numbers import Real
import random
import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.sampling import Sampling
from pymoo.core.crossover import Crossover
from pymoo.core.mutation import Mutation
import string
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from pymoo.core.duplicate import ElementwiseDuplicateElimination
from pymoo.core.crossover import Crossover
from pymoo.core.variable import Real, get
from pymoo.util.misc import row_at_least_once_true
from pymoo.core.crossover import Crossover
from pymoo.core.population import Population
from pymoo.util.misc import crossover_mask
from mnist.mnist_problem import MNISTProblem
from fmnist import fmnist_simulation
from mnist import mutations
from pymoo.operators.sampling.rnd import random_by_bounds

class FMnistSamplingValid(Sampling):

    def _do(self, problem, n_samples, **kwargs):

        X = np.empty((n_samples, len(problem.xu)))
        
        seed_pure= problem.seed_digits[0]
    
        for i in range(0,n_samples):
            while True:
                cand = random_by_bounds(n_var=problem.n_var,
                                n_samples=1,
                                xl=problem.xl,
                                xu=problem.xu)[0]
                # print(f"created candidate: {cand}")
                
                if problem.n_var == 3:
                    digit_mutated = self._generate_digit_mutated(problem,
                                    digit=seed_pure,
                                    extent_1=cand[0],
                                    extent_2=cand[1],
                                    c_index=cand[2])
                elif problem.n_var == 6:
                    digit_mutated = self._generate_digit_mutated_bi(problem, 
                            seed_pure, 
                            cand[0], 
                            cand[1], 
                            cand[2],
                            cand[3],
                            cand[4],
                            cand[5])
                else:
                    print("Problem instance not supported. N vars is not supported.")
                    sys.exit()

                if digit_mutated.distance(seed_pure) <= problem.max_seed_distance:
                    break
                else:
                    print("Digit invalid. Resampling...")
            X[i] = np.asarray(cand)
        # print(f"constructed initial population: {X}")

        return X

    def _generate_digit_mutated(self, 
            problem: MNISTProblem, 
            digit, 
            extent_1, 
            extent_2, 
            c_index):
        print("Generating new digit by mutation.")
        new_digit = digit.clone()
        new_digit = mutations.apply_mutation_index(problem,
                                                          new_digit,
                                                            extent_1=extent_1,
                                                            extent_2=extent_2,
                                                            index=c_index)

        return new_digit

    def _generate_digit_mutated_bi(self, 
            problem: MNISTProblem, 
            digit, 
            extent_1, 
            extent_2, 
            extent_3,
            extent_4,
            c_index_1,
            c_index_2):
        print("Generating new digit by mutation.")
        new_digit = digit.clone()
        new_digit = mutations.apply_mutation_index_bi(
                            problem,
                            new_digit,
                            extent_1=extent_1,
                            extent_2=extent_2,
                            extent_3=extent_3,
                            extent_4=extent_4,
                            index_1=c_index_1,
                            index_2=c_index_2
                        )

        return new_digit