

class Leisure_Activity:
    """
        This class represents a leisure activity and associated preferences.
        Leisure activities will be selected randomly according to their weight whenever a simulated person has free time. 
    """
    def __init__(self,name,location = None, weekdays = None):
        """
            Constructor.

            Args:
                name (string): the name of the activity.
                location (Room): the location of the activity.
                weight (int): the weight of the activity. Activities with greater weight are more likely to be chosen.
                weekdays (int[]): the weekdays where the obligation happens. 0 = Monday, 6 = Sunday. None means every day.

        """
        self.name = name
        self.location = location
        self.weekdays = weekdays

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

        return True

