import pandas as pd

class Data_Recorder:
    """
    
        base class for recording data from an experiment.
        in it's base form, this class will record the following features:
        - date (datetime): the date and time of the data point
        - room_X (int): the value of the presence sensor in room number X. 0 stands for no presence, 1 for presence.
        - prediction_X (int): the predicted value of the presence sensor in room number X. 0 stands for no presence, 1 for presence. The value may be None if there is no prediction.
    """

    def __init__(self,filename):
        """
            Constructor.

            parameters:
                filename (string): the filename where the recorded data will be stored.
        """
        self.filename = filename

    def set_simulation(self,simulation):
        """
            used to notify the data recorder of the simulation
        """
        self.simulation = simulation
    
    def on_simulation_start(self):
        """
            Called when the simulation is started. 
            Initializes data to keep track of.
            Can be overwritten to keep track of more/ other data.
        """
        self.dates = []
        self.rooms = [] 
        self.room_predictions = []
        for index in range(len(self.simulation.rooms)):
            self.rooms.append([])
            self.room_predictions.append([])

    def on_new_datapoint(self, time, sensor_data, prediction ):
        """
            Notifies the data recorder of a new data point.
            The data recorder keeps track of the data internally.

            Args:
                time (datetime): the time of the data point.
                sensor_data (array of booleans): the sensor data for all rooms.
                prediction (array of booleans): the prediction for all rooms.
        """
        self.dates.append(time)
        for index in range(len(sensor_data)):
            self.rooms[index].append(int(sensor_data[index]))
            predicted_value = None
            if(prediction is not None):
                predicted_value = int(prediction[index])
            self.room_predictions[index].append(predicted_value)

    def compile_data(self):
        """
            Calculates a dictionary representation of the data stored so far.
            This will be called to compile data to be stored into a file.

            Returns:
                data (dict): a dictionary representation of the data.
        """
        data = {"date": self.dates}
        for index in range(len(self.simulation.rooms)):
            data["room_" + str(index)] = self.rooms[index]
            data["prediction_" + str(index)] = self.room_predictions[index]
        return data


    def on_simulation_end(self):
        """
            Called when simulation is ended.
            Stores the collected data into the file.
        """
        print(f"Storing data ...")
        data = self.compile_data()
        data_frame = pd.DataFrame(data)

        data_frame.to_pickle(self.filename)

        print(f"Finished. Stored dataframe with {len(data_frame)} elements under: {self.filename}")

