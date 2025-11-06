# Scenario Purpose

This scenario illustrates how to:
- define a scenario for the simulation
- record data with the simulation
- deploy a machine learning model in the simulation
- record and evaluate data about the performance of the machine learning model. 

# Project Structure

The project is structured along the following folders:
- *data*: this folder contains the data recorded as part of this scenario.
- *images*: contains images for visualizing the scenario and displaying it in the simulator
- *notebooks*: contains Python Notebooks to visualize the collected data.


# Useage

The scenario can be started as a module via *python -m examples.simple_scenario.main <execution_mode>* from the main folder of the project.

Execution mode can have one of three values:
- *RECORD*: runs the simulation for 6 months, recording presence data. Data will be stored in *data/recording.pickle* and can be explored using *data_exploration.ipynb*
- RUN:  runs the simulation for 24 months, recording presence data and predictions. Data will be stored in *data/running.pickle* and can be explored using *model_evaluation.ipynb*
- VIEW: runs the simulation indefinitely with predictions and a user interface. No data will be recorded
