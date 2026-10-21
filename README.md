# Project Purpose

"Evolving Home" (EvoHome) is an exemplar for Lifelong Learning in the smart home domain.
The exemplar consists of a simulator for occupancy sensors in a building in which persons walk around according to daily schedule and preferences. 

The simulator can be used to create datasets for training Machine Learning models and to test and evaluate Machine Learning models based on their ability to predict presence of people in a room at specific times.

The simulation can be configured with changes (such as changing schedules, persons moving in or out) that change the behaviour of the simulation and would likely degrade the prediction quality of static models. This can be used to evaluate Lifelong Learning approaches that are used to counter these changes.

# Project Structure

The project is structured along the following folders:
* *domain_model*: represents the model used for the simulation. The model consists of a home with persons, schedules and changes.
* *view*: the visualization of the domain model in a pygame window.
* *simulation*: The simulation engine that controls the simulation.
* *examples*: example projects to showcase how this exemplar can be used.
* *tests*: unittests

# Project Setup

This project requires Python 3.10.6 or higher and has beend developed using VSCode.
Dependencies are listed in requirements.txt and can be installed using *pip install -r requirements.txt*

# Testing
Automates tests are located in folder "test" and can be executed with *python -m unittest*.

# Test Scenarios
The folder *examples* contains several scenarios. These scenarios both serve to provide documentation and code examples for the features of the framework and to provide a set of base scenarios that can be extended. 

As a starting point for understanding how to interact with the framework, we recommend the *simpe_scenario*.

Currently, the following scenarios are implemented:
- *simple_scenario*: a simple scenario consisting of a four-person household. This scenario is both used as a showcase for how to configure a complete scenario and as an extensible base for custom scenarios.
- *data_loading*: this scenario showcases how a custom dataset - e.g., from a real smart home - could be loaded into the simulation.
- *gradual_change_scenario*: this scenario illustrates the implementation of gradual changes over time.
- *room_change_scenario*: this scenario illustrates how rooms can be added / removed during the simulation.
- *complex_scenario*: a more complex scenario consisting of a live-in school with up to 50 pupils. This scenario serves as a test case for more complex setups involving a larger number of persons and homes.


