class Shift:
    def __init__(self, month, day, start_time, end_time, duration, description, days_of_week, week_hours):
        self.month = month
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.description = description

        self.description = self.description + " - Week hours: [" + week_hours + "]"
        
        
        self.data_list = [self.month, self.day, self.start_time, self.end_time, self.duration, self.description]
        


    def toString(self):
        return self.data_list
    
    
    def __repr__(self):
        return f'Shift({self.month}, {self.day}, {self.start_time}, {self.end_time}, {self.duration}, {self.description})'
    

    def get_shift(self):
        
        return self.data_list