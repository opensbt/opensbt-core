# Copyright (c) 2022 fortiss GmbH
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import sys

import os
import time
import multiprocessing as mp

import carla
import docker
import matplotlib.pyplot as plt

from carla_simulation.runner import Runner

from carla_simulation.metrics.raw import RawData
from carla_simulation.controllers.npc import NpcAgent


NETWORK_NAME = 'carla-network'

def run_scenarios(scenario_dir, visualization_flag=False):
    client = docker.from_env()
    network = client.networks.get(NETWORK_NAME)
    servers = [
        container.attrs[
            'NetworkSettings'
        ][
            'Networks'
        ][
            NETWORK_NAME
        ][
            'IPAddress'
        ]
        for container in network.containers
    ]

    scenario_map = 'Town01'
    for server in servers:
        client = carla.Client(server, 2000)
        server_map = client.get_world().get_map().name.split('/')[-1]
        if server_map != scenario_map:
            client.load_world(scenario_map)

    scenarios = mp.JoinableQueue()
    with os.scandir(scenario_dir) as entries:
        for entry in entries:
            if entry.name.endswith('.xosc') and entry.is_file():
                scenarios.put(entry.name)

    with mp.Manager() as manager:
        start_time = time.time()

        evaluations = manager.list()
        for server in servers:
            runner = Runner(
                server,
                NpcAgent,
                RawData,
                visualization_flag
            )
            mp.Process(
                target=runner.run,
                args=(scenario_dir, scenarios, evaluations),
                daemon = True
            ).start()

        scenarios.join()

        stop_time = time.time()

        print('Time: {}s'.format(stop_time - start_time))

        return list(evaluations)
