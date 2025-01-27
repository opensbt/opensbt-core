import pymoo

from opensbt.model_ga.individual import IndividualSimulated
pymoo.core.individual.Individual = IndividualSimulated

from opensbt.model_ga.population import PopulationExtended
pymoo.core.population.Population = PopulationExtended

from opensbt.model_ga.result  import SimulationResult
pymoo.core.result.Result = SimulationResult

from opensbt.model_ga.problem import SimulationProblem
pymoo.core.problem.Problem = SimulationProblem

from opensbt.algorithm.ps_fps import PureSamplingFPS
from opensbt.algorithm.ps_grid import PureSamplingGrid
from opensbt.algorithm.ps_rand import PureSamplingRand
from opensbt.algorithm.nsga2_optimizer import *
from opensbt.algorithm.pso_optimizer import *
from opensbt.algorithm.algorithm import AlgorithmType
from opensbt.algorithm.nsga2dt_optimizer import NsgaIIDTOptimizer

import argparse
import logging as log
import os
import sys

from opensbt.experiment.experiment_store import experiments_store
from default_experiments import *
from opensbt.utils.log_utils import *
from opensbt.config import RESULTS_FOLDER, LOG_FILE

os.chmod(os.getcwd(), 0o777)

logger = log.getLogger(__name__)

setup_logging(LOG_FILE)

disable_pymoo_warnings()

results_folder = RESULTS_FOLDER

algorithm = None
problem = None
experiment = None

########

"""  This module is the entry point when running OpenSBT in the standalone mode. """

parser = argparse.ArgumentParser(description="Pass parameters for search. Pass -h for a list of all options.")
parser.add_argument('-e', dest='exp_number', type=str, action='store',
                    help='Name of default experiment to be used. (show all experiments via -info)].')
parser.add_argument('-i', dest='n_generations', type=int, default=None, action='store',
                    help='Number generations to perform.')
parser.add_argument('-n', dest='size_population', type=int, default=None, action='store',
                    help='The size of the initial population of scenario candidates.')
parser.add_argument('-a', dest='algorithm', type=int, default=None, action='store',
                    help='The algorithm to use for search. (Currently only 1: NSGAII supported.)')
parser.add_argument('-t', dest='maximal_execution_time', type=str, default=None, action='store',
                    help='The time to use for search.')
parser.add_argument('-f', dest='scenario_path', type=str, action='store',
                    help='The path to the scenario description file.')
parser.add_argument('-min', dest='var_min', nargs="+", type=float, action='store',
                    help='The lower bound of each search parameter.')
parser.add_argument('-max', dest='var_max', nargs="+", type=float, action='store',
                    help='The upper bound of each search parameter.')
parser.add_argument('-m', dest='design_names', nargs="+", type=str, action='store',
                    help='The names of the variables to modify.')
parser.add_argument('-o', dest='results_folder', type=str, action='store', default=RESULTS_FOLDER,
                    help='The name of the folder where the results of the search are stored (default: \\results\\)')
parser.add_argument('-v', dest='do_visualize', action='store_true',
                    help='Whether to use the simuator\'s visualization. This feature is useful for debugging and demonstrations, however it reduces the search performance.')
parser.add_argument('-info', dest='show_info', action='store_true',
                    help='Names of all defined experiments.')
parser.add_argument('-s', dest='seed', action='store', default=None, type=int,
                    help='Seed for randomized operations.')

args = parser.parse_args()

#######

if args.show_info:
    log.info("Experiments with the following names are defined:")
    store = experiments_store.get_store()
    for name in store.keys():
        log.info(name)
    
    sys.exit(0)

parser.add_argument('-list', dest='show_info', action='store_false',
                    help='List name of all defined experiments')

if args.exp_number and args.scenario_path:
    log.info("Flags set not correctly: Experiment file and example experiment cannot be set at the same time")
    sys.exit()
elif not (args.exp_number or args.scenario_path):
    log.info("Flags set not correctly: No file is provided or no example experiment selected.")
    sys.exit()

if args.exp_number:
    log.info(f"Selected experiment: {args.exp_number}")
    experiment = experiments_store.load(experiment_name=args.exp_number)
    config = experiment.search_configuration
    problem = experiment.problem
    algorithm = experiment.algorithm

elif (args.scenario_path):
    scenario_path = args.scenario_path
    var_min = []
    var_max = []
    #TODO create an ADASProblem from user input
    #TODO create an experiment from user input
    log.info("-- Experiment provided by file")

    if args.var_min is None:
        log.info("-- Minimal bounds for search are not set.")
        sys.exit()

    if args.var_max is None:
        log.info("-- Maximal bounds for search are not set.")
        sys.exit()

    log.info("Creating an experiment from user input not yet supported. Use default_experiments.py to create experiment")
    sys.exit()
else:
    log.info("-- No file provided and no experiment selected")
    sys.exit()

'''
override params if set by user
'''

if not args.size_population is None:
    config.population_size = args.size_population
if not args.n_generations is None:
    config.n_generations = args.n_generations
    config.inner_num_gen = args.n_generations #for NSGAII-DT
if not args.algorithm is None:
    algorithm = AlgorithmType(args.algorithm)
if not args.maximal_execution_time is None:
    config.maximal_execution_time = args.maximal_execution_time
if not args.var_max is None:
    problem.var_max = args.var_max
if not args.var_min is None:
    problem.var_min = args.var_min
if not args.design_names is None:
    problem.design_names = args.design_names
if not args.do_visualize is None:
    problem.do_visualize = args.do_visualize
if not args.seed is None:
    config.seed = args.seed

####### Run algorithm

if __name__ == "__main__":
    execTime = None
    opt = None
    if algorithm == AlgorithmType.NSGAII:
        log.info("Pymoo NSGA-II algorithm is used.")
        optimizer = NsgaIIOptimizer(
                              problem=problem,
                              config=config)
    elif algorithm == AlgorithmType.PSO:
        log.info("Pymoo PSO algorithm is used.")
        optimizer = PSOOptimizer(
                              problem=problem,
                              config=config)
    elif algorithm == AlgorithmType.PS_RAND:
        log.info("Random Sampling Algorithm is used.")
        optimizer = PureSamplingRand(
                              problem=problem,
                              config=config)
    elif algorithm == AlgorithmType.PS_GRID:
        log.info("Grid Sampling Algorithm is used.")
        optimizer = PureSamplingGrid(
                              problem=problem,
                              config=config)
    elif algorithm == AlgorithmType.PS_FPS:
        log.info("Furthes Point Sampling Algorithm is used.")
        optimizer = PureSamplingFPS(
                              problem=problem,
                              config=config)
    elif algorithm == AlgorithmType.NSGAII_DT:
        log.info("NSGAII_DT algorithm is used.")
        optimizer = NsgaIIDTOptimizer(
                              problem=problem,
                              config=config)
    else:
        raise ValueError("Error: No algorithm with the given code: " + str(algorithm))

    res = optimizer.run()
    res.write_results(results_folder=results_folder, 
                      params = optimizer.parameters,
                      save_folder = optimizer.save_folder)

    log.info("====== Algorithm search time: " + str("%.2f" % res.exec_time) + " sec")
