from datetime import datetime
from tkinter import messagebox


class Contract:
    def __init__(self, start_date, end_date, salary):
        self.start_date = start_date
        self.end_date = end_date
        self.salary = salary

        self.validate_date_format(self.start_date)
        self.validate_date_format(self.end_date)
    
    def validate_date_format(self, date):
        try:
            datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
            return messagebox.showerror("Erreur",f"Le format de la date '{date}' doit être JJ-MM-AAAA")
        
    def update(self, start_date, end_date, salary):
        self.start_date = start_date
        self.end_date = end_date
        self.salary = salary

        # Vérification des formats de dates
        self.validate_date_format(self.start_date)
        self.validate_date_format(self.end_date)

    def to_dict(self):
        return {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'salary': self.salary
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['start_date'], data['end_date'], data['salary'])