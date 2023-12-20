import tkinter as tk
from tkinter import messagebox
import random

POPULATION_SIZE = 100
MUTATION_RATE = 0.2
MAX_GENERATIONS = 5000

def initialize_board(board_size):
    return [[0] * board_size for _ in range(board_size)]

def generate_random_tour(board_size, start_position):
    tour = [start_position]
    visited = set(tour)
    for _ in range(1, board_size * board_size):
        current_position = tour[-1]
        possible_moves = get_possible_moves(current_position, board_size)
        valid_moves = [move for move in possible_moves if move not in visited]

        if not valid_moves:
            break  # No valid moves left

        chosen_move = random.choice(valid_moves)
        tour.append(chosen_move)
        visited.add(chosen_move)

    return tour

def get_possible_moves(position, board_size):
    x, y = position
    moves = [
        (x + 1, y + 2), (x + 1, y - 2), (x - 1, y + 2), (x - 1, y - 2),
        (x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1)
    ]
    return [(i, j) for i, j in moves if 0 <= i < board_size and 0 <= j < board_size]

def calculate_fitness(tour):
    return len(set(tour))

def crossover(parent1, parent2, board_size):
    crossover_point = random.randint(0, board_size * board_size - 1)
    child = parent1[:crossover_point] + [square for square in parent2 if square not in parent1[:crossover_point]]
    return child

def mutate(tour, board_size):
    if random.random() < MUTATION_RATE:
        idx1, idx2 = random.sample(range(board_size * board_size), 2)
        if 0 <= idx1 < len(tour) and 0 <= idx2 < len(tour):
            tour[idx1], tour[idx2] = tour[idx2], tour[idx1]
    return tour

class KnightTourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knight's Tour Genetic Algorithm")
        self.root.board_size_label = tk.Label(self.root, text="Board Size:")
        self.root.board_size_entry = tk.Entry(self.root)
        self.root.start_position_label = tk.Label(self.root, text="Starting Position (row column):")
        self.root.start_position_entry = tk.Entry(self.root)
        self.root.start_button = tk.Button(self.root, text="Start Knight's Tour", command=self.run_genetic_algorithm)
        self.root.reset_button = tk.Button(self.root, text="Reset", command=self.reset_board)
        self.generation_label = tk.Label(root, text="Generation: 0")

        self.generation_label.pack()
        self.root.board_size_label.pack()
        self.root.board_size_entry.pack()
        self.root.start_position_label.pack()
        self.root.start_position_entry.pack()
        self.root.start_button.pack()
        self.root.reset_button.pack()
        self.root.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.root.canvas.pack()

    def draw_tour(self, tour, board_size):
        cell_size = max(400 // board_size, 40)
        canvas_width = board_size * cell_size
        canvas_height = board_size * cell_size
        self.root.canvas.config(width=canvas_width, height=canvas_height)
        for i in range(board_size):
            for j in range(board_size):
                color = "white" if (i + j) % 2 == 0 else "black"
                x0, y0 = j * cell_size, i * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                self.root.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

        for count, (x, y) in enumerate(tour, start=1):  # Start counting from 1
            x_pixel, y_pixel = x * cell_size + cell_size // 2, y * cell_size + cell_size // 2
            self.root.canvas.create_text(x_pixel, y_pixel, text=str(count), fill="red", font=("Helvetica", 10, "bold"))

        self.root.update()

    def run_genetic_algorithm(self):
        try:
            board_size = int(self.root.board_size_entry.get())
            start_position = tuple(map(int, self.root.start_position_entry.get().split())) or (0, 0)

            if board_size < 5:
                messagebox.showinfo("Error", "Please enter a board size greater than or equal to 5.")
                return

            if not (0 <= start_position[0] < board_size and 0 <= start_position[1] < board_size):
                messagebox.showinfo("Error", "Invalid starting position. Please enter a valid position.")
                return

            for generation in range(1, MAX_GENERATIONS + 1):
                population = [generate_random_tour(board_size, start_position) for _ in range(POPULATION_SIZE)]
                population = sorted(population, key=lambda x: calculate_fitness(x), reverse=True)

                if calculate_fitness(population[0]) == board_size * board_size:
                    print(f"Solution found in generation {generation}")
                    print(population[0])
                    self.draw_tour(population[0], board_size)
                    break

                elite = population[:10]
                offspring = []

                while len(offspring) < POPULATION_SIZE - len(elite):
                    parent1, parent2 = random.sample(elite, 2)
                    child = crossover(parent1, parent2, board_size)
                    child = mutate(child, board_size)
                    offspring.append(child)

                population = elite + offspring

                if generation % 10 == 0:
                    self.generation_label.config(text=f"Generation: {generation}")
                    self.draw_tour(population[0], board_size)

        except ValueError:
            messagebox.showinfo("Error", "Invalid input. Please enter valid numeric values.")

    def reset_board(self):
        self.root.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = KnightTourGUI(root)
    root.mainloop()
