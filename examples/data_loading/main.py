

import sys

from examples.data_loading.src.smart_campus_data_loader import SmartCampus_Data_Loader
from examples.data_loading.src.occupancy_data_loader import Occupancy_Data_Loader
from simulation.replay_simulator import Replay_Simulator
from simulation.simulation import Simulation
from datetime import datetime, timezone


"""
    This file showcases how to use the ReplaySimulator in conjunction with a data loader class that loads the data from hard drive.

    Execution arguments:
    - Expects one command Line argument. 

"""
 
if __name__ == "__main__":
    data = Occupancy_Data_Loader.load_data()
    rooms = Occupancy_Data_Loader.get_rooms()

    simulation = Simulation(display_user_interface = True, 
                            max_simulated_minutes = -1,
                            prediction_delay_in_min = 60,
                            random_seed = 42)
    
    simulator = Replay_Simulator(rooms= rooms, 
                                 data = data,
                                 background_image= "examples/data_loading/images/smart_campus.png",
                                 start_date= datetime(year = 2025,month=11, day = 14, hour = 8)
                                 )
    simulation.set_simulator(simulator)

    simulation.start()

    
