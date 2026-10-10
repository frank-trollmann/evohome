from datetime import timedelta
import sys

from examples.complex_scenario.src.adaptation.composite_adaptation_controller import CompositeAdaptationController
from examples.complex_scenario.src.complex_scenario import create_complex_scenario

from examples.complex_scenario.src.extended_data_recorder import Extended_Data_Recorder
from examples.complex_scenario.src.learning.composite_predictor import Composite_Predictor
from simulation.scenario_simulator import Scenario_Simulator
from simulation.learning_system.data_recorder import Data_Recorder
from simulation.simulation import Simulation

 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing command line argument. Please provide the following arguments:")
        print("- Execution mode: RECORD/VIEW/RUN/ADAPT")
        sys.exit()

    execution_mode = sys.argv[1].upper()
    if not execution_mode in ["RECORD","VIEW", "RUN", "ADAPT"]:
        print(f"Invalid execution mode {execution_mode}. Please provide one of the following arguments: RECORD/VIEW/RUN/ADAPT")
        sys.exit()

    scenario = create_complex_scenario()
    simulation = Simulation(display_user_interface = execution_mode == "VIEW", 
                            max_simulated_minutes = -1,
                            prediction_delay_in_min = 60,
                            random_seed = 42)
    scenario_simulator = Scenario_Simulator(scenario, simulation, verbose=False) 
    simulation.set_simulator(scenario_simulator)

    if execution_mode == "RECORD":
        simulation.max_simulated_minutes = 90 * 24 * 60 # 90 days
        scenario.startTime += timedelta(days = -90)
        data_recorder = Extended_Data_Recorder("examples/complex_scenario/data/recording.pickle")
        simulation.set_data_recorder(data_recorder)

    if execution_mode == "RUN":
        simulation.max_simulated_minutes = 5 * 365 * 24 * 60 # roughly 5 years
        data_recorder = Data_Recorder("examples/complex_scenario/data/running.pickle")
        simulation.set_data_recorder(data_recorder)

        prediction_system = Composite_Predictor(scenario=scenario)
        simulation.set_prediction_system(prediction_system)

    if execution_mode == "ADAPT":
        simulation.max_simulated_minutes = 5 * 365 * 24 * 60 # roughly 5 years
        data_recorder = Data_Recorder("examples/complex_scenario/data/adapt.pickle")
        simulation.set_data_recorder(data_recorder)

        prediction_system = Composite_Predictor(scenario=scenario)
        simulation.set_prediction_system(prediction_system)

        adaptation_controller = CompositeAdaptationController(scenario = scenario, composite_predictor=prediction_system)
        simulation.set_adaptation_controller(adaptation_controller)

    simulation.start()
