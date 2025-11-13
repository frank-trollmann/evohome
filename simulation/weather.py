

import math
import random


class Weather_Simulation:
    """
        Simulates weather conditions.
        The weather is represented by a single value "quality" that represents how comfortable it is to be outside at this weather.
        The quality is calculated as season_factor * time_factor + adjustment.
        - season_factor: a factor based on the current season
        - time_factor: a factor based on the time of day.
        - adjustment: a random adjustment that represent current weather conditions
        Quality ranges from 0 (bad weather)  to 1 (good weather)
    """

    def __init__(self):
        self.quality = 0
        self.adjustment = 0
        self.season_factor = 0
        self.last_simulated_day = 0

    def tick(self, current_time):
        """
            Simulates the current weather. 
            After this has been called, the weather is stored in self.quality.
        """
        year_day = current_time.timetuple().tm_yday
        if self.last_simulated_day != year_day:
            self.last_simulated_day = year_day
            self.season_factor = self.__to_sin_value(year_day / 365)

        day_fraction = (60*current_time.hour + current_time.minute) /(24*60)
        time_factor = 0.5 + 0.5* self.__to_sin_value(day_fraction)
    
        self.adjustment += random.choice([0.01, -0.01])
        self.adjustment = min(0.1, max(-0.2,self.adjustment))

        value = self.season_factor * time_factor + self.adjustment;
        self.quality = min(1,max(0,value))



    def get_quality(self):
        """
            Returns the current weather quality.
            Returns:
                float: the current weather quality between 0 (bad) and 1 (good).
        """
        return self.quality

    def __to_sin_value(self, fraction):
        """
            returns an adjusted sine value such that ...
            - the value is strictly between 0 and 1.
            - a wave starts at 0 for fraction 1, goes to 1 for fraction 0.5 and goes back to 0 for fraction 1
            - one wave iteration happens exactly between fractions of [0,1]
        """
        return 0.5 + 0.5* math.sin(2* math.pi * (fraction-0.25))

