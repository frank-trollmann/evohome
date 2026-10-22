

from random import Random

class Campus_Random_Generator:
    """
        Random generator instance for controlled randomness in the scenario.
        This random number generator guarantees reproducibility of scenario. Do not use outside of the scenario setup and changes.
    """
    _generator = Random()

