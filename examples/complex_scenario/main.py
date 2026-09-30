import sys

from examples.complex_scenario.src.complex_scenario import create_complex_scenario

from simulation.scenario_simulator import Scenario_Simulator
from simulation.learning_system.data_recorder import Data_Recorder
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

    scenario = create_complex_scenario()
    simulation = Simulation(display_user_interface = execution_mode == "VIEW", 
                            max_simulated_minutes = -1,
                            prediction_delay_in_min = 60,
                            random_seed = 42)
    scenario_simulator = Scenario_Simulator(scenario, simulation, verbose=False) 
    simulation.set_simulator(scenario_simulator)

    if execution_mode == "RECORD":
        simulation.max_simulated_minutes = 5 * 365 * 24 * 60 # roughly 5 years
        data_recorder = Data_Recorder("examples/complex_scenario/data/recording.pickle")
        simulation.set_data_recorder(data_recorder)

    simulation.start()
