from tkinter import *
from tkinter import ttk


class Visualizer():
    def __init__(self):
        self.WIDTH = self.HEIGHT = 1000
        self.CELLWIDTH = self.CELLHEIGHT = 10
        self.ROWS = self.COLUMNS = self.WIDTH // self.CELLWIDTH

        self.COLOUR_START = "#006a4e"
        self.COLOUR_GOAL = "#8d021f"
        self.COLOUR_WALL = "#080808"
        self.COLOUR_FREE = "#f5f5f5"
        self.COLOUR_EXPLORED = "#152238"
        self.COLOUR_PATH = "#cd8d00"

        self.squares = list()
        self.square_types = list()
        self.buttons = list()

        self.window = Tk()
        self.window.title("Pathfinding Visualizer")

        self.top = Frame(self.window)
        self.top.pack(side=TOP)

        self.canvas = Canvas(
            self.window, width=self.WIDTH, height=self.HEIGHT
        )
        self.canvas.pack()

        self.create_grid()

        self.prev = None
        self.window.bind("<Button-1>", self.colour_wall)
        self.window.bind("<B1-Motion>", self.colour_wall)

        self.start = None
        self.end = None
        self.window.bind("<Button-2>", self.colour_start_goal)

        self.create_button("A*")
        self.create_button("Dijkstra")
        self.create_button("D*")
        self.create_button("Reset")

        self.window.mainloop()

    def create_grid(self):
        '''Creates the grid, based on the constants already declared.'''
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

    def create_button(self, algorithm):
        '''Creats a button, which is linked to the corresponding algorithm.'''
        self.buttons.append(ttk.Button(
            self.window, text=algorithm, command=lambda: self.pathfind(
                algorithm)
        ).pack(in_=self.top, side=LEFT))

    def colour_wall(self, event):
        '''Colours a wall, based on the x and y values of the mouse.'''
        x = event.x // self.CELLWIDTH
        y = event.y // self.CELLHEIGHT

        if (x, y) == self.prev or x < 0 or y < 0:
            return

        if self.square_types[x][y] == 1:
            self.canvas.itemconfig(
                self.squares[x][y], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)
            self.square_types[x][y] = 0
        else:
            self.canvas.itemconfig(
                self.squares[x][y], fill=self.COLOUR_WALL, outline=self.COLOUR_WALL)
            self.square_types[x][y] = 1

        self.prev = x, y

    def colour_start_goal(self, event):
        '''Colours the start or the end goal, based on the x and y values of the mouse.'''
        start = False
        end = False

        for row_ind, row in enumerate(self.square_types):
            for col_ind, column in enumerate(row):
                if column == 2:
                    start = True
                if column == 3:
                    end = True

        x = event.x // self.CELLWIDTH
        y = event.y // self.CELLHEIGHT

        if x < 0 or y < 0:
            return

        # If the pressed square is end or start, remove it.
        if (x, y) == self.start:
            self.canvas.itemconfig(
                self.squares[x][y], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)
            self.square_types[x][y] = 0

            self.start = None
            return
        elif (x, y) == self.end:
            self.canvas.itemconfig(
                self.squares[x][y], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)
            self.square_types[x][y] = 0

            self.end = None
            return

        # If one of them exists and the other doesn't, place the other.
        if start:
            if not end:
                self.canvas.itemconfig(
                    self.squares[x][y], fill=self.COLOUR_GOAL, outline=self.COLOUR_GOAL)
                self.square_types[x][y] = 3

                self.end = x, y
        else:
            self.canvas.itemconfig(
                self.squares[x][y], fill=self.COLOUR_START, outline=self.COLOUR_START)
            self.square_types[x][y] = 2

            self.start = x, y

    def pathfind(self, algorithm):
        '''Picks the pathfinding algorithm used.'''
        if algorithm == "A*":
            self.worker = self.a_star()
        elif algorithm == "Dijkstra":
            self.worker = self.dijkstra()
        elif algorithm == "D*":
            self.worker = self.d_star()
        elif algorithm == "Reset":
            self.reset()
            return

        self.animate()

    def animate(self):
        '''Animates the pathfinding.'''
        if self.worker != None:
            try:
                next(self.worker)
                self.window.after(self.SPEED, self.animate)
            except StopIteration:
                self.worker = None
            finally:
                self.window.after_cancel(self.animate)

    def a_star(self):
        # TODO
        return

    def dijkstra(self):
        # TODO
        return

    def d_star(self):
        # TODO
        return

    def reset(self):
        '''Resets the grid to it's starting point.'''
        for row_ind, row in enumerate(self.square_types):
            for col_ind, column in enumerate(row):
                if column != 0:
                    self.canvas.itemconfig(
                        self.squares[row_ind][col_ind], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)
                    self.square_types[row_ind][col_ind] = 0


if __name__ == "__main__":
    Visualizer()
