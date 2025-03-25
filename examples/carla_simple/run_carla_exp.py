import sys
import os
sys.path.insert(0, os.getcwd() +  "/examples/carla_simple/carla_runner/src")

import pymoo

from opensbt.model_ga.individual import IndividualSimulated
pymoo.core.individual.Individual = IndividualSimulated

from opensbt.model_ga.population import PopulationExtended
pymoo.core.population.Population = PopulationExtended

from opensbt.model_ga.result  import SimulationResult
pymoo.core.result.Result = SimulationResult

from opensbt.model_ga.problem import SimulationProblem
pymoo.core.problem.Problem = SimulationProblem

from opensbt.algorithm.nsga2_optimizer import *
from opensbt.algorithm.pso_optimizer import *

import logging as log
import os

from opensbt.experiment.experiment_store import experiments_store
from default_experiments import *
from opensbt.utils.log_utils import *
from opensbt.config import RESULTS_FOLDER, LOG_FILE

os.chmod(os.getcwd(), 0o777)

logger = log.getLogger(__name__)

setup_logging(LOG_FILE)

disable_pymoo_warnings()

import os
from opensbt.algorithm.nsga2_optimizer import NsgaIIOptimizer
from opensbt.evaluation.fitness import *
from opensbt.problem.adas_problem import ADASProblem
from opensbt.problem.pymoo_test_problem import PymooTestProblem
from opensbt.experiment.experiment_store import *
from opensbt.algorithm.algorithm import *
from opensbt.evaluation.critical import *

#########################################
### Carla Examples,  ego speed is in km/h
##################################

from examples.carla_simple.carla_simulation import CarlaSimulator

problem = ADASProblem(
                        problem_name="PedestrianCrossingStartWalk",
                        scenario_path=os.getcwd() + "/examples/carla/scenarios/PedestrianCrossing.xosc",
                        xl=[0.5, 1, 0],
                        xu=[3, 22, 60],
                        simulation_variables=[
                            "PedSpeed",
                            "EgoSpeed",
                            "PedDist"],
                        fitness_function=FitnessMinDistanceVelocity(),  
                        critical_function=CriticalAdasDistanceVelocity(),
                        simulate_function=CarlaSimulator.simulate,
                        simulation_time=10,
                        sampling_time=100,
                        approx_eval_time=10,
                        do_visualize = True
                        )

config=DefaultSearchConfiguration()

config.population_size = 2
config.n_generations = 2

optimizer = NsgaIIOptimizer(
            problem=problem,
            config=config)

res = optimizer.run()

res.write_results(results_folder=RESULTS_FOLDER, params = optimizer.parameters)

log.info("====== Algorithm search time: " + str("%.2f" % res.exec_time) + " sec")
