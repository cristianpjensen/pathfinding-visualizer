from tkinter import *
from tkinter import ttk


class Visualizer():
    '''A GUI visualizer for various pathfinding methods.'''

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

        self.SPEED = 1

        self.squares = list()
        self.maze = list()
        self.buttons = list()

        # Coordinates.
        self.start = None
        self.goal = None
        self.prev = None

        self.window = Tk()
        self.window.title("Pathfinding Visualizer")

        self.top = Frame(self.window)
        self.top.pack(side=TOP)

        self.canvas = Canvas(self.window, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack()

        self.create_grid()
        self.create_button("A*")
        self.create_button("Dijkstra")
        self.create_button("D*")
        self.create_button("Reset")

        self.window.bind("<Button-1>", self.colour_wall)
        self.window.bind("<B1-Motion>", self.colour_wall)
        self.window.bind("<Button-2>", self.colour_start_goal)
        self.window.bind("<Button-3>", self.colour_start_goal)

        self.window.mainloop()

    def create_grid(self):
        '''Creates the grid, based on the constants already declared.'''

        for column in range(self.COLUMNS):
            self.squares.append(list())
            self.maze.append(list())
            for row in range(self.ROWS):
                x1 = column * self.CELLWIDTH
                y1 = row * self.CELLHEIGHT
                x2 = x1 + self.CELLWIDTH
                y2 = y1 + self.CELLHEIGHT

                self.squares[column].append(self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=self.COLOUR_FREE, outline=self.COLOUR_FREE
                ))
                self.maze[column].append(0)

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

        # Return if the square wasn the previously selected.
        if (x, y) == self.prev or x < 0 or y < 0:
            return

        # Inverse them, wall > free, free > wall.
        if self.maze[x][y] == 1:
            self.canvas.itemconfig(
                self.squares[x][y], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)
            self.maze[x][y] = 0
        else:
            self.canvas.itemconfig(
                self.squares[x][y], fill=self.COLOUR_WALL, outline=self.COLOUR_WALL)
            self.maze[x][y] = 1

        self.prev = x, y

    def colour_start_goal(self, event):
        '''Colours the start or the end goal, based on the x and y values of the mouse.'''

        x = event.x // self.CELLWIDTH
        y = event.y // self.CELLHEIGHT

        # If out of bounds, return.
        if x < 0 or y < 0:
            return

        # If the pressed square is end or start, remove it.
        if (x, y) == self.start:
            self.canvas.itemconfig(
                self.squares[x][y], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)
            self.maze[x][y] = 0
            self.start = None
            return
        elif (x, y) == self.goal:
            self.canvas.itemconfig(
                self.squares[x][y], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)
            self.maze[x][y] = 0
            self.goal = None
            return

        # Determines if `self.start` or `self.goal` will be placed.
        if self.start != None:
            if self.goal == None:
                self.canvas.itemconfig(
                    self.squares[x][y], fill=self.COLOUR_GOAL, outline=self.COLOUR_GOAL)
                self.maze[x][y] = 3

                self.goal = x, y
        else:
            self.canvas.itemconfig(
                self.squares[x][y], fill=self.COLOUR_START, outline=self.COLOUR_START)
            self.maze[x][y] = 2

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
        '''Finds the best path, via the A* search algorithm.'''

        # TODO

        raise NotImplementedError

        self.window.title("A* search algorithm")

    def dijkstra(self):
        '''Finds the best path, via Dijkstra's shortest path algorithm.'''

        self.window.title("Dijkstra's algorithm")

        distances = list()

        for row_ind, row in enumerate(self.maze):
            distances.append(list())
            for column in range(len(row)):
                distances[row_ind].append(float("inf"))

        x_parent, y_parent = parent_position = self.start

        distances[x_parent][y_parent] = 0

        self.frontier = list()

        while True:
            x_parent, y_parent = parent_position

            for new_position in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                position = x_parent + \
                    new_position[0], y_parent + new_position[1]
                x, y = position

                distance = distances[x_parent][y_parent] + 1

                # Continue if outside of bounds.
                if x < 0 or x > (self.ROWS - 1) or y < 0 or y > (self.COLUMNS - 1):
                    continue

                # Continue if it is a wall.
                if self.maze[x][y] == 1:
                    continue

                # Stop if the start has been found.
                if (x, y) == self.goal:
                    x_path, y_path = self.goal

                    # Backtrack.
                    while True:
                        minimum = float("inf")

                        # Get the neighbour with the least distance from the start.
                        for child_position in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                            x_current, y_current = x_path + \
                                child_position[0], y_path + child_position[1]

                            if distances[x_current][y_current] < minimum:
                                minimum = distances[x_current][y_current]
                                x_min, y_min = x_current, y_current

                            if minimum == 0:
                                return

                        x_path, y_path = x_min, y_min

                        self.canvas.itemconfig(
                            self.squares[x_min][y_min], fill=self.COLOUR_PATH, outline=self.COLOUR_PATH)
                        yield

                # Only assign the new distance, if it is less than the old distance.
                if distance < distances[x][y]:
                    distances[x][y] = distance
                    self.canvas.itemconfig(
                        self.squares[x][y], fill=self.COLOUR_EXPLORED, outline=self.COLOUR_EXPLORED)
                    yield

                    self.frontier.append((x, y))

            parent_position = self.frontier.pop(0)

    def d_star(self):
        '''Finds the best path, via the D* search algorithm.'''

        # TODO

        raise NotImplementedError

        self.window.title("D* search algorithm")

    def reset(self):
        '''Resets the grid to it's starting point.'''

        self.window.title("Pathfinding Visualizer")

        for row_ind, row in enumerate(self.maze):
            for col_ind, column in enumerate(row):
                self.canvas.itemconfig(
                    self.squares[row_ind][col_ind], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)
                self.maze[row_ind][col_ind] = 0

        # Reset all variables.
        self.worker = None
        self.frontier = list()
        self.start = None
        self.goal = None


if __name__ == "__main__":
    Visualizer()
