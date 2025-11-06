# Project Purpose

"Evolving Home" (EvoHome) is an exemplar for lifeling machine learning in the smart home domain.
The exemplar consists of a simulator for presense sensors in a smart home in which persons walk around according to daily schedule and preferences. 

The simulator can be used to create datasets for training machine learning models and to test and evaluate machine learning models based on their ability to predict presence of people in a room at specific times.

the simulation can be configured with changes (such as changing schedules, people moving in or out) that change the behaviour of the simulation and would likely degrade the prediction quality of static models. This can be used to evaluate lifelong learning methods that are used to counter these changes.

# Project Structure

The project is structured along the following folders:
* *domain_model*: represents the model used for the simulation. The model consists of a home with persons, schedules and changes.
* *view*: the visualization of the domain model in a pygame window.
* *simulation*: The simulation engine that controls the simulation.
* *examples*: example projects to showcase how this exemplar can be used.

# Project Setup

This project requires Python 3.10.6 or higher and has beend developed using VSCode.
Dependencies are listed in requirements.txt and can be installed using *pip install -r requirements.txt*


