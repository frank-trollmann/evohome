

from random import Random

class Simulation_Random_Generator:
    """
        Random generator instance for the simulation.
        In order to not be influenced by random number generator use within adaptation or prediction, this is a dedicated insctance of the random number generator.
    """
    _generator = Random()

