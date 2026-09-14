import sys

from examples.gradual_change_scenario.src.gradual_change_scenario import create_gradual_change_scenario

from simulation.learning_system.data_recorder import Data_Recorder
from simulation.scenario_simulator import Scenario_Simulator
from simulation.simulation import Simulation

 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing command line argument. Please provide the following arguments:")
        print("- Execution mode: RECORD/VIEW")
        sys.exit()

    execution_mode = sys.argv[1].upper()
    if not execution_mode in ["RECORD","VIEW"]:
        print(f"Invalid execution mode {execution_mode}. Please provide one of the following arguments: RECORD/VIEW")
        sys.exit()

    scenario = create_gradual_change_scenario()
    simulation = Simulation(display_user_interface = execution_mode == "VIEW", 
                            max_simulated_minutes = -1,
                            prediction_delay_in_min = 60,
                            random_seed = 42)
    scenario_simulator = Scenario_Simulator(scenario, simulation) 
    simulation.set_simulator(scenario_simulator)

    if execution_mode == "RECORD":
        simulation.max_simulated_minutes = 10*30*24*60
        data_recorder = Data_Recorder("examples/gradual_change_scenario/data/recording.pickle")
        simulation.set_data_recorder(data_recorder)

    simulation.start()

