import tkinter as tk
from tkinter import messagebox, scrolledtext
import solver
from data_visualizer import DataVisualizationOverlay

COLORS = {
    "background": "#121213",
    "text": "#ffffff",
    "empty_tile": "#3a3a3c",
    "grey_tile": "#3a3a3c",
    "yellow_tile": "#b59f3b",
    "green_tile": "#538d4e",
    "keyboard_key": "#818384",
    "used_key": "#3a3a3c",
    "border": "#3a3a3c",
    "highlight": "#565758",
    "button_text": "#000000"
}

class WordleSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Solver")
        self.root.config(bg=COLORS["background"])
        self.root.geometry("1280x720")
        
        solver.fetchWords('all-answers.csv')
        
        self.current_row = 0
        self.current_col = 0
        self.tiles = []
        self.current_guesses = []
        self.position_values = []
        self.current_focused_widget = None
        self.guess_validated = False
        self.data_overlay = None
        
        self.container = tk.Frame(root, bg=COLORS["background"])
        self.container.pack(expand=True)
        
        self.main_frame = tk.Frame(self.container, bg=COLORS["background"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.create_header()
        self.create_directions()
        self.create_left_panel()
        self.create_game_board()
        self.create_right_panel()
        self.create_data_button()
        self.create_reset_button()
        
        self.update_word_statistics()
        
        self.root.bind("<Key>", self.key_pressed)
        self.root.bind("<Button-1>", self.check_focus_area)
        
        self.update_directions("Please enter a valid word and press RETURN/ENTER")
    
    def create_header(self):
        tk.Label(
            self.main_frame, 
            text="WORDLE SOLVER", 
            font=('Inter', 30, 'bold'), 
            bg=COLORS["background"], 
            fg=COLORS["text"]
        ).grid(row=0, column=0, columnspan=3, pady=(0, 10))
    
    def create_directions(self):
        self.directions_frame = tk.Frame(
            self.main_frame,
            bg=COLORS["background"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=10,
            pady=5
        )
        self.directions_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, pady=(0, 20))
        
        self.directions_label = tk.Label(
            self.directions_frame,
            text="",
            font=('Inter', 12),
            bg=COLORS["background"],
            fg=COLORS["text"],
            wraplength=1000,
            justify="center"
        )
        self.directions_label.pack(fill=tk.X)
    
    def update_directions(self, text):
        self.directions_label.config(text=text)
    
    def create_left_panel(self):
        left_panel = tk.Frame(self.main_frame, bg=COLORS["background"])
        left_panel.grid(row=2, column=0, sticky="ns", padx=(0, 20))
        
        self.remaining_words_label = tk.Label(
            left_panel,
            text=f"Possible Words: {len(solver.possible_words)}",
            font=('Inter', 14, 'bold'),
            bg=COLORS["background"],
            fg=COLORS["text"]
        )
        self.remaining_words_label.pack(pady=(0, 10))
        
        tk.Label(
            left_panel,
            text="Best Next Words:",
            font=('Inter', 14, 'bold'),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(pady=(0, 5))
        
        self.word_suggestions = scrolledtext.ScrolledText(
            left_panel,
            width=25,
            height=25,
            font=('Courier', 12),
            bg=COLORS["background"],
            fg=COLORS["text"],
            bd=1,
            relief="solid",
            borderwidth=1
        )
        self.word_suggestions.pack(fill=tk.BOTH, expand=True)
        
        left_panel.bind("<Button-1>", lambda event: self.set_focus("game"))
    
    def create_game_board(self):
        game_board = tk.Frame(self.main_frame, bg=COLORS["background"])
        game_board.grid(row=2, column=1, sticky="nsew")
        
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.columnconfigure(2, weight=1)
        
        self.grid_frame = tk.Frame(game_board, bg=COLORS["background"])
        self.grid_frame.pack(expand=True)
        
        for row in range(6):
            self.tiles.append([])
            self.current_guesses.append([" "] * 5)
            self.position_values.append([0] * 5)
            
            for col in range(5):
                tile_frame = tk.Frame(
                    self.grid_frame,
                    width=60,
                    height=60,
                    bg=COLORS["background"],
                    highlightbackground=COLORS["border"],
                    highlightthickness=2
                )
                tile_frame.grid(row=row, column=col, padx=5, pady=5)
                tile_frame.grid_propagate(False)
                
                tile_label = tk.Label(
                    tile_frame,
                    text="",
                    font=('Inter', 24, 'bold'),
                    bg=COLORS["background"],
                    fg=COLORS["text"]
                )
                tile_label.place(relx=0.5, rely=0.5, anchor="center")
                
                tile_frame.bind("<Button-1>", lambda event, r=row, c=col: self.cycle_tile_color(r, c))
                
                self.tiles[row].append((tile_frame, tile_label))
        
        self.grid_frame.bind("<Button-1>", lambda event: self.set_focus("game"))
        game_board.bind("<Button-1>", lambda event: self.set_focus("game"))
    
    def create_data_button(self):
        data_button_frame = tk.Frame(self.main_frame, bg=COLORS["background"])
        data_button_frame.grid(row=3, column=1, sticky="n", pady=(20, 0))
        
        tk.Button(
            data_button_frame,
            text="Look at possible word data",
            font=('Inter', 12),
            bg=COLORS["keyboard_key"],
            fg=COLORS["button_text"],
            command=self.show_data_overlay
        ).pack()
    
    def show_data_overlay(self):
        if len(solver.possible_words) > 0:
            data = solver.fetchData(solver.possible_words)
            self.data_overlay = DataVisualizationOverlay(self.root, data, solver.possible_words, self.hide_data_overlay)
        else:
            messagebox.showinfo("No Data", "No possible words available to analyze.")
    
    def hide_data_overlay(self):
        if self.data_overlay:
            self.data_overlay.destroy()
            self.data_overlay = None
    
    def create_right_panel(self):
        right_panel = tk.Frame(self.main_frame, bg=COLORS["background"])
        right_panel.grid(row=2, column=2, sticky="ns", padx=(20, 0))
        
        tk.Label(
            right_panel,
            text="Find Filler Words",
            font=('Inter', 14, 'bold'),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(pady=(0, 10))
        
        tk.Label(
            right_panel,
            text="Enter up to 5 unique letters:",
            font=('Inter', 12),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(pady=(0, 5))
        
        self.filler_entry = tk.Entry(
            right_panel,
            font=('Inter', 14),
            width=15,
            bg=COLORS["background"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"]
        )
        self.filler_entry.pack(pady=(0, 10))
        
        self.filler_entry.bind("<FocusIn>", lambda event: self.set_focus("filler"))
        
        tk.Button(
            right_panel,
            text="Search",
            font=('Inter', 12),
            bg=COLORS["keyboard_key"],
            fg=COLORS["button_text"],
            command=self.search_filler_words
        ).pack(pady=(0, 10))
        
        self.filler_results = scrolledtext.ScrolledText(
            right_panel,
            width=25,
            height=20,
            font=('Courier', 12),
            bg=COLORS["background"],
            fg=COLORS["text"],
            bd=1,
            relief="solid",
            borderwidth=1
        )
        self.filler_results.pack(fill=tk.BOTH, expand=True)
        
        right_panel.bind("<Button-1>", lambda event: self.check_click_source(event, "right_panel"))
        self.filler_results.bind("<Button-1>", lambda event: self.check_click_source(event, "filler_results"))
    
    def create_reset_button(self):
        reset_frame = tk.Frame(self.main_frame, bg=COLORS["background"])
        reset_frame.grid(row=3, column=2, sticky="se", pady=(20, 0))
        
        tk.Button(
            reset_frame,
            text="Reset Game",
            font=('Inter', 12),
            bg=COLORS["keyboard_key"],
            fg=COLORS["button_text"],
            command=self.reset_game
        ).pack()

    def check_focus_area(self, event):
        widget = event.widget
        if widget in [self.root, self.container, self.main_frame]:
            self.set_focus("game")
    
    def check_click_source(self, event, source):
        if source in ["filler_results", "word_suggestions"]:
            return "break"
        elif source == "right_panel":
            widget = event.widget
            if widget != self.filler_entry and widget != self.filler_results:
                self.set_focus("game")
        
    def set_focus(self, widget_name):
        self.current_focused_widget = widget_name
        self.filler_entry.focus_set() if widget_name == "filler" else self.root.focus_set()
        
        self.filler_entry.config(
            highlightbackground=COLORS["highlight" if widget_name == "filler" else "border"], 
            highlightthickness=2
        )
    
    def key_pressed(self, event):
        if self.current_focused_widget == "filler" or self.current_row >= 6:
            return
            
        key = event.char.lower()
        
        if event.keysym == "BackSpace":
            self.handle_backspace()
        elif event.keysym == "Return":
            self.handle_enter()
        elif key.isalpha() and len(key) == 1:
            self.handle_letter(key)
    
    def handle_letter(self, letter):
        if self.current_col < 5 and not self.guess_validated:
            _, label = self.tiles[self.current_row][self.current_col]
            label.config(text=letter.upper())
            
            self.current_guesses[self.current_row][self.current_col] = letter
            
            self.current_col += 1
    
    def handle_backspace(self):
        if self.current_col > 0 and not self.guess_validated:
            self.current_col -= 1
            
            _, label = self.tiles[self.current_row][self.current_col]
            label.config(text="")
            
            self.current_guesses[self.current_row][self.current_col] = " "
    
    def handle_enter(self):
        if not self.guess_validated and self.current_col == 5:
            current_word = ''.join(self.current_guesses[self.current_row])
            
            if not solver.validInput(current_word):
                self.update_directions("That is not a valid word, Try Again!")
                return
            
            self.guess_validated = True
            self.update_directions("Click on each tile to set the appropriate color (grey, yellow, green), then press RETURN/ENTER when done")
            
            for col in range(5):
                frame, label = self.tiles[self.current_row][col]
                frame.config(bg=COLORS["grey_tile"])
                label.config(bg=COLORS["grey_tile"])
                self.position_values[self.current_row][col] = 0
                
            return
        
        elif self.guess_validated:
            self.process_guess()
            return
    
    def cycle_tile_color(self, row, col):
        if row != self.current_row or not self.guess_validated:
            return
            
        frame, label = self.tiles[row][col]
        current_value = self.position_values[row][col]
        
        new_value = (current_value + 1) % 3
        self.position_values[row][col] = new_value
        
        color_map = {0: COLORS["grey_tile"], 1: COLORS["yellow_tile"], 2: COLORS["green_tile"]}
        frame.config(bg=color_map[new_value])
        label.config(bg=color_map[new_value])
    
    def process_guess(self):
        current_word = ''.join(self.current_guesses[self.current_row])
        position_values = self.position_values[self.current_row]
        
        solver.filterWords(current_word, position_values)
        
        self.update_word_statistics()
        
        if len(solver.possible_words) == 1:
            messagebox.showinfo("Solution Found", f"The answer is: {solver.possible_words[0]}")
            self.update_directions(f"Solution Found! The answer is: {solver.possible_words[0]}")
        elif len(solver.possible_words) == 0:
            messagebox.showerror("No Solutions", "No words match your criteria. Please check your inputs.")
            self.update_directions("No words match your criteria. Please check your inputs or reset the game.")
            solver.reset()
            self.update_word_statistics()
        else:
            self.update_directions("Please enter a valid word and press RETURN/ENTER")
        
        self.current_row += 1
        self.current_col = 0
        self.guess_validated = False
        
        if self.current_row >= 6:
            if len(solver.possible_words) > 1:
                possibilities = ", ".join(solver.possible_words[:5])
                if len(solver.possible_words) > 5:
                    possibilities += f", and {len(solver.possible_words) - 5} more"
                messagebox.showinfo("Game Over", f"Possible answers: {possibilities}")
                self.update_directions(f"Game Over! Possible answers include: {possibilities}")
    
    def update_word_statistics(self):
        self.remaining_words_label.config(text=f"Possible Words: {len(solver.possible_words)}")
        
        data = solver.fetchData(solver.possible_words)
        best_words = solver.bestNextWords(len(solver.possible_words), data)
        
        self.word_suggestions.config(state=tk.NORMAL)
        self.word_suggestions.delete(1.0, tk.END)
        
        for i, (word, score) in enumerate(best_words):
            self.word_suggestions.insert(tk.END, f"{i+1}. {word} (Score: {score})\n")
        
        self.word_suggestions.config(state=tk.DISABLED)
    
    def search_filler_words(self):
        letters = self.filler_entry.get().lower()
        
        if not letters.isalpha():
            messagebox.showerror("Invalid Input", "Please enter letters only.")
            return
        
        unique_letters = ''.join(sorted(set(letters)))
        if len(unique_letters) > 5:
            messagebox.showerror("Too Many Letters", "Please enter up to 5 unique letters.")
            return
        
        filler_words = solver.findFillerWords(unique_letters)
        
        self.filler_results.config(state=tk.NORMAL)
        self.filler_results.delete(1.0, tk.END)
        
        self.filler_results.insert(tk.END, "No words found." if not filler_words else "\n".join(filler_words))
        
        self.filler_results.config(state=tk.DISABLED)
        
        self.set_focus("game")
    
    def reset_game(self):
        solver.reset()
        
        self.current_row = 0
        self.current_col = 0
        self.guess_validated = False
        
        for row in range(6):
            self.current_guesses[row] = [" "] * 5
            self.position_values[row] = [0] * 5
            
            for col in range(5):
                frame, label = self.tiles[row][col]
                frame.config(bg=COLORS["background"])
                label.config(bg=COLORS["background"], text="")
        
        self.update_word_statistics()
        
        self.update_directions("Please enter a valid word and press RETURN/ENTER")
        
        self.filler_entry.delete(0, tk.END)
        self.filler_results.config(state=tk.NORMAL)
        self.filler_results.delete(1.0, tk.END)
        self.filler_results.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = WordleSolverGUI(root)

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    app.set_focus("game")
    root.mainloop()