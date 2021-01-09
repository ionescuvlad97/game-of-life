import tkinter as tk
import random
import time

class GameOfLife(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.width = 1000
        self.height = 650
        self.cell_dim = 25
        self.canvas_bg = "white"

        self.running = True

        self.pack()
        self.create_widgets()

        self.cells = [[Cell(i, j, i+self.cell_dim, j+self.cell_dim)
                       for i in range(0, self.width, self.cell_dim)]
                       for j in range(0, self.height, self.cell_dim)]

    def create_widgets(self):
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=3)
        self.master.columnconfigure(2, weight=1)

        self.canvas = tk.Canvas(self,
                                width=self.width,
                                height=self.height,
                                bg=self.canvas_bg)
        self.draw_grid()
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.random_setup_btn = tk.Button(self, text="Random setup",
                                command=self.setup_random_cells)
        self.random_setup_btn.grid(row=1, column=0, sticky="NSEW")

        self.start_btn = tk.Button(self, text="Start",
                                command=self.start_game)
        self.start_btn.grid(row=1, column=1, sticky="NSEW")

        self.stop_btn = tk.Button(self, text="Stop",
                                command=self.stop_game)
        self.stop_btn.grid(row=1, column=2, sticky="NSEW")

        self.quit_btn = tk.Button(self, text="Quit", fg="red",
                                  command=self.master.destroy)
        self.quit_btn.grid(row=2, column=0, columnspan=3, sticky="NSEW")

        self.canvas.bind('<Button 1>', self.getCellBoundaries)

    def draw_grid(self):
        for i in range(self.cell_dim, self.width, self.cell_dim):
            self.canvas.create_line(i, 0, i, self.height, fill="lightgray")
        for i in range(self.cell_dim, self.height, self.cell_dim):
            self.canvas.create_line(0, i, self.width, i, fill="lightgray")

    def print_cells_state(self, cells):
        for line in cells:
            for cell in line:
                print(cell.state, end = " ")
            print()
        print()

    def set_cells_random_state(self):
        for line in self.cells:
            for cell in line:
                cell.state = random.randint(0, 1)
        self.print_cells_state(self.cells)

        # self.cells[1][0].state = 1
        # self.cells[1][1].state = 1
        # self.cells[1][2].state = 1


    def draw_cells(self, cells):
        for line in cells:
            for cell in line:
                if cell.state == 1:
                    cell.rectangle_object = self.canvas.create_rectangle(
                                                    cell.x1 + 2, cell.y1 + 2,
                                                    cell.x2 - 2, cell.y2 - 2,
                                                    fill="black")
        self.canvas.update()

    def clear_drawn_cells(self, cells):
        for line in cells:
            for cell in line:
                self.canvas.delete(cell.rectangle_object)

    def setup_random_cells(self):
        self.clear_drawn_cells(self.cells)
        self.set_cells_random_state()
        self.draw_cells(self.cells)

    def neighbors(self, radius, rowNumber, columnNumber, cells):
        states = [[cell.state for cell in line] for line in cells]
        sum = 0
        for i in range(rowNumber-1, rowNumber+1+radius):
            for j in range(columnNumber-1, columnNumber+1+radius):
                if i >= 0 and i < len(states) and j >=0 and j < len(states[0]):
                    if states[i][j] == 1:
                        sum += 1
        if states[rowNumber][columnNumber] == 1:
            sum -= 1
        return sum

    def play_game(self):
        if self.running:
            new_cells = [[Cell(i, j, i+self.cell_dim, j+self.cell_dim)
                           for i in range(0, self.width, self.cell_dim)]
                           for j in range(0, self.height, self.cell_dim)]
            for line_index, line in enumerate(self.cells):
                for cell_index, cell in enumerate(line):
                    number_of_neighbors = self.neighbors(1, line_index, cell_index, self.cells)
                    print(line_index, cell_index)
                    print(number_of_neighbors)
                    if cell.state == 1 and (number_of_neighbors < 2 or number_of_neighbors > 3):
                        new_cells[line_index][cell_index].state = 0
                    elif cell.state == 0 and number_of_neighbors == 3:
                        new_cells[line_index][cell_index].state = 1
                    else:
                        new_cells[line_index][cell_index].state = cell.state
            print()
            self.clear_drawn_cells(self.cells)
            self.draw_cells(new_cells)
            self.cells = new_cells
            self.master.after(500, self.play_game)

    def start_game(self):
        self.running = True
        self.play_game()

    def stop_game(self):
        self.running = False

    def allow_coords(self):
        self.canvas.bind('<Motion>', self.motion)

    def motion(self, event):
        x, y = event.x, event.y

    def setup_cells(self):
        # set cell state
        # create the rectangle associated with that cell
        #
        cell.rectangle_object = self.canvas.create_rectangle(
                                        cell.x1 + 2, cell.y1 + 2,
                                        cell.x2 - 2, cell.y2 - 2,
                                        fill="black")

    def getorigin(self, eventorigin):
          return (eventorigin.x, eventorigin.y)

    def getCellBoundaries(self, eventorigin):
        x = eventorigin.x
        y = eventorigin.y

        x2 = x + self.cell_dim - x % self.cell_dim
        y2 = y + self.cell_dim - y % self.cell_dim

        x1 = x2 - self.cell_dim
        y1 = y2 - self.cell_dim

        print('({}, {}) -> ({}, {}) ({}, {})'.format(x, y, x1, y1, x2, y2))
        return (x1, y1, x2, y2)


class Cell:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.state = 0
        self.rectangle_object = None

def main():
    root = tk.Tk()
    app = GameOfLife(master=root)
    root.mainloop()

if __name__ == '__main__':
    main()
