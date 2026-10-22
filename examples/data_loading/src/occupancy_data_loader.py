import pandas as pd

from domain_model.room import Room

class Occupancy_Data_Loader:
    """
        Example for how to load data from a csv file and prepare it for use in a replay simulator.
    """


    @classmethod
    def load_data(cls):
        """
            Loads the data from hard drive and converts it into a dataframe.

            The loaded data is a time-indexed DataFrame with sparse values - i.e., it only contains entries when a sensor value has changed.

            For purposes of the simulation, we need to convert it into a DataFrame with the following properties:
                - The dataframe is time-indexed over Datetime objects.
                - The dataframe is 

            Expected output:
                - Time-indexed Dataframe with rooms as columns.
                - Time indexes are in minute-frequency
                - Each room's occupancy is represented by a Boolean feature of the room's name.
        """

        # load data, find start and end of data timeframe
        raw_data = cls.load_raw_data()
        min_date = raw_data["time"].min()
        min_date = min_date.replace(microsecond=0).replace(second=0)
        max_date = raw_data["time"].max()
        max_date = max_date.replace(microsecond=0).replace(second=0)

        # prepare processed dataframe in minute resolution
        rooms = cls.get_rooms()
        date_index = pd.date_range(start = min_date, end = max_date, freq='1min')
        processed_data =  pd.DataFrame(index = date_index)

        # add data room by room
        for room in rooms:
            print("loading data for room " + room.name)

            # initialze with no occupation for the entire interval
            processed_data[room.name] = False

            # set occupied timeblocks
            for index in range(len(raw_data)-1):
                value = raw_data[room.name].iloc[index]
                if(value > 0 ):
                    start_date = raw_data["time"].iloc[index]
                    start_date = start_date.replace(microsecond=0).replace(second=0)
                    end_date = raw_data["time"].iloc[index+1]
                    end_date = end_date.replace(microsecond=0).replace(second=0)
                    processed_data.loc[(processed_data.index >= start_date) & (processed_data.index < end_date),room.name] = True

        return processed_data



    @classmethod
    def load_raw_data(cls):
        """
            Load raw data from data/occupancy_data.csv

            returns: the loaded data as a time-indexed pandas DataFrame
        """
        raw_data = pd.read_csv("examples/data_loading/data/occupancy_data.csv")
        raw_data["time"] = pd.to_datetime(raw_data["time"])
        return raw_data
   
    @classmethod
    def get_rooms(cls):
        """
            Retrieves the rooms of this scenario as list.

            The Room objects are not used for simulation purposes but for visualization (name and coordinate in user interface)

        """
        return [Room(name = "A1", x = 2750, y = 1060),
                    Room(name = "A6", x = 1930, y = 2000),
                    Room(name = "A11", x = 650, y = 2000),
                    Room(name = "A12", x = 600, y = 1700),
                    Room(name = "B3", x = 2345, y = 1560),
                    Room(name = "B4", x = 2140, y = 1560),
                    Room(name = "B5", x = 1960, y = 1560),
                    Room(name = "B6", x = 1830, y = 1560),
                    Room(name = "B7", x = 1700, y = 1560),
                    Room(name = "B12", x = 980, y = 1560),
                    Room(name = "B14", x = 1080, y = 980),
                    Room(name = "Makerspace", x = 2190, y = 2000),
                    Room(name = "Phone Booth 1", x = 2520, y = 1730),
                    Room(name = "Phone Booth 3", x = 2520, y = 1830)]