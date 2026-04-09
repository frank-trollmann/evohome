import pandas as pd

from domain_model.room import Room

class Occupancy_Data_Loader:
    """
        Example for a class that loads data from a csv file and prepares it into the format required for the simulation
    """


    @classmethod
    def load_data(cls):
        """
            Loads the data from hard drive and converts it into a dataframe.

            Assumptions:
                - Dataframe is time-indexed but only contains new entries when at least one room has changed.

            Expected output:
                - Time-indexed Dataframe with rooms as columns.
                - Each cell has boolean value, representing occupancy status.
        """

        # find start and end time 
        raw_data = cls.load_raw_data()
        min_date = raw_data["time"].min()
        min_date = min_date.replace(microsecond=0)
        max_date = raw_data["time"].max()
        max_date = max_date.replace(microsecond=0)

        # prepare processed dataframe
        rooms = cls.get_rooms()
        date_index = pd.date_range(start = min_date, end = max_date, freq='1s')
        processed_data =  pd.DataFrame(index = date_index)

        # add data room by room
        for room in rooms:
            print("loading data for room " + room.name)

            # initialze with no presence
            processed_data[room.name] = False

            # add presence timeblocks
            for index in range(len(raw_data)-1):
                value = raw_data[room.name].iloc[index]
                if(value > 0 ):
                    start_date = raw_data["time"].iloc[index]
                    start_date = start_date.replace(microsecond=0)
                    end_date = raw_data["time"].iloc[index+1]
                    end_date = end_date.replace(microsecond=0)
                    processed_data.loc[(processed_data.index >= start_date) & (processed_data.index < end_date),room.name] = True

        return processed_data



    @classmethod
    def load_raw_data(cls):
        """
            Load raw data from data/occupancy_data.csv
        """
        raw_data = pd.read_csv("examples/data_loading/data/occupancy_data.csv")
        raw_data["time"] = pd.to_datetime(raw_data["time"])
        return raw_data
   
    @classmethod
    def get_rooms(cls):
        """
            returns the rooms from this scenario.
        """
        return [Room("A1",2750,1060),
                    Room("A6",1930,2000),
                    Room("A11",650,2000),
                    Room("A12",600,1700),
                    Room("B3",2345,1560),
                    Room("B4",2140,1560),
                    Room("B5",1960,1560),
                    Room("B6",1830,1560),
                    Room("B7",1700,1560),
                    Room("B12",980,1560),
                    Room("B14",1080,980),
                    Room("Makerspace",2190,2000),
                    Room("Phone Booth 1",2520,1730),
                    Room("Phone Booth 3",2520,1830)]