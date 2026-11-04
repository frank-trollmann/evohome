# Project Purpose

"Evolving Home" (EvoHome) is an exemplar for Lifelong Learning in the smart home domain. The exemplar consists of a simulator for occupancy sensors in a building in which persons move around according to daily schedule and preferences. 

The main aim of the exemplar is to enable researchers to evaluate their Lifelong Learning approaches in a new domain that includes both sudden and incremental data drift. The simulation allows for the recording of datasets that can be used to evaluate machine learning models and their adaptation. Machine Learning models and adaptation mechanisms can also be implemented directly in the exemplar in order to measure their accuracy and prediction / adaptation duration within the framework.

The exemplar can be configured to serve the following purposes:
- Create datasets of occupancy sensor data from specific simulated scenarios.
- Evaluate prediction approaches by integrating them into the simulation and recording their predictions as part of the produced dataset.
- Evaluate adaptation approaches by integrating them into the simulation and recording their predictions as part of the produced dataset.
- Visualize a scenario and it's predictions in a graphical user interface. This is mainly intended for visualization and scenario debugging purposes.
- Load existing datasets in order to visualize them or test prediction /adaptation mechanisms on them.


# Getting Started

The project is based on Python 3.12. All required libraries are contained in requirements.txt. To run this project, we recommend setting up a virtual environment and installing all dependencies with *pip install -r requirements.txt*. Note that some of the required Machine Learning libraries have not been updated to newer versions of Python. Using the latest version of Python is thus not recommended.

If you are unfamiliar with Python and need a step-by-step installation guide, please refer to [documentation/python_setup.md](documentation/python_setup.md)

To run the simulation environment, a scenario needs to be configured. This exemplar comes with several example scenarios to illustrate different aspects of the framework and provide a starting point for simulation. A list of scenarios is available further down. Here, we want to illustrate how to use the exemplar based on the *simple_scenario* example.

The *simple_scenario* is located in *examples/simple_scenario*. It consists of a four-person household, simulated over two years. During this time, the scenario implements sevaral changes, such as a person moving out of the household temporarily. Details about the scenario and it's implementation can be found in the scenario's [README](examples/simple_scenario/README.md). Here, we want to exemplify how to run the scenario and visualize the resulting datasets.

The scenario can be started as a module via *python -m examples.simple_scenario.main <execution_mode>* from the main folder of the project. For a quick start, we recommend execution mode *VIEW*. This mode runs the scenario with a pygame user interface. In addition, the simple scenario supports the following execution modes:
- *RECORD*: runs the simulation for 3 months, recording occupancy sensor values. Data will be stored in *examples/simple_scenario/data/recording.pickle*.
- *RUN*:  runs the simulation for 24 months, with a simple decision tree classifier for prediction. Data will be stored in *examples/simple_scenario/data/running.pickle*.
- *ADAPT*: runs the simulation for 24 months, with a simple decision tree classifier for prediction and an adaptation mechanism that retrains the classifier at the beginning of every week.  Data will be stored in *data/adapting.pickle*.

The main output of running the scenario in different modes is a recording of the respective run in form of a dataset. These datasets are intended to be loaded and used in the scope of a machine learning system. To illustrate this, the scenario comes with example code, in the form of Python notebooks. The folder *examples/simple_scenario/notebooks* contains three notebooks:
- [data_exploration.ipynb](examples/simple_scenario/notebooks/data_exploration.ipynb) explores the data recorded with the execution mode *RECORD*. It serves to showcase how to load the stored data as a Pandas DataFrame and visualize it with Data Science libraries.
- [prediction_evaluation.ipynb](examples/simple_scenario/notebooks/adaptation_evaluation.ipynb) loads the data recorded with execution mode *RUN* in order to showcase how the simple decision tree classifier performed on the scenario and how it's prediction quality degrades when changes are executed.
- [adaptation_evaluation.ipynb](examples/simple_scenario/notebooks/adaptation_evaluation.ipynb) load the data recorded with execution modes *RUN* and *ADAPT* in order to compare them. This allows to evaluate the effects of the simple adaptation mechanism, as well as the costs of prediction and adaptation in terms of execution times.

In a self-defined scenario, the recorded data forms the interface between the simulation and the visualization, meaning the simulation needs to be run first to produce data that then can be visualized. For the sake of illustration, we have committed datasets and pre-filled Python notebooks to this git repository in order to remove dependencies and make understanding the exemplar and it's produced data easier.


# Documentation and Examples

Setting up a custom simulation scenario requires familiarity with the simulation domain model. Documentation for the domain model can be found in [documentation/scenario_configuration.md](documentation/scenario_configuration.md).

Setting up the simulation for various use cases requires setting up a main instance of the simulation and configuring it according to the use case. Documentation for how this can be done can be found in [documentation/simulation_setup.md](documentation/simulation_setup.md).

In addition, this exemplar comes with a set of examples with varying purposes and levels of complexity. Currently, the following scenarios are available:
- *simple_scenario*: a simple scenario consisting of a four-person household. This scenario is a showcase for how to configure a complete scenario including prediction and adaptation mechanism.
- *data_loading*: this scenario showcases how a custom dataset - e.g., from a real smart home - could be loaded into the simulation.
- *gradual_change_scenario*: this scenario illustrates the implementation of gradual changes over time. It also illustrates how custom changes can be implemented.
- *room_change_scenario*: this scenario illustrates how the exemplar deals with an evolution of the learning task in which rooms are added / removed during the scenario. 
- *complex_scenario*: a more complex scenario consisting of a live-in school with up to 50 pupils which is simulated over five years. This scenario serves as a test case for more complex setups involving a larger number of persons and homes.


# Project Structure

The project is structured along the following folders:
* *domain_model*: represents the model used for the simulation. The model consists of a home with persons, schedules and changes.
* *view*: the visualization of the domain model in a pygame window.
* *simulation*: The simulation engine that controls the simulation.
* *documentation*: contains documentation for how to use the exemplar.
* *images*: contains images used in documentation.
* *examples*: example projects to showcase how this exemplar can be used.
* *tests*: unittests


# Testing
Automates tests are located in folder "test" and can be executed with *python -m unittest*.



