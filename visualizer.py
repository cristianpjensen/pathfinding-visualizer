from tkinter import *
from tkinter import ttk


class Visualizer():
    def __init__(self):
        self.WIDTH = self.HEIGHT = 1000
        self.CELLWIDTH = self.CELLHEIGHT = 10
        self.ROWS = self.COLUMNS = self.WIDTH // self.CELLWIDTH

        self.squares = []
        self.square_types = []

        self.window = Tk()
        self.canvas = Canvas(
            self.window, width=self.WIDTH, height=self.HEIGHT, borderwidth=0, highlightthickness=0
        )
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        for column in range(self.COLUMNS):
            self.squares.append(list())
            self.square_types.append(list())
            for row in range(self.ROWS):
                x1 = column * self.CELLWIDTH
                y1 = row * self.CELLHEIGHT
                x2 = x1 + self.CELLWIDTH
                y2 = y1 + self.CELLHEIGHT

                self.squares[column].append(self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="white", outline="white"
                ))
                self.square_types[column].append(0)

        self.window.bind("<B1-Motion>", self.wall)

        self.window.mainloop()

    def wall(self, event):
        python_green = "#476042"

        x = event.x // self.CELLWIDTH
        y = event.y // self.CELLHEIGHT

        self.canvas.itemconfig(
            self.squares[x][y], fill="black", outline="black")
        self.square_types[x][y] = 1


if __name__ == "__main__":
    Visualizer()
