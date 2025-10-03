class Shift:
    def __init__(self, month, day, start_time, end_time, duration, description):
        self.month = month
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.description = description
        self.data_list = [month, day, start_time, end_time, duration, description]

    def __repr__(self):
        return f'Shift({self.month}, {self.day}, {self.start_time}, {self.end_time}, {self.duration}, {self.description})'
    
    def toString(self):
        return self.data_list

    def get_shift(self):
        shift = [self.month, self.day, self.start_time, self.end_time, self.duration, self.description]
        return shift