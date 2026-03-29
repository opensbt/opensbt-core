<div align="center">

  <img src="./docs/figures/fortiss-openSBT-Logo-RGB-neg-back.png" height="120" />
  <p></p>
  <p style="margin-top: 1em;">
    <strong>OpenSBT: A Modular Framework for Search-Based Testing of Automated Driving Systems</strong>
  </p>

  <hr width="60%" style="margin: 1.5em 0;"/>

  <p>
    <img src="https://github.com/opensbt/opensbt-core/actions/workflows/main.yml/badge.svg" alt="Pipeline Status"/>
    <img src="https://github.com/opensbt/opensbt-core/actions/workflows/sphinx.yml/badge.svg?branch=main&event=push" alt="Docs Status"/>
    <a href="https://doi.org/10.1145/3639478.3640027">
      <img src="https://img.shields.io/badge/DOI-10.1145/3639478.3640027-orange.svg" alt="DOI"/>
    </a>
    <a href="https://opensbt.github.io/opensbt-core/">
      <img src="https://img.shields.io/badge/Documentation-online-blue" alt="Documentation"/>
    </a>
  </p>

</div>

## Table of Contents
- [About](#about)
- [Overview](#overview)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Output](#output)
- [Application](#application)
- [Contribution](#contribution)
- [Acknowledgements](#acknowledgements)
- [Reference](#reference)
- [License](#license)

## About

OpenSBT is a modular and extensible codebase designed to facilitate search-based testing of automated driving systems, whether for research, in education or in an industrial context. It provides well-defined interfaces for the integration of search algorithms, fitness functions, testing oracles, and simulation environments in a modular and flexible manner. In addition, OpenSBT supports the visualization of testing results and analysis of the failing behaviour of automated driving systems. 

## Overview

<div align="center"><img src="https://github.com/opensbt/opensbt-core/blob/main/docs/figures/OpenSBT_architecture_120124.png?raw=True" width=500 ></div>

OpenSBT builds upon [Pymoo](https://pymoo.org/) 0.6.0.1 and extends internal optimization related models to tailor heuristic search algorithms for testing automated driving systems. An introductory video of OpenSBT can be found here: https://www.youtube.com/watch?v=qi_CTTzrk5s. 

## Installation

OpenSBT requires Python to be installed and its compatibility has been tested with Python 3.8. OpenSBT can be run as a standalone application or can be imported as a library.

You can install OpenSBT via pypi:

```bash
pip install opensbt
```

If using as a standalone appplication install the dependencies after downloading OpenSBT files:

```bash
pip install -r requirements.txt
```

A complete installation example is available as a [jupyter notebook](https://github.com/opensbt/opensbt-core/tree/main/docs/jupyter/01_Installation.ipynb).

## Getting Started

In the core implementation of OpenSBT a simplified dummy simulator is integrated (linear motion planning, no GPU required). To run an example test generation for this example run (flag -e holds the experiment number):

```bash
python run.py -e 5
```

Several result artefacts are generated after the generation has finished. All artefacts are written into the *results* folder in a folder named DummySimulator (problem name). 

You can find several tutorials as [jupyter notebooks](https://github.com/opensbt/opensbt-core/tree/main/docs/jupyter) which explain step-by-step of how integrate custom simulators and define testing components and objectives in OpenSBT.

The tutorials include as an example the integration of a real-world FMI-based AEB agent developed in the [fortiss Mobility lab](https://www.fortiss.org/forschung/fortiss-labs/detail/mobility-lab) simulated in [CARLA](https://carla.org/) using the simulator adapter [CARLA Runner Extension](https://github.com/opensbt/carla-runner).

As another example we have integrated Simulink-based systems simulated in Prescan [simulator adapter](https://github.com/opensbt/prescan_runner) into OpenSBT.


## Output

OpenSBT produces several result artefacts. An excerpt is given below.

| Type | Description | Example | 
|:--------------|:-------------|:--------------|
| Design Space Plot | Visualization of all evaluated test cases in the input space and predicted failing regions using the decision tree algorithm, pairwise. Constraints of derived regions are stored in a CSV file [bounds_regions.csv](https://github.com/opensbt/opensbt-core/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/classification/bounds_regions.csv) and the learned tree in [tree.pdf](https://github.com/opensbt/opensbt-core/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/classification/tree.pdf) | <img src="https://github.com/opensbt/opensbt-core/blob/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/design_space/orientation_ego_orientation_ped.png?raw=True" alt="Design Space Plot" width="400"/>  |
| Scenario 2D Visualization | Visualization of traces of the ego vehicle and adversaries in a two-dimensional GIF animation | <img src="https://github.com/opensbt/opensbt-core/blob/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/gif/0_trajectory.gif?raw=True" alt="Scenario Visualization" width="300"/> |
Objective Space Plot | Visualization of fitness values of evaluated test cases, pairwise.   | <img src="https://github.com/opensbt/opensbt-core/blob/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/objective_space/Min Adapted Distance_Velocity At Min Adapted Distance.png?raw=True" alt="Objective Space Plot" width="400"/> |
| All Testcases |  CSV file of all test inputs of all evaluated testcases | [all_testcases.csv](https://github.com/opensbt/opensbt-core/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/all_testcases.csv) |
| All Failing Testcases |  CSV file of all failing test inputs of all evaluated testcases | [all_critical_testcases.csv](https://github.com/opensbt/opensbt-core/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/all_critical_testcases.csv)|
| Calculation Properties |  CSV file of all experiment configuration parameters (e.g. algorithm parameters, such as population size, number iterations; search space, fitness function etc..).  | [calculation_properties.csv](https://github.com/opensbt/opensbt-core/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/calculation_properties.csv) |
| Evaluation Results |  CSV file containing performance values of the algorithm, e.g., number failing test cases found in relation to all evaluations, execution time.| [summary_results.csv](https://github.com/opensbt/opensbt-core/tree/main/docs/example/results/single/PedestrianCrossingStartWalk/NSGA2-F/ex1/summary_results.csv)|

## Application

Following Simulators have been integrated already into OpenSBT:

- [Prescan](https://plm.sw.siemens.com/de-DE/simcenter/autonomous-vehicle-solutions/prescan/?srsltid=AfmBOopocBsnRiNvzArkpWzeY4hpyFAta4txtL_dYqWWtkw4w5u3PzhE): [Example](https://github.com/opensbt/prescan-runner)
- [CARLA](https://carla.org/): [Example](https://github.com/opensbt/carla-runner)
- [Donkey](https://github.com/tawnkramer/donkey): [Example](https://github.com/opensbt/opensbt-core/tree/main/examples/lanekeeping/donkey?ref_type=heads)
- [Udacity](https://github.com/udacity/self-driving-car-sim): [Example](https://github.com/opensbt/opensbt-core/tree/main/examples/lanekeeping/udacity?ref_type=heads)
- [BeamNG](https://www.beamng.com/game/): [Example]()
- [esmini](https://github.com/esmini/esmini): [Example](https://github.com/opensbt/opensbt-core/tree/main/examples/esmini?ref_type=heads)

OpenSBT has been applied in research:

- Replication Study: [Paper](https://dl.acm.org/doi/10.1016/j.infsof.2023.107286), [Code](https://github.com/Leviathan321/reflection_study) 
- Autonomous Driving Testing: [Paper](https://doi.org/10.1007/978-3-031-46002-9_15), [Video](https://drive.google.com/file/d/1lr5BZpLFaxotwNFju43WF1C9fUTNM-SS/view?usp=sharing) 
- Algorithm Benchmarking: [Paper](https://dl.acm.org/doi/10.1145/3643786.3648023), [Code](https://github.com/ast-fortiss-tum/svm-paper-deeptest-24) 
- Failure Coverage Study: [Paper](https://link.springer.com/article/10.1007/s10664-024-10564-3), [Code](https://github.com/ast-fortiss-tum/coverage-emse-24) 

## Contribution

If you like to contribute please contact one of the developers listed below or create a pull request. If you face any issues with OpenSBT feel free to create an issue or contact the developers.

## Acknowledgements
<a href="https://www.fortiss.org"><img align="right" src="https://www.fortiss.org/fileadmin/user_upload/06_Ergebnisse/Informationsmaterialien/Logo_fortiss_RGB_blue.png" width="120"/></a>

OpenSBT has been developed by [Lev Sorokin](mailto:lev.sorokin@tum.de), [Tiziano Munaro](mailto:munaro@fortiss.org) and [Damir Safin](mailto:safin@fortiss.org) within the 
[FOCETA Project](https://www.foceta-project.eu/tools/) at [fortiss GmbH](https://www.fortiss.org/). Special thanks go to [Brian Hsuan-Cheng Liao](mailto:h.liao@eu.denso.com) and Adam Molin from [DENSO AUTOMOTIVE Deutschland GmbH](https://www.denso.com/de/de/about-us/company-information/dnde/) for their valuable feedback and evaluation of OpenSBT on the AVP Case Study in the Prescan simulator.



## Reference

If you use or extend OpenSBT please cite our framework. Here is an example BibTeX entry:

```bibtex
@inproceedings{10.1145/3639478.3640027,
    author = {Sorokin, Lev and Munaro, Tiziano and Safin, Damir and Liao, Brian Hsuan-Cheng and Molin, Adam},
    title = {OpenSBT: A Modular Framework for Search-based Testing of Automated Driving Systems},
    year = {2024},
    isbn = {9798400705021},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3639478.3640027},
    doi = {10.1145/3639478.3640027},
    booktitle = {Proceedings of the 2024 IEEE/ACM 46th International Conference on Software Engineering: Companion Proceedings},
    pages = {94–98},
    numpages = {5},
    keywords = {search-based software testing, metaheuristics, scenario-based testing, autonomous driving, automated driving},
    location = {, Lisbon, Portugal, },
    series = {ICSE-Companion '24}
}
```
## License

OpenSBT is licensed under the [Apache License, Version 2.0](LICENSE).
