import datetime
import unittest

from pandas import DataFrame

from domain_model.room import Room
from simulation.replay_simulator import Replay_Simulator
from simulation.simulation import Simulation

class Test_Replay_Simulator(unittest.TestCase):
    """
        This test checks the replay simulator and it's use in simulation.
    """

    def setUp(self):
        """
            run the simple scenario for two days and check that there is no exception and the appropriate files have been created
        """
        self.room1 = Room("Room1",0,0)
        self.room2 = Room("Room2",0,0)
        
        self.start_date = datetime.datetime(year=2007, month= 7, day = 7, hour=7, minute = 7)
        delta = datetime.timedelta(minutes=1)
        index = [self.start_date, 
                 self.start_date + delta,
                 self.start_date + delta + delta]
        data_dict = {
            "Room1":[True, False, False],
            "Room2":[False, True, False]
        }
        data = DataFrame(data = data_dict, index = index)

        self.simulator = Replay_Simulator(rooms= [self.room1, self.room2], 
                                          data = data, 
                                          )
        self.simulation = Simulation(display_user_interface = False, 
                            max_simulated_minutes = 3,
                            prediction_delay_in_min = 0,
                            random_seed = 42)
        self.simulation.set_simulator(self.simulator)

    
    def test_start_date(self):
        assert self.start_date == self.simulator.get_start_time(), f"Start time {self.simulator.get_start_time()} is incorrect"
    
    def test_rooms(self):
        assert self.simulator.get_room_by_name("Room1") == self.room1
        assert self.simulator.get_rooms() == [self.room1, self.room2]

    def test_simulation(self):
        try: 
            self.simulation.start()
        except:
            assert False, "Exception during simulation: {exception}"