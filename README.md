# Exercise-1 Cellular Automata
add desc

## Setup
- Python Version: 3.7
- Required packages are written in <a href="https://github.com/crowdmodeling20ss/exercise1/blob/master/requirements.txt">requirement.txt</a>

## Run Simulation
There is three types of simulation:

### PredefinedSimulation.py
In this type of simulation, settings of the simulation is predefined hard-coded. You just need to choose scenario number for most of the scenarios. 

To run scenarios below, add the scenario number into `scenario.txt`:
- 2: Task 2
- 3: Task 3 equal_block_distance
- 41: Task 4 bottleneck
- 42: Task 4 chicken_test
- 1: Rimea Scenario 1
- 6: Rimea Scenario 6
- 7:Rimea Scenario 7

Then, run the `python Main.py` command. For the Rimea Scenario 4 you need to add two more parameters which are line_movement and density. Line movement could be 0 or 1. Density could be any floating number greater than 0. To run Rimea Scenario 4 with 0.5 density and normal map, your `scenario.txt` should be like that:
```
4 0 0.5
```
If you want to enable line movement, just change 0 to 1:
```
4 1 0.5
```
### ConfigurableSimulation.py
In this type of simulation, settings of the simulation is provided completely by user. Look at the example scenario <a href="">here</a>. After settings are determined in `new_scenario.txt`, the simulation could be run via `python Main.py configurable` command.
### UserInterfacedSimulation.py
(not implemented yet)
