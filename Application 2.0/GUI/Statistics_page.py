from tkinter import Frame, Label
from tools import Tools

class StatisticsPage(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = Label(self, text="Statistics Page")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        Tools.create_button(self, "Record Statistics", self.record_statistics, 1, 0)

    def record_statistics(self):

        pass
