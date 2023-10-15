#!/bin/bash

export OPENSBT_CORE_PATH=/home/sorokin/Projects/testing/search-based-test-case-generation
export OPENSBT_RUNNER_PATH=/home/sorokin/Projects/testing/ff1_carla
export ROSCO_PATH=/home/sorokin/Projects/testing/rosco
export SHARE_PATH=/home/sorokin/Projects/testing/rosco/share
export CARLA_PATH=/home/sorokin/Carla
export SCENARIORUNNER_PATH=/home/sorokin/scenario_runner
export PYTHONPATH=/home/sorokin/CARLA/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg:/home/sorokin/CARLA/PythonAPI/carla/agents:/home/sorokin/CARLA/PythonAPI/carla:/home/sorokin/scenario_runner

sudo docker stop $(sudo docker ps -aq --filter="name=carla-client")
sudo docker stop $(sudo docker ps -aq --filter="name=carla-server")

python run.py -e 1 -i 1 -n 10

sudo docker stop $(sudo docker ps -aq --filter="name=carla-client")
sudo docker stop $(sudo docker ps -aq --filter="name=carla-server")
