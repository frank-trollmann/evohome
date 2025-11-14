

from simulation.learning_system.adaptation_controller import Adaptation_Controller

class Simple_Adaptation_Controller(Adaptation_Controller):
    """
        Example for how a an adaptation controller can be implemented.
        This adaptation controller simply retrains the prediction every week.
    """

    def on_simulation_start(self):
        pass
        # TODO: this should initialize the dataset
        


    def on_new_prediction(self, time, y, y_pred, prediction_time):
        """
            Notifies the adaptation controller of a new prediction.
            This function can be implemented to react to a new data point.

            Args:
                time (datetime): the time of the data point.
                y (array of booleans): the actual sensor data for all rooms.
                y_pred (array of booleans): the prediction for all rooms.
                prediction_time (float): the time it took to compute the prediction.
        """
        pass
        # TODO. this should retrain every week.

       
