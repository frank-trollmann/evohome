
import random


class Leisure_Activity:
    """
        This class represents a leisure activity and associated preferences.
        Leisure activities will be selected randomly according to their weight whenever a simulated person has free time. 
    """
    def __init__(self,name,location = None, weekdays = None, min_duration = 1, max_duration = -1, required_ressources = []):
        """
            Constructor.

            Args:
                name (string): the name of the activity.
                location (Room): the location of the activity.
                weight (int): the weight of the activity. Activities with greater weight are more likely to be chosen.
                weekdays (int[]): the weekdays where the obligation happens. 0 = Monday, 6 = Sunday. None means every day.
                min_duration (int): the minimum duration of the activity in minutes.
                max_duration (int): the maximum duration of the activity in minutes. -1 means no maximum.
                required_ressources (string[]): the ressources required to perform this activity.

        """
        self.name = name
        self.location = location
        self.weekdays = weekdays
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.required_ressources = set(required_ressources)

    def is_available(self,date):
        """
            Checks whether the activity is currently available
            
            Args:
                date (datetime): the date to execute the activity on.

            Returns:
                bool: True if the date is a day of the week where this obligation happens.
        """
        weekday = date.weekday()
        if self.weekdays is not None and weekday not in self.weekdays:
            return False
        
        if self.location is not None and not self.location.ressources_available(self.required_ressources):
            return False

        return True
    
    def calculate_duration(self):
        """
            Calculates a random duration of this activity. 
            The duration will be between self.min_duration and self.max_duration.
            If self.max_duration is not set, this will return -1 (to be interpreted as running indefinitely.)
        """
        if self.max_duration <=0:
            return -1
        min_duration = max(self.min_duration,1)
        return random.randint(min_duration, self.max_duration)
    
    def start_activity(self):
        """
            Called when starting the activity.
            Does busywork, such as blocking required ressources
        """
        if self.location is not None:
            self.location.block_ressources(self.required_ressources)

    def end_activity(self):
        """
            Called when ending the activity.
            Does busywork, such as releasing required ressources
        """
        if self.location is not None:
            self.location.release_ressources(self.required_ressources)

