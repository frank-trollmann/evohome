import domain_model.scenario
from examples.data_recording.data_recorder import Data_Recorder
from examples.data_recording.decision_tree_predictor import Decision_Tree_Predictor
from simulation import prediction_system
from simulation.simulation import Simulation



def main(scenario, prediction_system):
    simulation = Simulation(display_user_interface = False, 
                            max_simulated_minutes = 24*30*24*60, 
                            prediction_delay_in_min = 60)
    simulation.set_scenario(scenario)
    simulation.set_prediction_system(prediction_system)
    simulation.start()



if __name__ == "__main__":
    scenario = domain_model.scenario.create_test_scenario()
    prediction_system = Decision_Tree_Predictor(record_data=True)
    #prediction_system = Data_Recorder("examples/data_recording/data/recording.pickle")
    main(scenario, prediction_system)
