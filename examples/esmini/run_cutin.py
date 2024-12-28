import pymoo

from opensbt.model_ga.individual import IndividualSimulated
pymoo.core.individual.Individual = IndividualSimulated

from opensbt.model_ga.population import PopulationExtended
pymoo.core.population.Population = PopulationExtended

from opensbt.model_ga.result  import SimulationResult
pymoo.core.result.Result = SimulationResult

from opensbt.model_ga.problem import SimulationProblem
pymoo.core.problem.Problem = SimulationProblem

from opensbt.simulation.simulator import SimulationOutput
from opensbt.utils import geometric

from typing import Tuple
import numpy as np
import pymoo
from opensbt.algorithm.nsga2_optimizer import NsgaIIOptimizer

import logging as log
import os

from examples.esmini.esmini_simulation import EsminiSimulator
from opensbt.algorithm.ps_grid import PureSamplingGrid
from opensbt.config import LOG_FILE
from opensbt.evaluation.critical import CriticalAdasDistanceVelocity
from opensbt.evaluation.fitness import Fitness

from opensbt.experiment.search_configuration import DefaultSearchConfiguration
from opensbt.problem.adas_problem import ADASProblem
from opensbt.utils.log_utils import disable_pymoo_warnings, setup_logging
from opensbt.config import DEFAULT_CAR_LENGTH

os.chmod(os.getcwd(), 0o777)
logger = log.getLogger(__name__)
setup_logging(LOG_FILE)
disable_pymoo_warnings()

class FitnessMinDistanceVelocityExtended(Fitness):
    @property
    def min_or_max(self):
        return "min", "max"

    @property
    def name(self):
        return "Min distance", "Velocity at min distance"

    def eval(self, simout: SimulationOutput, **kwargs) -> Tuple[float]:
        if "adversary" in simout.location:
            name_adversary = "adversary"
        else:
            name_adversary = "other"

        traceEgo = simout.location["ego"]
        tracePed = simout.location[name_adversary]

        ind_min_dist = np.argmin(geometric.distPair(traceEgo, tracePed))

        # distance between ego and other object
        distance = np.min(geometric.distPair(traceEgo, tracePed))  - DEFAULT_CAR_LENGTH/2

        # speed of ego at time of the minimal distance
        speed = simout.speed["ego"][ind_min_dist]

        return (distance, speed)

problem = ADASProblem(
                      problem_name="My_Cut_In_Problem",
                      scenario_path=os.path.join(os.getcwd(), "examples", "esmini", "scenarios", "cutin", "alks_cut-in.xosc"),
                      simulation_variables=[                    # provide here the search variables
                          "EgoSpeed",
                          "TargetSpeed",
                          "LaneChangetime"
                      ],
                      xl=[30,20,1], # provide here the lower ranges for the search variables
                      xu=[40,30,10], # provide here the upper ranges for the search variables
                      fitness_function=FitnessMinDistanceVelocityExtended(), # we select an appropriate fitness function later
                      critical_function=CriticalAdasDistanceVelocity(), # we select an appropriate criticality function later
                      simulate_function=EsminiSimulator.simulate,
                      do_visualize=False
                      )
config = DefaultSearchConfiguration()
config.population_size = 2
config.n_generations = 2
optimizer = NsgaIIOptimizer(
                            problem=problem,
                            config=config)

res = optimizer.run()

res.write_results(params=optimizer.parameters)