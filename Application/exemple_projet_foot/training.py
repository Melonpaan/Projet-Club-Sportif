class Training:
    def __init__(self, date, stadium, duration, training_type):
        self.date = date
        self.stadium = stadium
        self.duration = duration
        self.training_type = training_type
        self.participants = []

    def add_participant(self, person):
        if person not in self.participants:
            self.participants.append(person)

    def remove_participant(self, person):
        if person in self.participants:
            self.participants.remove(person)

    def display_details(self):
        details = f"Training on {self.date} at {self.stadium.name}\n" \
                  f"Duration: {self.duration} minutes\n" \
                  f"Type: {self.training_type}\n" \
                  f"Participants: {', '.join([p.first_name + ' ' + p.last_name for p in self.participants])}"
        return details
