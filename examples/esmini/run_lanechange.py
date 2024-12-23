from typing import Tuple
import numpy as np
import pymoo

from opensbt.model_ga.individual import IndividualSimulated
from opensbt.simulation.simulator import SimulationOutput
from opensbt.utils import geometric
pymoo.core.individual.Individual = IndividualSimulated

from opensbt.model_ga.population import PopulationExtended
pymoo.core.population.Population = PopulationExtended

from opensbt.model_ga.result  import SimulationResult
pymoo.core.result.Result = SimulationResult

from opensbt.model_ga.problem import SimulationProblem
pymoo.core.problem.Problem = SimulationProblem

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
                        problem_name="EsminiLaneChange",
                        scenario_path=os.getcwd() + "/examples/esmini/scenarios/lanechange/lanechange_scenario.xosc",
                        xl=[20, 20, 55],
                        xu=[25, 30, 80],
                        simulation_variables=[
                            "EgoTargetSpeed",
                            "SpeedLaneChange",
                            "RPrecederStartS"],
                        fitness_function=FitnessMinDistanceVelocityExtended(),  
                        critical_function=CriticalAdasDistanceVelocity(),
                        simulate_function=EsminiSimulator.simulate,
                        simulation_time=10,
                        sampling_time=100,
                        approx_eval_time=10,
                        do_visualize=True
                        )

config = DefaultSearchConfiguration()
config.population_size = 5
optimizer = PureSamplingGrid(
                            problem=problem,
                            config=config)

res = optimizer.run()

res.write_results(params=optimizer.parameters)