# Classe stade

class Stadium:
    def __init__(self, name, location, capacity):
        self.name = name
        self.location = location
        self.capacity = capacity

    def display_details(self):
        return f"Stadium Name: {self.name}\nLocation: {self.location}\nCapacity: {self.capacity}"

    def __str__(self):
        return self.display_details()
