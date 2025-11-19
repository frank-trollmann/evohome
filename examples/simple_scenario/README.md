# Scenario Purpose

This scenario illustrates how to:
- define a scenario for the simulation
- record data with the simulation
- deploy a machine learning model in the simulation
- record and evaluate data about the performance of the machine learning model.

# The Scenario:

The scenario is defined in src/simple_scenario.py. 

Here we describe a short summary of the scenario:

## House and Occupants:

It consists of a house with 11 rooms. The layout of the house is as follows:
![House](images/house_1.png)

The house has four occupants : 
- Arny and Betty (sleep in Bedroom 1)
- Coline (sleeps in Bedroom 2)
- Dave (sleeps in Bedroom 3)

## Schedules:

Each person has a daily schedule of obligations that differs only between weekday and weekend. Initially, these obligations are as follows:

### Arny Weekday:
| Obligation | Time | Location |
| ---------- | ---- | -------- | 
| Breakfast | 6:00 - 6:30 | Living Room |
| Work       | 7:00 - 14:00 | Office |
| Get kids from school | 14:00 - 15:00 | Outside |
| Prepare Dinner | 16:00 - 17:00 | Kitchen |
| Dinner | 17:00 - 18:00 | Living Room |

### Arny Weekend:
| Obligation | Time | Location |
| ---------- | ---- | -------- | 
| Study | 10:00 - 11:00 | Bedroom 2 |
| Lunch | 12:00 - 13:00 | Living Room |
| Prepare Dinner | 16:00 - 17:00 | Kitchen |
| Dinner | 17:00 - 18:00 | Living Room |


### Betty Weekday:
| Obligation | Time | Location |
| ---------- | ---- | -------- | 
| Work       | 6:00 - 16:00 | Outside |
| Dinner | 17:00 - 18:00 | Living Room |
| Read Bedtime Story | 19:30 - 20:00 | Bedroom 2 |

### Betty Weekend:
| Obligation | Time | Location |
| ---------- | ---- | -------- | 
| Prepare Lunch | 11:00 - 12:00 | Kitchen |
| Lunch | 12:00 - 13:00 | Living Room |
| Piano Practice | 13:00 - 15:00 | Outside |
| Dinner | 17:00 - 18:00 | Living Room |
| Read Bedtime Story | 19:30 - 10:00 | Bedroom 2 |

### Coline Weekday:
| Obligation | Time | Location |
| ---------- | ---- | -------- | 
| Breakfast | 6:00 - 6:30 | Living Room |
| School | 7:00 - 15:00 | Outside |
| Dinner | 17:00 - 18:00 | Living Room |
| Read Bedtime Story | 19:30 - 10:00 | Bedroom 2 |

### Coline Weekend:
| Obligation | Time | Location |
| ---------- | ---- | -------- | 
| Study | 10:00 - 11:00 | Bedroom 2 |
| Lunch | 12:00 - 13:00 | Living Room |
| Dinner | 17:00 - 18:00 | Living Room |
| Read Bedtime Story | 19:30 - 10:00 | Bedroom 2 |


### Dave Weekday:
| Obligation | Time | Location |
| ---------- | ---- | -------- | 
| Breakfast | 6:00 - 6:30 | Living Room |
| School       | 7:00 - 15:00 | Outside |
| Dinner | 17:00 - 18:00 | Living Room |

### Dave Weekend:
| Obligation | Time | Location |
| ---------- | ---- | -------- | 
| Lunch | 12:00 - 13:00 | Living Room |
| Chess Club| 15:00 - 17:00 | Outside |
| Dinner | 17:00 - 18:00 | Living Room |

## Variability: 
The scenario runs from 06.06.2020 for approximately two years. During this time the scenario is subject to the following variability:

### Leisure time:
During periods of leisure time (when no obligation is scheduled) the person picks randomly from a weighted list of leisure activities. Some activities require ressources (e.g., watching TV occupies the TV) which limits choices for others. The priority of activities that happen outside of the house or on the porch is influenced by weather, so that activities on the porch will be less likely during winter or bad weather.

### Cooking time change:
Starting from 02.03.2021, Arny starts and ends cooking Dinner half an hour earlier. This directly changes presence times in the kitchen on every day.

### Daves temporarily leaves.
On 02.06.2021 Dave temporarily leaves the household because he participates in a student exchange. Dave returns on 02.09.2021. This changes presence times for Daves room (Room 3) and any rooms Dave occupies during obligations or leisure times.


### Leisure activity change
On 02.01.2022, Dave changes priority in leisure activities. Instead of playing video games, Dave is learning to cook and practices cooking regularly. This changes the distribution of rooms in leisure times.







# Project Structure

The project is structured along the following folders:
- *data*: this folder contains the data recorded as part of this scenario.
- *images*: contains images for visualizing the scenario and displaying it in the simulator
- *notebooks*: contains Python Notebooks to visualize the collected data.
- *src*: contains source code.


# Useage

The scenario can be started as a module via *python -m examples.simple_scenario.main <execution_mode>* from the main folder of the project.

Execution mode can have one of three values:
- *RECORD*: runs the simulation for 6 months, recording presence data. Data will be stored in *data/recording.pickle* and can be explored using *data_exploration.ipynb*
- RUN:  runs the simulation for 24 months, recording presence data and predictions. Data will be stored in *data/running.pickle* and can be explored using *model_evaluation.ipynb*
- ADAPT: runs the simulation for 24 months, while adapting. The scenario is the same as in RUN but an additional adpatation controller retrains the model periodically. Data will be stored in *data/adapting.pickle* and can be explored using *adaptation_evaluation.ipynb*
- VIEW: runs the simulation indefinitely with predictions and a user interface. No data will be recorded.
