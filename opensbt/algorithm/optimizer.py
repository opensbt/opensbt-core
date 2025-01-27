import os

from abc import ABC, abstractclassmethod, abstractmethod
from typing import Dict

from opensbt.experiment.search_configuration import SearchConfiguration
from opensbt.model_ga.problem import SimulationProblem
from opensbt.model_ga.result import SimulationResult
from pymoo.optimize import minimize
from pymoo.core.problem import Problem  
from pymoo.core.algorithm import Algorithm

import dill
from opensbt.config import RESULTS_FOLDER, EXPERIMENTAL_MODE, BACKUP_ITERATIONS
from opensbt.visualization.visualizer import create_save_folder, backup_object

class Optimizer(ABC):
    """ Base class for all optimizers in OpenSBT.  Subclasses need to   
        implement the __init__ method. The run method has to be overriden when non pymoo implemented algorithms are used.
        For reference consider the implementation of the NSGA-II-DT optimizer in opensbt/algorithm/nsga2dt_optimizer.py
    """
    
    algorithm_name: str
    parameters: Dict
    config: SearchConfiguration
    problem: Problem
    algorithm: Algorithm
    termination: object
    save_history: bool
    
    parameters: str

    save_folder: str
    
    @abstractmethod
    def __init__(self, problem: SimulationProblem, config: SearchConfiguration):
        """Initialize here the Optimization algorithm to be used for search-based testing.

        :param problem: The testing problem to be solved.
        :type problem: SimulationProblem
        :param config: The configuration for the search.
        :type config: SearchConfiguration
        """
        pass

    def run(self) -> SimulationResult:
        # create a backup during the search for each generation
        algorithm = self.algorithm
        algorithm.setup(problem = self.problem, 
                        termination = self.termination,
                        save_history = self.save_history)
        save_folder = create_save_folder(self.problem, 
                                RESULTS_FOLDER,
                                algorithm_name=self.algorithm_name,
                                is_experimental=EXPERIMENTAL_MODE)

        while(algorithm.termination.do_continue()):
            algorithm.next()
            if BACKUP_ITERATIONS:
                n_iter = algorithm.n_iter - 1
                backup_object(algorithm, 
                              save_folder, 
                              name = f"algorithm_iteration_{n_iter}")

        res = algorithm.result()
        self.save_folder = save_folder
        return res
