
import pandas as pd
from sklearn import tree

from examples.complex_scenario.src.adaptation.room_adaptation_controller import Room_Adaptation_Controller
from simulation.learning_system.adaptation_controller import Adaptation_Controller

class CompositeAdaptationController(Adaptation_Controller):
    """
        A composite adaptation controller delegating to a set of sigle adaptation controllers - one for each room.
        
        Each individual adaptation controller is in charge of adapting a specific predictor.

    """

    def __init__(self, scenario, composite_predictor):
        """
            constructor
            
            Args:
                scenario (Scenario): reference to the scenario
                composite_predictor (Composite_Predictor): reference to the predictor
        """
        self.substituted_index = 0
        self.composite_predictor = composite_predictor
        self.room_names = scenario.get_room_names()
        self.adaptation_controllers = [None] * len(self.room_names)
        for room_index in range(len(self.room_names)):
            self.adaptation_controllers[room_index] = Room_Adaptation_Controller(self.room_names[room_index], room_index, composite_predictor.predictors[room_index])

    def on_simulation_start(self):
        """
            Start the simulation.
            Load the dataset and initialize the starting data for all adaptation controllers
        """
        file_name = "examples/complex_scenario/data/recording.pickle"
        data_frame = pd.read_pickle(file_name)
        training_features = ["weekday","hour", "minute"]
        self.X = data_frame[training_features][-7*24*60:]

        for room_index in range(len(self.room_names)):
            y = data_frame[f"room_{room_index}"][-7*24*60:]
            self.adaptation_controllers[room_index].on_simulation_start(self.X,y)

    

    def on_new_prediction(self, time, y, y_pred, prediction_metadata):
        """
            notifies of new predictions.
            The predictions are forwarded to the individual room adaptation controllers
        """

        # update X value globally to avoid doing identical work in each room controller
        x_value = {"weekday": time.weekday(), "hour": time.hour, "minute": time.minute}
        self.X.iloc[self.substituted_index] = x_value
        self.substituted_index = (self.substituted_index + 1) % len(self.X)

        for room_index in range(len(self.room_names)):
            self.adaptation_controllers[room_index].on_new_prediction(time,y[room_index], y_pred[room_index], self.substituted_index)

