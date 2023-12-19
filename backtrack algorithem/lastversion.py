

import tkinter as tk
from PIL import Image, ImageTk

class ChessKnight:
    def __init__(self, boardsize):
        self.boardsize = boardsize
        self.visited = [[-1 for _ in range(self.boardsize)] for _ in range(self.boardsize)]
        self.X = [2, 1, -1, -2, -2, -1, 1, 2]
        self.Y = [1, 2, 2, 1, -1, -2, -2, -1]

    def solveChessKnightTour(self, start_x, start_y):
        self.visited = [[-1 for _ in range(self.boardsize)] for _ in range(self.boardsize)]
        self.visited[start_x][start_y] = 0
        self.solveChessProblem(1, start_x, start_y)

    def countValidMoves(self, x, y):
        count = 0
        for i in range(len(self.X)):
            nextX = x + self.X[i]
            nextY = y + self.Y[i]
            if self.isValidChessMove(nextX, nextY) and self.visited[nextX][nextY] == -1:
                count += 1
        return count

    def solveChessProblem(self, moveCount, x, y):
        if moveCount == self.boardsize * self.boardsize:
            return True

        moves = [(self.X[i], self.Y[i]) for i in range(len(self.X))]
        moves.sort(key=lambda move: self.countValidMoves(x + move[0], y + move[1]))

        for i in moves:
            nextX = x + i[0]
            nextY = y + i[1]

            if self.isValidChessMove(nextX, nextY) and self.visited[nextX][nextY] == -1:
                self.visited[nextX][nextY] = moveCount
                if self.solveChessProblem(moveCount + 1, nextX, nextY):
                    return True

                self.visited[nextX][nextY] = -1

        return False

    def isValidChessMove(self, x, y):
        return not (x < 0 or x >= self.boardsize or y < 0 or y >= self.boardsize)

class KnightTourGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Knight's Tour")
        self.root.board_size_label = tk.Label(self.root, text="Board Size:")
        self.root.board_size_entry = tk.Entry(self.root)
        self.root.start_x_label = tk.Label(self.root, text="Position x:")
        self.root.start_x_entry = tk.Entry(self.root)
        self.root.start_y_label = tk.Label(self.root, text="Position y:")
        self.root.start_y_entry = tk.Entry(self.root)
        self.root.start_button = tk.Button(self.root, text="Start Knight's Tour", command=self.start_knight_tour)
        self.root.reset_button = tk.Button(self.root, text="Reset", command=self.reset_board)
        self.root.board_size_label.pack()
        self.root.board_size_entry.pack()
        self.root.start_x_label.pack()
        self.root.start_x_entry.pack()
        self.root.start_y_label.pack()
        self.root.start_y_entry.pack()
        self.root.start_button.pack()
        self.root.reset_button.pack()
        self.board_size = None
        self.board = None
        self.canvas_size = 50
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()
        self.solution_found = False
        self.chess_knight = ChessKnight(0)

    def start_knight_tour(self):
        self.reset_board()
        try:
            self.board_size = int(self.root.board_size_entry.get())
            start_x = int(self.root.start_x_entry.get())
            start_y = int(self.root.start_y_entry.get())

            if self.board_size < 5 or not (0 <= start_x < self.board_size) or not (0 <= start_y < self.board_size):
                raise ValueError("Invalid input values.")

            self.chess_knight = ChessKnight(self.board_size)
            self.chess_knight.solveChessKnightTour(start_x, start_y)
            self.board = self.chess_knight.visited
            self.display_knight_tour_gui()

        except ValueError as e:
            print(e)
            self.show_message("Invalid Input", "Invalid input values.")

    def reset_board(self):
        self.board = None
        self.canvas.delete("all")

    def display_knight_tour_gui(self):
        if self.board_size < 5:
            self.show_message("No Solution", "Board size is too small. Try a larger size.")
            return

        self.canvas.delete("all")

        canvas_width = len(self.board) * self.canvas_size
        canvas_height = len(self.board) * self.canvas_size
        self.canvas.config(width=canvas_width, height=canvas_height)

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                color = 'white' if (row + col) % 2 == 0 else 'black'
                self.canvas.create_rectangle(col * self.canvas_size, row * self.canvas_size,
                                              (col + 1) * self.canvas_size, (row + 1) * self.canvas_size,
                                              fill=color)

        for moveCount in range(0, self.board_size * self.board_size):
            x, y = self.get_position_by_move_count(moveCount)
            if x is not None and y is not None:
                # Display an image for the current cell
                current_image_path = "h.png" 
                current_image = Image.open(current_image_path)
                current_image = current_image.resize((self.canvas_size, self.canvas_size), Image.LANCZOS)
                current_image = ImageTk.PhotoImage(current_image)
                self.canvas.create_image((y + 0.5) * self.canvas_size, (x + 0.5) * self.canvas_size,
                                          image=current_image)

                if moveCount > 0:
                    prev_x, prev_y = self.get_position_by_move_count(moveCount - 1)
                    self.canvas.create_text((prev_y + 0.5) * self.canvas_size, (prev_x + 0.5) * self.canvas_size,
                                            text=str(moveCount), fill="red", font=("Helvetica", 12, "bold"))

                
                if moveCount == self.board_size * self.board_size - 1:
                    self.canvas.create_text((y + 0.5) * self.canvas_size, (x + 0.5) * self.canvas_size,
                                            text=str(moveCount + 1), fill="red", font=("Helvetica", 12, "bold"))

                self.root.update()
                self.root.after(500)

    def get_position_by_move_count(self, moveCount):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == moveCount:
                    return i, j
        return None, None

    def show_message(self, title, message):
        tk.messagebox.showinfo(title, message)


       
if __name__ == "__main__":
    gui = KnightTourGUI()
    gui.root.mainloop()
