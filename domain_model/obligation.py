

class Obligation:
    """
        This class represents a regular obligation of a person.
        The obligation requires a person to be at a specific location between specific start and end times on specific weekdays.
        Obligations with location None are interpreted as happening outside of the house.
        Obligations with no weekdays attached are interpreted as happening every day.
    """
    def __init__(self,name, start_time, end_time, location = None, weekdays = None):
        """
            Constructor.

            Args:
                name (string): the name of the obligation.
                start_time (time): the start time of the obligation.
                end_time (time): the end time of the obligation.
                location (Room): the location where the obligation happens. None means the location happens outside of the house.
                weekdays (int[]): the weekdays where the obligation happens. 0 = Monday, 6 = Sunday. None means every day.

        """
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.weekdays = weekdays

    def happens_today(self,date):
        """
            Checks whether the obligation schould be scheduled on a given date. 
            
            Args:
                date (datetime): the date to check.

            Returns:
                bool: True if the date is a day of the week where this obligation happens.
        """
        if self.weekdays == None:
            return True
        
        weekday = date.weekday()
        if weekday in self.weekdays:
            return True
        return False
