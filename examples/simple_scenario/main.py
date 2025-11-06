import sys

from examples.simple_scenario.src.extended_data_recorder import Extended_Data_Recorder
from examples.simple_scenario.src.decision_tree_predictor import Decision_Tree_Predictor
from examples.simple_scenario.src.simple_scenario import create_simple_scenario

from simulation import prediction_system
from simulation.simulation import Simulation

 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing command line argument. Please provide the following arguments:")
        print("- Execution mode: RECORD/RUN/VIEW")
        sys.exit()

    execution_mode = sys.argv[1].upper()
    if not execution_mode in ["RECORD","RUN","VIEW"]:
        print(f"Invalid execution mode {execution_mode}. Please provide one of the following arguments: RECORD/RUN/VIEW")
        sys.exit()

    scenario = create_simple_scenario()
    simulation = Simulation(display_user_interface = execution_mode == "VIEW", 
                            max_simulated_minutes = -1,
                            prediction_delay_in_min = 60)
    simulation.set_scenario(scenario)

    if execution_mode == "RECORD":
        simulation.max_simulated_minutes = 6*30*24*60
        data_recorder = Extended_Data_Recorder("examples/simple_scenario/data/recording.pickle")
        simulation.set_data_recorder(data_recorder)

    if execution_mode == "RUN":
        simulation.max_simulated_minutes = 24*30*24*60
        data_recorder = Extended_Data_Recorder("examples/simple_scenario/data/running.pickle")
        simulation.set_data_recorder(data_recorder)

        prediction_system = Decision_Tree_Predictor()
        simulation.set_prediction_system(prediction_system)

    if execution_mode == "VIEW":
        prediction_system = Decision_Tree_Predictor()
        simulation.set_prediction_system(prediction_system)
        simulation.prediction_delay_in_min = 0

    simulation.start()

