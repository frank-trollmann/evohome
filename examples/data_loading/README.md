# Scenario Purpose

This scenario illustrates how to run the exemplar with recorded occupancy data, rather than a simulated scenario. This is accomplished by loading data from a dataset and using the *ReplaySimulator*$* to play it back. 

# Useage

The scenario can be started as a module via *python -m examples.data_loading.main* from the main folder of the project.
Running the module will create the pygame surface and visualize the loaded data.

# The Scenario:

The scenario simulates room usage on the campus of CODE University of Applied Sciences with some of it's meeting rooms.
Data is loaded from *data/occupancy_data.csv*. The data is purely fictional.


# Project Structure

The project is structured along the following folders:
- *data*: this folder contains scenario data.
- *images*: contains images for visualizing the scenario and displaying it in the simulator
- *src*: contains source code.

# Source Code

The main discussion of source code for running a scenario can be found in the simple_scenario example.

Here we discuss onle the part that relates to loading and running an existing scenario.

This is accomplished with the following lines:
```
 data = Occupancy_Data_Loader.load_data()
 rooms = Occupancy_Data_Loader.get_rooms()
 simulator = Replay_Simulator(rooms= rooms, 
                                 data = data,
                                 background_image= "examples/data_loading/images/smart_campus.png",
                                 start_date= datetime(year = 2025, month=11, day = 14, hour = 8),
                                 )
 simulation.set_simulator(simulator)
```

The main interface towards the simulation is the $Replay_Simulator$. This simulator draws it's data from an existing dataset (parameter $data$) and starts simulation at the provided $start_date$. It can also be filled with a custom *background_image* as well as a set of $rooms$ in order to determine visualization-friendly room names and coordinates.

The class *Occupancy_Data_Loader* is specific to this example and showcases how the dataset is loaded and converted into the right format.
