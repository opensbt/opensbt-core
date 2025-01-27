import os
from opensbt.evaluation.fitness import *
from opensbt.experiment.search_configuration import DefaultSearchConfiguration
from opensbt.problem.adas_problem import ADASProblem
from opensbt.problem.pymoo_test_problem import PymooTestProblem
from opensbt.experiment.experiment_store import *
from opensbt.algorithm.algorithm import *
from opensbt.evaluation.critical import *
#########################################
### Carla Examples,  ego speed is in km/h
##################################

def getExp1() -> Experiment:
    from examples.carla.carla_simulation import CarlaSimulator
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
    experiment = Experiment(name="1",
                            problem=problem,
                            algorithm=AlgorithmType.NSGAII,
                            search_configuration=DefaultSearchConfiguration())
    return experiment

experiments_store.register(getExp1())

def getExp1a() -> Experiment:
    from examples.carla.carla_simulation import CarlaSimulator
    problem = ADASProblem(
                          problem_name="PedestrianCrossingStartWalk",
                          scenario_path=os.getcwd() + "/examples/carla/scenarios/PedestrianCrossing.xosc",
                          xl=[0.5, 1, 0],
                          xu=[3, 22, 60],
                          simulation_variables=[
                              "PedSpeed",
                              "EgoSpeed",
                              "PedDist"],
                          fitness_function=FitnessMinTTCVelocity(),           # ONLY CHANGE - use TTC instead distance
                          critical_function=CriticalAdasTTCVelocity(),
                          simulate_function=CarlaSimulator.simulate,
                          simulation_time=10,
                          sampling_time=100,
                          approx_eval_time=10,
                          do_visualize = True
                          )
    experiment = Experiment(name="1a",
                            problem=problem,
                            algorithm=AlgorithmType.NSGAII,
                            search_configuration=DefaultSearchConfiguration())
    return experiment

experiments_store.register(getExp1a())

def getExp3() -> Experiment:
    from examples.carla.carla_simulation import CarlaSimulator
    problem = ADASProblem(
                          problem_name="TwoPedestriansCrossing",
                          scenario_path=os.getcwd() + "/examples/carla/scenarios/PedestrianCrossingSecond.xosc",
                          xl=[0.5, 1, 0],
                          xu=[3, 80, 60],
                          simulation_variables=[
                              "PedestrianSpeed",
                              "FinalHostSpeed",
                              "PedestrianEgoDistanceStartWalk"],
                          fitness_function=FitnessMinDistanceVelocityFrontOnly(),  
                          critical_function=CriticalAdasFrontCollisions(),
                          simulate_function=CarlaSimulator.simulate,
                          simulation_time=10,
                          sampling_time=100,
                          approx_eval_time=10,
                          do_visualize=True
                          )
    config = DefaultSearchConfiguration()
    experiment = Experiment(name="3",
                            problem=problem,
                            algorithm=AlgorithmType.NSGAII,
                            search_configuration=config)

    return experiment
    
experiments_store.register(getExp3())

#########################################
### Mathematical Test Problems
##################################
'''
    BNH Problem

    Pareto solutions:
    x∗1=x∗2∈[0,3]  and x∗1∈[3,5], x∗2=3
'''

def getExp2() -> Experiment:
    problem = PymooTestProblem(
        'BNH',
        critical_function=CriticalBnhDivided())

    config = DefaultSearchConfiguration()
    # config.maximal_execution_time = "00:00:01"
    config.n_generations = 10
    config.population_size = 10
    config.inner_num_gen = 5
    experiment = Experiment(name="2",
                            problem=problem,
                            algorithm=AlgorithmType.NSGAII_DT,
                            search_configuration=config)

    return experiment

experiments_store.register(getExp2())

'''
Rastrigin SOO problem (n_var = 2, n_obj = 1), test for PSO
'''
def getExp4() -> Experiment:
    problem = PymooTestProblem(
        'rastrigin',
        critical_function=CriticalRastrigin())

    config = DefaultSearchConfiguration()
    # config.maximal_execution_time = "00:00:01"
    config.population_size = 10
    config.n_generations = 10
    experiment = Experiment(name="4",
                            problem=problem,
                            algorithm=AlgorithmType.PSO,
                            search_configuration=config)

    return experiment
experiments_store.register(getExp4())

'''
Random Sampling for BNH Problem
'''
def getExp99() -> Experiment:
    problem = PymooTestProblem(
            'BNH',
            critical_function=CriticalBnhDivided())

    config = DefaultSearchConfiguration()
    config.population_size = 10   # defines the number of samples for a single axis
    experiment = Experiment(name="99",
                            problem=problem,
                            algorithm=AlgorithmType.PS_RAND,
                            search_configuration=config)

    return experiment  
experiments_store.register(getExp99())

#########################################
### Dummy Simulation Problems (Toy Example)
##################################

''' Dummy Simulation with planar motion planning and simplified AEB
'''

def getExp5() -> Experiment:
    from opensbt.simulation.dummy_simulation import DummySimulator

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
                          fitness_function=FitnessMinDistanceVelocity(),
                          critical_function=CriticalAdasDistanceVelocity(),
                          simulate_function=DummySimulator.simulate,
                          simulation_time=10,
                          sampling_time=0.25
                          )
    config = DefaultSearchConfiguration()
    config.population_size = 20
    config.n_generations = 50
    experiment = Experiment(name="5",
                            problem=problem,
                            algorithm=AlgorithmType.NSGAII,
                            search_configuration=config)
    return experiment
experiments_store.register(getExp5())

''' Dummy Simulation with planar motion planning and simplified AEB
'''

def getExp6() -> Experiment:
    from opensbt.simulation.dummy_simulation import DummySimulator

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
    config.n_generations = 10
    config.inner_num_gen = 5
    experiment = Experiment(name="6",
                            problem=problem,
                            algorithm=AlgorithmType.NSGAII_DT,
                            search_configuration=config)
    return experiment
experiments_store.register(getExp6())
