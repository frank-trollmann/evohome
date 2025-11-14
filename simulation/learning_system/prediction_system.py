

class Prediction_System:

    def set_simulation(self,simulation):
        self.simulation = simulation

    
    def on_simulation_start(self):
        """
            Notifies the prediction system that the simulation has started.
            Is called after the simulation environment is initialized but before the first tick.
            Any initializing work (e.g., determining the initial model) can be done here.
        """
        pass

    def on_simulation_end(self):
        """
            Notifies the prediction system that the simulation has ended.
            Is called after the last tick.
            Any postprocessing work (e.g., storing a dataset of the simulation run) can be done here.
        """
        pass

    def on_new_datapoint(self, time, sensor_data, prediction ):
        """
            Method that notifies the prediction system of a new data point. 
            This can be used to collect data for a data set or as starting point for checking and adapting the current prediction model (e.g., as part of the M-phase of a MAPE-K loop.)
            
            This method will be called by the simulation in consecutive order. It can be assumed to be the lastes point in a time series with constant frequency. 

            parameters:
            - time: an object of type datetime
            - sensor_data: an array of booleans. Each element in the array corresponds to the presence sensor in a room. Rooms are represented in the same order as self.simulation.rooms.
            - the prediction that was made for this time point (None if predict_presence is unimplemented or if the prediction delay is not exceeded)
        """
        pass

    def predict_presence(self, time):
        """
            Method that predicts the presence in rooms. The predicted presence is made known in the prediction.
            Note that the data this prediction is made on is dependent on the implementation.

            parameters:
            - time: the time to predict for. An object of type datetime.
        """
        return None