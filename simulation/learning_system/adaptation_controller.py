
from simulation.learning_system.adaptation_metadata import Adaptation_Metadata


class Adaptation_Controller:

    def set_simulation(self, simulation):
        """
            sets the reference to the simulation
        """
        self.simulation = simulation

    def on_simulation_start(self):
        """
            Notifies the adaptation controller that the simulation has started.
            Is called after the simulation environment is initialized but before the first tick.
            Any initializing work (e.g., determining the initial model) can be done here.
            You can assume that simulation.prediction_system is set at this point.
        """
        pass

    def on_new_prediction(self, time, y, y_pred, prediction_metadata):
        """
            Notifies the adaptation controller of a new prediction.
            This function can be implemented to react to a new data point.
            The function is called retroactively in the minute for which the prediction is made. 

            Args:
                time (datetime): the time of the data point.
                y (array of booleans): the actual sensor data for all rooms.
                y_pred (array of booleans): the prediction for all rooms.
                prediction_metadata (Prediction_Metadata): the metadata of the prediction
        """
        pass

    def get_last_adaptation_metadata(self):
        """
            Returns the metadata of the last call of on_new_prediction.
            In it's default implementation the metadata is empty. Adaptation time is added externally in the simulation.

            This method can be overwritten in order to keep track of more metadata.
        """
        return  Adaptation_Metadata()

