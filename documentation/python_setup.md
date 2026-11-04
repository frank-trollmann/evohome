# Python Setup 
This guide gives detailed steps for setting up the Python environment for this project. The document is directed at Python beginners who need help setting up virtual environments and installing dependencies. More specifically, this document describes how to ...
- Install Conda Miniforge
- Create and activate a virtual environment
- Install all dependencies needed for the exemplar.
- Check that everything is installed correctly.
- View Python Notebooks to visualize the datasets created with the exemplar.

Conda Miniforge is not a requirement for the exemplar, but a choice for the convenience of managing Python versions and virtual environments easily. 

The following steps should get your environment ready to use the exemplar.

## 1) Installing Conda Miniforge

To create a suitable Python environment we recommend using Conda Miniforge. Links and instructions for installation for different platforms can be found [here](https://conda-forge.org/download/). 

Once installed, you can use the Miniforge prompt application to run conda commands. If you have chosen to add Conda Miniforge to your PATH during installation, you should also be able to run the command $conda$ in your terminal directly.

## 2) Creating a virtual environment.

It is strongly recommended to run this project with Python 3.12, since this version of Python is compatible with common Machine Learning libraries, such as TensorFlow, Keras, or Numpy. These frameworks usually lag behind the latest version of Python a bit, meaning newer versions of Python may not be able to install all dependencies for this project.

A virtual environment with Python 3.12 can be created from the Conda Miniforge with the following command:

````
conda create -n evoHomeEnv python=3.12
````

Once the environment is created, you can activate it with the following command:
````
conda activate evoHomeEnv
````
Once the environment is activated, any call to the Python program will use this environment and the libraries installed in it. You can decativate the environment with the following command: 

````
conda deactivate
````


## 3) Installing all dependencies.

All dependencies of the project are located in requirements.txt. You can install them in your Python environment with the following command:

````
pip install -r requirements.txt
````

## 4) Checking that everything is installed correctly.

To check that everything is installed correctly, you can run the simple scenario in record mode.

From the main folder of the project, the scenario can be run with the following command:

````
python -m examples.simple_scenario.main RECORD
````

This runs the simulation for three months on the simple scenario example (see main documentation). It should run through without error and end on the message "Finished. Stored dataframe with 129600 elements under: (...)".


## 5) Viewing Python Notebooks.

Python notebooks are used to visualize and evaluate the datasets recorded as part of the simulation. If you intend to work with this exemplar actively, we recommend to set up notebooks as part of your development environment. If you just want a quick look through the notebooks, you can use the Jupyter environemnt. It can be installed with the following command in your Python environment:

````
pip install jupyter notebook`
````

Once installed, it can be started with the following command:
````
jupyter notebook
````

This command will start a webserver and open a browser window with the Jupyter environment.
