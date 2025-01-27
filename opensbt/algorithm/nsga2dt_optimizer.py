from opensbt.config import BACKUP_ITERATIONS
from opensbt.model_ga.result  import SimulationResult
from opensbt.evaluation.critical import Critical
from opensbt.utils.operators import select_operator
from pymoo.termination import get_termination
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.core.population import Population
from pymoo.core.problem import Problem
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.lhs import LHS
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from pymoo.core.problem import Problem
from opensbt.exception.configuration import RestrictiveConfigException
from opensbt.utils.archive import MemoryArchive
from opensbt.utils.time_utils import convert_pymoo_time_to_seconds
from pymoo.core.population import Population
from opensbt.visualization.configuration import *
from opensbt.algorithm.classification.decision_tree import decision_tree
from opensbt.utils.evaluation import evaluate_individuals
from opensbt.utils.sorting import *
from opensbt.utils.time_utils import convert_pymoo_time_to_seconds
from opensbt.visualization.configuration import *
from opensbt.experiment.search_configuration import SearchConfiguration
from opensbt.model_ga.result import *
import logging as log
from opensbt.algorithm.optimizer import Optimizer
from opensbt.visualization.visualizer import backup_object, create_save_folder
import copy
import sys
import time
import os
import random

class NsgaIIDTOptimizer(Optimizer):
    """ 
        This optimizer implements the NSGA-II-DT algorithm from [1] which is based on the NSGA-II algorithm 
        but is employing ML models, i.e. decision trees to guide the search for failures. 

        [1] Raja Ben Abdessalem, Shiva Nejati, Lionel C. Briand, and Thomas Stifter. 2018. 
        Testing vision-based control systems using learnable evolutionary algorithms. 
        In Proceedings of the 40th International Conference on Software Engineering (ICSE '18). 
        Association for Computing Machinery, New York, NY, USA, 1016–1026. 
        https://doi.org/10.1145/3180155.3180160
    """
    
    algorithm_name = "NSGA-II-DT" 

    def __init__(self,
                 problem: Problem,
                 config: SearchConfiguration):
        """Initializes the NSGA-II-DT Optimizer

        :param problem: The testing problem.
        :type problem: Problem
        :param config: The configuraiton for the search.
        :type config: SearchConfiguration
        """

        self.problem = problem
        self.config = config
        self.res = None

        log.info(f"Initialized algorithm with config: {config.__dict__}")
        
    def run(self) -> SimulationResult:
        """_summary_

        :return: Return a SimulationResults object which holds all information from the simulation.
        :rtype: SimulationResult
        """
        problem = self.problem
        config = self.config

        population_size = config.population_size
        maximal_execution_time = config.maximal_execution_time
        max_tree_iterations = config.max_tree_iterations
        num_offsprings = config.num_offsprings
        prob_crossover = config.prob_crossover
        eta_crossover = config.eta_crossover
        prob_mutation = config.prob_mutation
        eta_mutation = config.eta_mutation
        inner_num_gen = config.inner_num_gen

        '''Output variables'''
        all_population = Population()
        best_population = Population()
        best_population_unranked = Population()

        '''Initial conditions (initial region)'''
        xl = problem.xl
        xu = problem.xu
        
        random.seed(config.seed)

        # sampling = FloatRandomSampling()
        sampling = LHS()  # Latin Hypercube Sampling
        initial_population = sampling(problem, population_size)
        hist_holder = []

        '''Parameters of the algorithm'''
        if prob_mutation is None:
            prob_mutation = 1 / problem.n_var

        '''Parameter for evaluation'''
        if maximal_execution_time is not None:
            _maximal_execution_time = convert_pymoo_time_to_seconds(
                maximal_execution_time)
            max_tree_iterations = sys.maxsize
            log.info("Search is constrained by maximal execution time")
        elif max_tree_iterations is not None:
            _maximal_execution_time = sys.maxsize
            log.info("Search is constrained by maximal number of tree generations")
        else:
            log.info("Parameters are not correctly set, cannot start search.")
            sys.exit()
        ''' For backup '''
        save_folder = create_save_folder(self.problem, 
                                RESULTS_FOLDER,
                                algorithm_name=self.algorithm_name,
                                is_experimental=EXPERIMENTAL_MODE)

        ''' Computation start '''
        start_time = time.time()

        evaluate_individuals(initial_population, problem)

        initial_region = decision_tree.Region(xl, xu, initial_population)
        critical_regions = [initial_region]   
        hist_holder = []

        # inner_algorithm is a template for an algorithm object that is stored for every generation
        inner_algorithm = NSGA2(
            pop_size=None,
            n_offsprings=None,
            sampling = select_operator("init", config),
            crossover = select_operator( "cx", config, **{"eta" : eta_crossover, "prob" : prob_crossover}),
            mutation = select_operator( "mut", config, **{"eta" : eta_mutation, "prob" : prob_mutation}),
            eliminate_duplicates = select_operator( "dup", config),
            archive=MemoryArchive()
        )

        tree_iteration = 0
        n_func_evals = 0
        while n_func_evals < config.n_func_evals_lim:
            # extend the history by one generation
            hist_holder.extend([inner_algorithm] * inner_num_gen)

            log.info(f"running iteration {tree_iteration}")
            for critical_region in critical_regions:
                    
                sub_problem = problem

                if prob_mutation == None:
                    prob_mutation = 1 / problem.n_var

                nd_individuals_region = calc_nondominated_individuals(critical_region.population)
                initial_population = Population(
                    individuals=nd_individuals_region)
                pop_size = len(initial_population)

                algorithm = NSGA2(
                    pop_size=pop_size,
                    n_offsprings=num_offsprings,
                    sampling=initial_population,
                    crossover = select_operator( "cx", config, **{"eta" : eta_crossover, "prob" : prob_crossover}),
                    mutation = select_operator( "mut", config, **{"eta" : eta_mutation, "prob" : prob_mutation}),
                    eliminate_duplicates = select_operator( "dup", config),
                    archive=MemoryArchive()
                 )
                print(select_operator("mut", config))

                termination = get_termination("n_gen", inner_num_gen)

                res = minimize(sub_problem,
                               algorithm,
                               termination,
                               seed=config.seed,
                               save_history=True,
                               verbose=True)

                n_func_evals += res.history[-1].evaluator.n_eval

                self._update_history(res, hist_holder, tree_iteration, inner_num_gen, inner_algorithm)

                hist = res.history

                # hist[i] is an object of <class 'pymoo.algorithms.moo.nsga2.NSGA2'>
                best_population_unranked = Population.merge(
                    best_population, res.opt)
                best_population = get_nondominated_population(
                    best_population_unranked)
                for generation in hist:
                    all_population = Population.merge(
                        all_population, generation.pop)

            initial_region.population = best_population

            regions = decision_tree.generate_critical_regions(
                all_population, problem, save_folder=None)
            critical_regions = [
                region for region in regions if region.is_critical]
            if not critical_regions:
                critical_regions = [initial_region]
            tree_iteration += 1

            if BACKUP_ITERATIONS:
                result = self._create_result(problem, hist_holder, inner_algorithm, -1)
                n_iter = tree_iteration
                backup_object(result, 
                                save_folder, 
                                name = f"result_iteration_{n_iter}")

        execution_time = time.time() - start_time

        '''For forwarding to plotter'''
        self.parameters = {
            'Number of maximal tree generations': str(config.max_tree_iterations),
            'Number performed tree iterations': str(tree_iteration),
            "Population size": str(config.population_size),
            "Number of generations": str(config.inner_num_gen),
            "Number of offsprings": str(config.num_offsprings),
            "Crossover probability": str(config.prob_crossover),
            "Crossover eta": str(config.eta_crossover),
            "Mutation probability": str(config.prob_mutation),
            "Mutation eta": str(config.eta_mutation),
            "Seed" : str(config.seed)
        }
        
        result = self._create_result(problem, hist_holder, inner_algorithm, execution_time, save_folder)
        self.res = result
        return result

    def _update_history(self, res, hist_holder, tree_iteration, inner_num_gen, inner_algorithm):
        for i in range(inner_num_gen):
            pop = Population.merge(
                hist_holder[tree_iteration * inner_num_gen + i].pop, res.history[i].pop)
            # copy a template of the inner algorithm, and then modify its population and other properties
            algo = copy.deepcopy(inner_algorithm)
            algo.pop = pop
            opt_pop = Population(
                individuals=calc_nondominated_individuals(pop))
            algo.opt = opt_pop
            hist_holder[tree_iteration * inner_num_gen + i] = algo

    def _create_result(self, problem, hist_holder, inner_algorithm, execution_time, save_folder = None):
        I = 0
        for algo in hist_holder:
            I += len(algo.pop)
            algo.evaluator.n_eval = I
            algo.start_time = 0
            algo.problem = problem
            algo.result()

        res_holder = SimulationResult()
        res_holder.algorithm = inner_algorithm
        res_holder.algorithm.evaluator.n_eval = I
        res_holder.problem = problem
        res_holder.algorithm.problem = problem
        res_holder.history = hist_holder
        res_holder.exec_time = execution_time

        # calculate total optimal population using individuals from all iterations
        opt_all = Population()
        for algo in hist_holder:
            opt_all = Population.merge(opt_all, algo.pop)
        # log.info(f"opt_all: {opt_all}")
        opt_all_nds = get_nondominated_population(opt_all)
        res_holder.opt = opt_all_nds
        res_holder.save_folder = save_folder
        res_holder.archive = opt_all  # for now the same all pops together

        return res_holder