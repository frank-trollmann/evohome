

class Obligation:
    def __init__(self,name, start_time, end_time, location = None, weekdays = None):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.weekdays = weekdays

    def happens_today(self,date):
        if self.weekdays == None:
            return True
        
        weekday = date.weekday()
        if weekday in self.weekdays:
            return True
        return False
