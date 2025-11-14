
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

