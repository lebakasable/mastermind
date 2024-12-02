import tkinter as tk
from tkinter import messagebox
import itertools

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind")
        self.colors = ["Red", "Green", "Blue", "Yellow", "Orange", "Purple"]
        self.code = []
        self.guesses = []
        self.mode = tk.StringVar(value="Player vs Computer")
        self.create_widgets()
        self.possible_solutions = []
        self.current_guess = []

    def create_widgets(self):
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=10)

        tk.Label(mode_frame, text="Game Mode:").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(
            mode_frame, text="Player vs Computer", variable=self.mode, value="Player vs Computer", command=self.reset_game
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            mode_frame, text="Computer vs Player", variable=self.mode, value="Computer vs Player", command=self.reset_game
        ).pack(side=tk.LEFT)

        self.color_frame = tk.Frame(self.root)
        self.color_frame.pack(pady=10)

        self.color_buttons = []
        for color in self.colors:
            btn = tk.Button(
                self.color_frame, text=color, bg=color.lower(), command=lambda c=color: self.add_guess(c)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.color_buttons.append(btn)

        self.feedback_frame = tk.Frame(self.root)
        self.feedback_frame.pack(pady=10)

        self.feedback_label = tk.Label(self.feedback_frame, text="Make your guess!")
        self.feedback_label.pack()

        reset_button = tk.Button(self.feedback_frame, text="Reset", command=self.reset_game)
        reset_button.pack()

        self.reset_game()

    def reset_game(self):
        self.code = []
        self.guesses = []
        self.possible_solutions = list(itertools.product(self.colors, repeat=4))
        self.feedback_label.config(text="Game Reset! Make your guess.")
        
        self.enable_color_buttons()
        for btn in self.color_buttons:
            btn.config(command=lambda c=btn["text"]: self.add_guess(c))
        
        if self.mode.get() == "Player vs Computer":
            import random
            self.code = random.choices(self.colors, k=4)
            print(f"Debug: Computer's code is {self.code}")
        elif self.mode.get() == "Computer vs Player":
            self.start_computer_vs_player()

    def add_guess(self, color):
        if len(self.guesses) < 4:
            self.guesses.append(color)
        if len(self.guesses) == 4:
            self.check_guess()

    def check_guess(self):
        if self.guesses == self.code:
            messagebox.showinfo("Mastermind", "Congratulations! You guessed the code!")
            self.reset_game()
        else:
            feedback = self.get_feedback(self.guesses, self.code)
            self.feedback_label.config(text=f"Feedback: {feedback}")
            self.guesses = []

    def get_feedback(self, guess, code):
        blacks = sum([1 for i in range(4) if guess[i] == code[i]])
        whites = sum([min(guess.count(c), code.count(c)) for c in set(guess)]) - blacks
        return blacks, whites

    def start_computer_vs_player(self):
        self.feedback_label.config(text="Enter your secret code by selecting 4 colors.")
        self.code_entry = []
        self.enable_color_buttons()
        for btn in self.color_buttons:
            btn.config(command=lambda c=btn["text"]: self.add_code_color(c))

    def add_code_color(self, color):
        if len(self.code_entry) < 4:
            self.code_entry.append(color)
            self.feedback_label.config(text=f"Code so far: {self.code_entry}")
            if len(self.code_entry) == 4:
                self.code = self.code_entry
                self.feedback_label.config(text="Secret code set! Computer is guessing...")
                self.disable_color_buttons()
                self.root.after(1000, self.start_computer_guess)

    def start_computer_guess(self):
        self.current_guess = ("Red", "Red", "Green", "Green")
        self.feedback_label.config(text=f"Computer guesses: {self.current_guess}")
        self.root.after(1000, lambda: self.evaluate_computer_guess(self.current_guess))

    def evaluate_computer_guess(self, guess):
        feedback = self.get_feedback(guess, self.code)
        if feedback == (4, 0):
            messagebox.showinfo("Mastermind", f"Computer guessed the code: {guess}")
            self.reset_game()
            return

        self.possible_solutions = [
            solution
            for solution in self.possible_solutions
            if self.get_feedback(guess, solution) == feedback
        ]

        self.current_guess = self.possible_solutions[0]
        self.feedback_label.config(text=f"Computer guesses: {self.current_guess}")
        self.root.after(1000, lambda: self.evaluate_computer_guess(self.current_guess))

    def disable_color_buttons(self):
        for btn in self.color_buttons:
            btn.config(state=tk.DISABLED)

    def enable_color_buttons(self):
        for btn in self.color_buttons:
            btn.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()

