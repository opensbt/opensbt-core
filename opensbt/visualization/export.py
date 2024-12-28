import os
from extract.create_scenario_simout import extract_xosc
from opensbt.utils.duplicates import duplicate_free
from opensbt.visualization.visualizer import get_pop_using_mode

def export_xosc(res, save_folder, mode="crit", max="100"):
    problem = res.problem
    is_simulation = problem.is_simulation()
    if is_simulation:
        inds = get_pop_using_mode(res=res, 
                                  mode=mode)
        clean_pop = duplicate_free(inds)[:max]
        if len(clean_pop) == 0:
            return
        for i, ind in enumerate(inds):
            extract_xosc(ind.get("SO"),
                         file_path_new = save_folder + os.sep + "extract" + os.sep + f"scenario_{i}.xosc",
                         road_network_path=None)
    else:
        print("No xosc export possible. Problem is not ADASProblem.")