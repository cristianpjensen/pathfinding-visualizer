from tkinter import *
from tkinter import ttk


class Visualizer():
    """A GUI visualizer for various pathfinding methods."""

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

        self.SPEED = 10

        self.grid = list()
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
        self.create_button("Dijkstra")
        self.create_button("A*")
        self.create_button("DFS")
        self.create_button("Reset")

        self.window.bind("<Button-1>", self.colour_wall)
        self.window.bind("<B1-Motion>", self.colour_wall)
        self.window.bind("<Button-2>", self.colour_start_goal)
        self.window.bind("<Button-3>", self.colour_start_goal)

        self.window.mainloop()

    def create_grid(self):
        """Creates the grid, based on the constants already declared."""

        for column in range(self.COLUMNS):
            self.grid.append(list())
            self.maze.append(list())
            for row in range(self.ROWS):
                x1 = column * self.CELLWIDTH
                y1 = row * self.CELLHEIGHT
                x2 = x1 + self.CELLWIDTH
                y2 = y1 + self.CELLHEIGHT

                self.grid[column].append(self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=self.COLOUR_FREE, outline=self.COLOUR_FREE
                ))
                self.maze[column].append(0)

    def create_button(self, algorithm):
        """Creats a button, which is linked to the corresponding algorithm."""

        self.buttons.append(
            ttk.Button(
                self.window, text=algorithm, command=lambda: self.pathfind(
                    algorithm)
            ).pack(in_=self.top, side=LEFT)
        )

    def colour_wall(self, event):
        """Colours a wall, based on the x and y values of the mouse."""

        x = event.x // self.CELLWIDTH
        y = event.y // self.CELLHEIGHT

        # Return if the square wasn the previously selected, or out of bounds.
        if (x, y) == self.prev or x < 0 or y < 0:
            return

        # Inverse them, wall becomes free, free becomes wall.
        if self.maze[x][y] == 1:
            self.canvas.itemconfig(
                self.grid[x][y], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)
            self.maze[x][y] = 0
        else:
            self.canvas.itemconfig(
                self.grid[x][y], fill=self.COLOUR_WALL, outline=self.COLOUR_WALL)
            self.maze[x][y] = 1

        self.prev = x, y

    def colour_start_goal(self, event):
        """Colours the start or the end goal, based on the x and y values of the mouse."""

        x = event.x // self.CELLWIDTH
        y = event.y // self.CELLHEIGHT

        # If out of bounds, return.
        if x < 0 or y < 0:
            return

        # If the pressed square is `self.start` or `self.goal`, remove it.
        if (x, y) == self.start:
            self.canvas.itemconfig(
                self.grid[x][y], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)
            self.maze[x][y] = 0
            self.start = None
            return
        elif (x, y) == self.goal:
            self.canvas.itemconfig(
                self.grid[x][y], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)
            self.maze[x][y] = 0
            self.goal = None
            return

        # Determines if `self.start` or `self.goal` will be placed.
        if self.start != None:
            if self.goal == None:
                self.canvas.itemconfig(
                    self.grid[x][y], fill=self.COLOUR_GOAL, outline=self.COLOUR_GOAL)
                self.maze[x][y] = 3

                self.goal = x, y
        else:
            self.canvas.itemconfig(
                self.grid[x][y], fill=self.COLOUR_START, outline=self.COLOUR_START)
            self.maze[x][y] = 2

            self.start = x, y

    def pathfind(self, algorithm):
        """Picks the pathfinding algorithm used."""

        if algorithm == "A*":
            self.worker = self.a_star()
        elif algorithm == "Dijkstra":
            self.worker = self.dijkstra()
        elif algorithm == "DFS":
            self.worker = self.dfs()
        elif algorithm == "Reset":
            self.reset()
            return

        self.animate()

    def animate(self):
        """Animates the pathfinding."""

        if self.worker != None:
            try:
                next(self.worker)
                self.window.after(self.SPEED, self.animate)
            except StopIteration:
                self.worker = None
            finally:
                self.window.after_cancel(self.animate)

    def a_star(self):
        """Finds the best path, via the A* search algorithm."""

        self.window.title("A* search algorithm")

        dist = list()
        cost = list()
        open_list = list()
        closed_list = list()

        # Create a map of the distances and costs for each position.
        for row_ind, row in enumerate(self.maze):
            dist.append(list())
            cost.append(list())
            for column in range(len(row)):
                dist[row_ind].append(float("inf"))
                cost[row_ind].append(float("inf"))

        pos = self.start
        cost[pos[0]][pos[1]] = self.manhattan(pos)
        dist[pos[0]][pos[1]] = 0

        while True:
            x, y = pos
            closed_list.append(pos)

            # Colour explored, but keep the colour of start.
            if pos != self.start:
                self.canvas.itemconfig(
                    self.grid[x][y], fill=self.COLOUR_EXPLORED, outline=self.COLOUR_EXPLORED)
                yield

            for change in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nb_pos = pos[0] + change[0], pos[1] + change[1]
                x_nb, y_nb = nb_pos

                nb_dist = dist[x][y] + 1
                nb_cost = nb_dist + self.manhattan(nb_pos)

                # Ignore if not walkable.
                if (x_nb < 0 or x_nb > (self.ROWS - 1) or y_nb < 0 or y_nb > (self.COLUMNS - 1)
                        or self.maze[x_nb][y_nb] == 1):
                    continue

                # Stop when the position is the goal.
                if nb_pos == self.goal:
                    x_path, y_path = self.goal

                    # Backtrack.
                    while True:
                        minimum = float("inf")

                        # Get the neighbour with the least distance from the start.
                        for change in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                            x, y = x_path + change[0], y_path + change[1]

                            # Continue if not in closed list.
                            if (x, y) not in closed_list:
                                continue

                            if dist[x][y] < minimum:
                                minimum = dist[x][y]
                                x_min, y_min = x, y

                            if minimum == 0:
                                return

                        x_path, y_path = x_min, y_min

                        self.canvas.itemconfig(
                            self.grid[x_min][y_min], fill=self.COLOUR_PATH, outline=self.COLOUR_PATH)
                        yield

                if nb_cost < cost[x_nb][y_nb]:
                    cost[x_nb][y_nb] = nb_cost
                    dist[x_nb][y_nb] = nb_dist

                    # Append in a sorted manner.
                    if len(open_list) == 0:
                        open_list.append(nb_pos)
                    elif nb_cost > cost[open_list[-1][0]][open_list[-1][1]]:
                        open_list.append(nb_pos)
                    else:
                        for ind, position in enumerate(open_list):
                            if nb_cost <= cost[position[0]][position[1]]:
                                open_list.insert(ind, nb_pos)
                                break

            # Next position is the first in the open list = the smallest cost.
            pos = open_list.pop(0)
            closed_list.append(pos)

    def manhattan(self, coords):
        """Calculates the manhattan distance between the goal and the given coords."""

        x1, y1 = self.goal
        x2, y2 = coords

        return abs(x1 - x2) + abs(y1 - y2)

    def dijkstra(self):
        """Finds the best path, via Dijkstra's shortest path algorithm."""

        self.window.title("Dijkstra's algorithm")

        dist = list()
        frontier = list()

        # Create a map of the distances for each position.
        for row_ind, row in enumerate(self.maze):
            dist.append(list())
            for column in range(len(row)):
                dist[row_ind].append(float("inf"))

        pos = self.start
        dist[pos[0]][pos[1]] = 0

        while True:
            x, y = pos

            for change in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nb_pos = x + change[0], y + change[1]
                x_nb, y_nb = nb_pos

                nb_dist = dist[x][y] + 1

                # Ignore if outside of bounds, or a wall.
                if (x_nb < 0 or x_nb > (self.ROWS - 1) or y_nb < 0 or y_nb > (self.COLUMNS - 1)
                        or self.maze[x_nb][y_nb] == 1):
                    continue

                # Start has been found.
                if nb_pos == self.goal:
                    x_path, y_path = self.goal

                    # Backtrack.
                    while True:
                        minimum = float("inf")

                        # Get the neighbour with the least distance from the start.
                        for change in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                            x, y = x_path + change[0], y_path + change[1]

                            if dist[x][y] < minimum:
                                minimum = dist[x][y]
                                x_min, y_min = x, y

                            if minimum == 0:
                                return

                        x_path, y_path = x_min, y_min

                        self.canvas.itemconfig(
                            self.grid[x_min][y_min], fill=self.COLOUR_PATH, outline=self.COLOUR_PATH)
                        yield

                # Only assign the new distance, if it is less than the old distance.
                if nb_dist < dist[x_nb][y_nb]:
                    dist[x_nb][y_nb] = nb_dist
                    self.canvas.itemconfig(
                        self.grid[x_nb][y_nb], fill=self.COLOUR_EXPLORED, outline=self.COLOUR_EXPLORED)
                    yield

                    frontier.append(nb_pos)

            pos = frontier.pop(0)

    def dfs(self):
        """Finds the best path, via the depth-first search search algorithm."""

        self.window.title("Depth-first search")

        order = list()
        frontier = list()
        closed_list = list()

        # Create a map of the distances for each position.
        for row_ind, row in enumerate(self.maze):
            order.append(list())
            for column in range(len(row)):
                order[row_ind].append(float("inf"))

        pos = self.start
        order[pos[0]][pos[1]] = 0

        while True:
            x, y = pos

            for change in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nb_pos = x + change[0], y + change[1]
                x_nb, y_nb = nb_pos

                nb_order = order[x][y] + 1

                # Ignore if outside of bounds, or a wall.
                if (x_nb < 0 or x_nb > (self.ROWS - 1) or y_nb < 0 or y_nb > (self.COLUMNS - 1)
                        or self.maze[x_nb][y_nb] == 1):
                    continue

                # Start has been found.
                if nb_pos == self.goal:
                    x_path, y_path = self.goal
                    prev = order[x_path][y_path]

                    # Backtrack.
                    while True:

                        # Get the neighbour with the least distance from the start.
                        for change in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                            x, y = x_path + change[0], y_path + change[1]

                            if x < 0 or x > (self.ROWS - 1) or y < 0 or y > (self.COLUMNS - 1):
                                continue

                            if (x, y) not in closed_list:
                                continue

                            if order[x][y] == (prev - 1):
                                print(order[x][y])
                                x_path, y_path = x, y

                            if order[x][y] == 0:
                                return

                        prev = order[x_path][y_path]

                        self.canvas.itemconfig(
                            self.grid[x_path][y_path], fill=self.COLOUR_PATH, outline=self.COLOUR_PATH)
                        yield

                # Only assign the new distance, if it is less than the old distance.
                if nb_order < order[x_nb][y_nb]:
                    order[x_nb][y_nb] = nb_order
                    self.canvas.itemconfig(
                        self.grid[x_nb][y_nb], fill=self.COLOUR_EXPLORED, outline=self.COLOUR_EXPLORED)
                    yield

                    frontier.insert(0, nb_pos)

            pos = frontier.pop(0)
            closed_list.append(pos)

    def reset(self):
        """Resets the grid to it's starting point."""

        self.window.title("Pathfinding Visualizer")

        for row_ind, row in enumerate(self.maze):
            for col_ind, column in enumerate(row):
                self.canvas.itemconfig(
                    self.grid[row_ind][col_ind], fill=self.COLOUR_FREE, outline=self.COLOUR_FREE)
                self.maze[row_ind][col_ind] = 0

        # Reset all variables.
        self.worker = None
        self.start = None
        self.goal = None


if __name__ == "__main__":
    Visualizer()
