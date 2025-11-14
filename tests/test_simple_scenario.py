
import os
import unittest

from examples.simple_scenario.src.decision_tree_predictor import Decision_Tree_Predictor
from examples.simple_scenario.src.extended_data_recorder import Extended_Data_Recorder
from examples.simple_scenario.src.simple_scenario import create_simple_scenario
from simulation.simulation import Simulation

class Test_Simple_Scenario(unittest.TestCase):
    """
        tests the simple scenario.
        This is an integration test that tests a lot of components and how they play together.
    """

    def setUp(self):
        """
            run the simple scenario for two days and check that there is no exception and the appropriate files have been created
        """
        print("set up")
        # set up mock house
        self.simulation = Simulation(display_user_interface = False, 
                            max_simulated_minutes = -1,
                            prediction_delay_in_min = 60,
                            random_seed = 42)

        self.filename = "tests/simple_scenario_temp.pickle"
        
    def test_run_simulation(self):
        try:
            scenario = create_simple_scenario()
            self.simulation.max_simulated_minutes = 2*24*60
            self.simulation.set_scenario(scenario)

            data_recorder = Extended_Data_Recorder(self.filename)
            self.simulation.set_data_recorder(data_recorder)

            prediction_system = Decision_Tree_Predictor()
            self.simulation.set_prediction_system(prediction_system)

            self.simulation.start()
        except Exception as exception:
            assert False, "Exception during simulation: {exception}"
        
        # assert file exists:
        assert os.path.exists(self.filename), "Recorded file was not created."

    def tearDown(self):
        # remove file
        if os.path.exists(self.filename):
            os.remove(self.filename)

 