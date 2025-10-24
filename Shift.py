import hashlib

class Shift:
    def __init__(self, month, day, start_time, end_time, duration, store_number, department_number, job_description, days_of_week, week_hours):
        self.month = month
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.store_number = store_number
        self.department_number = department_number
        self.job_description = job_description

        
        self.description = f'{store_number} - Store {department_number} - {job_description} - Week Hours [{week_hours}]'
        
        self.data_list = [
            self.month, 
            self.day, 
            self.start_time, 
            self.end_time, 
            self.duration, 
            self.store_number, 
            self.department_number, 
            self.job_description,
            self.description
            ]
        


    def toString(self):
        return self.data_list
    
    
    def __repr__(self):
        return f'Shift({self.month}, {self.day}, {self.start_time}, {self.end_time}, {self.duration}, {self.description})'
    

    def get_shift(self):
        
        return self.data_list
    
    def make_uid(self):
        key = f"{self.month} {self.day}|{self.description}|{self.store_number}".strip()
        uid_hash = hashlib.sha1(key.encode("utf-8")).hexdigest()
        return f"{uid_hash}@thd-schedule"