

from random import Random

class Simulation_Random_Generator:
    """
        Random generator instance for the simulation scenario.
        This random number generator guarantees reproducibility of simulation. 
        WARNING: Do not use outside of the simulation, unles you know what you're doing.
    """
    _generator = Random()

