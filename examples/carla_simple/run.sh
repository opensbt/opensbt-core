# we need to create recordings directory and give full rights
mkdir -p tmp/recordings 
current_perms=$(stat -c "%a" tmp/recordings)
if [ "$current_perms" -ne 777 ]; then
    sudo chmod 777 -R tmp/recordings
fi

# REPLACE THE PATHS WITH THE ACTUAL PATHS IN YOUR SYSTEM
export CARLA_ROOT=~/CARLA_0.9.13
export SCENARIO_RUNNER_ROOT=/home/lev/Documents/aw/scenario_runner

export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI
export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla/agents
export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla/dist/carla-0.9.13-py3.7-linux-x86_64.egg
export PYTHONPATH=$PYTHONPATH:$SCENARIO_RUNNER_ROOT

# run experiment
python -m examples.carla_simple.run_carla_exp