from tkinter import *
from tkinter import ttk


class Visualizer():
    def __init__(self):
        self.WIDTH = self.HEIGHT = 1000
        self.CELLWIDTH = self.CELLHEIGHT = 10
        self.ROWS = self.COLUMNS = self.WIDTH // self.CELLWIDTH

        self.COLOUR_START = "#006a4e"
        self.COLOUR_GOAL = "green"
        self.COLOUR_WALL = "#080808"
        self.COLOUR_FREE = "#f5f5f5"
        self.COLOUR_EXPLORED = "#152238"
        self.COLOUR_PATH = "#cd8d00"

        self.squares = []
        self.square_types = []
        self.start_types_coords = None
        self.start_coords = None

        self.window = Tk()
        self.canvas = Canvas(
            self.window, width=self.WIDTH, height=self.HEIGHT
        )
        self.canvas.pack()

        self.create_grid()

        self.window.bind("<Button-1>", self.colour_wall)
        self.window.bind("<B1-Motion>", self.colour_wall)

        self.window.bind("<Button-2>", self.colour_start)

        self.window.mainloop()

    def colour_wall(self, event):
        x = event.x // self.CELLWIDTH
        y = event.y // self.CELLHEIGHT

        self.canvas.itemconfig(
            self.squares[x][y], fill=self.COLOUR_WALL, outline=self.COLOUR_WALL)
        self.square_types[x][y] = 1

    def colour_start(self, event):
        # If there already is a start, remove it.
        for row_ind, row in enumerate(self.square_types):
            for col_ind, column in enumerate(row):
                if column == 2:
                    self.square_types[row_ind][col_ind] = 0
                    self.canvas.itemconfig(
                        self.squares[row_ind][col_ind], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)

        x = event.x // self.CELLWIDTH
        y = event.y // self.CELLHEIGHT

        self.canvas.itemconfig(
            self.squares[x][y], fill=self.COLOUR_START, outline=self.COLOUR_START)
        self.square_types[x][y] = 2

    def create_grid(self):
        for column in range(self.COLUMNS):
            self.squares.append(list())
            self.square_types.append(list())
            for row in range(self.ROWS):
                x1 = column * self.CELLWIDTH
                y1 = row * self.CELLHEIGHT
                x2 = x1 + self.CELLWIDTH
                y2 = y1 + self.CELLHEIGHT

                self.squares[column].append(self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=self.COLOUR_FREE, outline=self.COLOUR_FREE
                ))
                self.square_types[column].append(0)


if __name__ == "__main__":
    Visualizer()
