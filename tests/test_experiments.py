import os
from pathlib import Path
import pymoo
import time

from opensbt.model_ga.individual import IndividualSimulated
from tests import test_base
pymoo.core.individual.Individual = IndividualSimulated

from opensbt.model_ga.population import PopulationExtended
pymoo.core.population.Population = PopulationExtended

from opensbt.model_ga.result  import SimulationResult
pymoo.core.result.Result = SimulationResult

from opensbt.model_ga.problem import SimulationProblem
pymoo.core.problem.Problem = SimulationProblem

from opensbt.algorithm.nsga2_optimizer import NsgaIIOptimizer
from opensbt.evaluation.critical import CriticalAdasDistanceVelocity
from opensbt.experiment.search_configuration import DefaultSearchConfiguration
from opensbt.evaluation.fitness import FitnessMinDistanceVelocityFrontOnly
from opensbt.problem.adas_problem import ADASProblem

class TestExperiments():
    WAIT_RESULTS_TIME = 10

    @staticmethod
    def results_correctly_written(result, results_path):
        req_folders = ["simout", "backup",
                "gif", "trace_comparison", 
                "design_space", "objective_space", "classification"]

        for folder in req_folders:
            if not os.path.isdir(results_path + folder):
                print(f"tocheck: {results_path + folder}")
                return False
        return True
        
    @staticmethod
    def test_dummy_experiment():
        test_base.configure_logging_and_env()

        from opensbt.simulation.dummy_simulation import DummySimulator
        
        results_folder = '/results/'
 
        problem = ADASProblem(
                            problem_name="DummySimulatorProblem",
                            scenario_path="./dummy_scenario",
                            xl=[0, 1, 0, 1],
                            xu=[360, 3,360, 3],
                            simulation_variables=[
                                "orientation_ego",
                                "velocity_ego",
                                "orientation_ped",
                                "velocity_ped"],
                            fitness_function=FitnessMinDistanceVelocityFrontOnly(),
                            critical_function=CriticalAdasDistanceVelocity(),
                            simulate_function=DummySimulator.simulate,
                            simulation_time=10,
                            sampling_time=0.25
                          )
        config = DefaultSearchConfiguration()
        config.population_size = 10
        config.n_generations = 20

        print("pymoo NSGA-II algorithm is used.")
        
        algo = NsgaIIOptimizer(
                              problem=problem,
                              config=config)
        res = algo.run()        
        res.write_results(results_folder=results_folder,
                        params = algo.parameters,
                        save_folder = algo.save_folder)

        exp_folder = os.getcwd() + results_folder + os.sep + problem.problem_name + os.sep  + \
                             algo.algorithm_name + os.sep
                             
        paths = sorted(Path(exp_folder).iterdir(), key=os.path.getmtime)
        
        results_path = str(paths[-1]) + os.sep

        time.sleep(TestExperiments.WAIT_RESULTS_TIME)
        
        assert TestExperiments.results_correctly_written(results_path=results_path)

