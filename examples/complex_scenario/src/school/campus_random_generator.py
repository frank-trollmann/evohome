

from random import Random

class Campus_Random_Generator:
    """
        Random generator instance for the simulation scenario.
        This random number generator guarantees reproducibility of simulation. Do not use outside of the simulation.
    """
    _generator = Random()

