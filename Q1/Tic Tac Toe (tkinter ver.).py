import tkinter as tk
import random

# Sound Import
try:
    import winsound
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Ultimate")
        self.root.geometry("480x680") 
        self.root.resizable(False, False)

        # Game State
        self.turn = 'X'
        self.starter = 'X' 
        self.board = [" " for _ in range(9)]
        self.game_mode = "PvP"
        self.game_active = False
        self.current_theme = "Dark"

        # Scores
        self.score_x = 0
        self.score_o = 0
        self.score_draw = 0

        # Theme Config
        self.themes = {
            "Dark": {
                "bg": "#1a1a2e",
                "grid_bg": "#16213e",    
                "frame_color": "#ffffff", # CHANGED: White frame for Dark Mode
                "text": "#ffffff",
                "btn_text": "#ffffff",
                "x_color": "#4cc9f0",
                "o_color": "#f72585",
                "taken_bg": "#0f3460",
                "win_highlight": "#39ff14",
                "menu_btn_bg": "#e94560",
                "overlay_bg": "#0f3460",
                "overlay_border": "#ffffff"
            },
            "Light": {
                "bg": "#ffffff",
                "grid_bg": "#e0e0e0",   
                "frame_color": "#000000", # CHANGED: Black frame for Light Mode
                "text": "#333333",
                "btn_text": "#333333",
                "x_color": "#007bff",   
                "o_color": "#dc3545",   
                "taken_bg": "#f8f9fa",  
                "win_highlight": "#28a745", 
                "menu_btn_bg": "#6c757d",
                "overlay_bg": "#f8f9fa",
                "overlay_border": "#000000"
            }
        }
        
        self.colors = self.themes[self.current_theme]

        # Fonts
        self.font_title = ("Verdana", 28, "bold")
        self.font_main = ("Verdana", 12)
        self.font_board = ("Verdana", 24, "bold")

        self.root.configure(bg=self.colors["bg"])
        self.show_main_menu()

    # --- Sound Engine ---
    def play_sound(self, sound_type):
        if not SOUND_ENABLED: return
        try:
            if sound_type == "click":
                winsound.Beep(600, 50) 
            elif sound_type == "win":
                for note in [523, 659, 784, 1046]: 
                    winsound.Beep(note, 100)
            elif sound_type == "draw":
                winsound.Beep(300, 300) 
        except:
            pass 

    # --- Theme Engine ---
    def toggle_theme(self):
        self.current_theme = "Light" if self.current_theme == "Dark" else "Dark"
        self.colors = self.themes[self.current_theme]
        self.apply_theme()

    def apply_theme(self):
        self.root.configure(bg=self.colors["bg"])
        
        if hasattr(self, 'grid_container') and self.grid_container.winfo_exists():
            # Update the frame color (Grid Lines)
            self.grid_container.config(bg=self.colors["frame_color"])

        if hasattr(self, 'status_label') and self.status_label.winfo_exists():
            self.status_label.config(bg=self.colors["bg"], fg=self.colors["text"])
            self.score_frame.config(bg=self.colors["bg"]) 
            self.label_x.config(bg=self.colors["bg"], fg=self.colors["x_color"])
            self.label_o.config(bg=self.colors["bg"], fg=self.colors["o_color"])
            self.label_d.config(bg=self.colors["bg"], fg=self.colors["text"])
            
            for i, btn in enumerate(self.buttons):
                current_text = self.board[i]
                if current_text == " ":
                    btn.config(bg=self.colors["grid_bg"])
                else:
                    p_color = self.colors["x_color"] if current_text == "X" else self.colors["o_color"]
                    btn.config(bg=self.colors["taken_bg"], disabledforeground=p_color)

        if hasattr(self, 'title_label') and self.title_label.winfo_exists():
            self.show_main_menu()

    # --- GUI Setup ---
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()
        self.game_active = False
        self.score_x = 0
        self.score_o = 0
        self.score_draw = 0
        self.starter = 'O' 

        title_frame = tk.Frame(self.root, bg=self.colors["bg"])
        title_frame.pack(pady=50)
        
        self.title_label = tk.Label(title_frame, text="TIC TAC TOE", font=self.font_title, 
                 bg=self.colors["bg"], fg=self.colors["x_color"])
        self.title_label.pack()

        menu_frame = tk.Frame(self.root, bg=self.colors["bg"])
        menu_frame.pack(pady=20)

        btn_style = {
            "font": self.font_main, "width": 20, "height": 2, "bd": 0, 
            "bg": self.colors["grid_bg"], "fg": self.colors["text"],
            "activebackground": self.colors["taken_bg"],
            "activeforeground": self.colors["text"]
        }

        tk.Button(menu_frame, text="Two Players", **btn_style, 
                  command=lambda: self.start_game("PvP")).pack(pady=8)
        
        tk.Button(menu_frame, text="Vs Computer (Easy)", **btn_style, 
                  command=lambda: self.start_game("Easy")).pack(pady=8)
        
        tk.Button(menu_frame, text="Vs Computer (Hard)", **btn_style, 
                  command=lambda: self.start_game("Hard")).pack(pady=8)

        tk.Button(menu_frame, text=f"Theme: {self.current_theme}", **btn_style,
                  command=self.toggle_theme).pack(pady=8)

        tk.Button(menu_frame, text="Exit", **btn_style, 
                  command=self.root.quit).pack(pady=8)

    def start_game(self, mode):
        self.game_mode = mode
        self.clear_window()
        self.setup_game_interface()
        self.reset_board()

    def setup_game_interface(self):
        # Scoreboard
        self.score_frame = tk.Frame(self.root, bg=self.colors["bg"], pady=10)
        self.score_frame.pack(fill="x")
        
        self.label_x = tk.Label(self.score_frame, text="", 
                                font=("Verdana", 12, "bold"), bg=self.colors["bg"], fg=self.colors["x_color"])
        self.label_x.pack(side="left", expand=True)
        
        self.label_d = tk.Label(self.score_frame, text="", 
                                font=("Verdana", 12), bg=self.colors["bg"], fg=self.colors["text"])
        self.label_d.pack(side="left", expand=True)
        
        self.label_o = tk.Label(self.score_frame, text="", 
                                font=("Verdana", 12, "bold"), bg=self.colors["bg"], fg=self.colors["o_color"])
        self.label_o.pack(side="left", expand=True)
        
        self.update_scores_label()

        # Status
        self.status_label = tk.Label(self.root, text="", font=("Verdana", 11), 
                                     bg=self.colors["bg"], fg=self.colors["text"], pady=15)
        self.status_label.pack()

        # Grid Container
        self.grid_container = tk.Frame(self.root, bg=self.colors["frame_color"], padx=3, pady=3)
        self.grid_container.pack(pady=10)

        self.buttons = []
        for i in range(9):
            btn = tk.Button(self.grid_container, text=" ", font=self.font_board, width=5, height=2, bd=0,
                            bg=self.colors["grid_bg"],
                            command=lambda i=i: self.on_click(i))
            
            # Using padx/pady to show the frame color underneath
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.buttons.append(btn)

        # Controls
        control_frame = tk.Frame(self.root, bg=self.colors["bg"])
        control_frame.pack(pady=20)

        ctrl_style = {"font": ("Verdana", 10, "bold"), "width": 12, "bd": 0, "bg": self.colors["menu_btn_bg"], "fg": "white"}
        
        tk.Button(control_frame, text="New Game", **ctrl_style, command=self.reset_board).pack(side="left", padx=10)
        tk.Button(control_frame, text="Main Menu", **ctrl_style, command=self.show_main_menu).pack(side="left", padx=10)

    # --- Game Logic ---
    def reset_board(self):
        self.board = [" " for _ in range(9)]
        self.game_active = True
        
        self.starter = 'O' if self.starter == 'X' else 'X'
        self.turn = self.starter

        self.update_status_text()
        
        for widget in self.grid_container.winfo_children():
            if isinstance(widget, tk.Frame): widget.destroy()

        for btn in self.buttons:
            btn.config(text=" ", state="normal", bg=self.colors["grid_bg"], relief="flat")
            btn.lift()

        if self.game_mode != "PvP" and self.turn == "O":
            self.root.after(800, self.computer_logic)

    def update_status_text(self):
        if self.game_mode == "PvP":
            txt = f"Turn: {self.turn}"
        else:
            txt = "Your Turn (X)" if self.turn == "X" else "Computer Thinking..."
        self.status_label.config(text=txt)

    def on_click(self, index):
        if not self.game_active or self.board[index] != " ": return
        if self.game_mode != "PvP" and self.turn != "X": return

        self.play_sound("click")
        self.make_move(index, self.turn)

        if self.game_active and self.game_mode != "PvP" and self.turn == "O":
            self.root.after(600, self.computer_logic)

    def make_move(self, index, player):
        self.board[index] = player
        
        p_color = self.colors["x_color"] if player == "X" else self.colors["o_color"]
        self.buttons[index].config(text=player, state="disabled", disabledforeground=p_color, bg=self.colors["taken_bg"])

        if self.check_winner(player):
            self.game_active = False
            self.play_sound("win")
            
            if player == "X": self.score_x += 1
            else: self.score_o += 1
            self.update_scores_label()
            
            self.animate_win(player)
        
        elif " " not in self.board:
            self.game_active = False
            self.play_sound("draw")
            self.score_draw += 1
            self.update_scores_label()
            self.status_label.config(text="Game Over: Draw")
            self.show_game_over_screen("It's a Draw!")
            
        else:
            self.turn = "O" if player == "X" else "X"
            self.update_status_text()

    def update_scores_label(self):
        if self.game_mode == "PvP":
            name_x, name_o = "Player X", "Player O"
        else:
            name_x, name_o = "You (X)", "CPU (O)"

        self.label_x.config(text=f"{name_x}: {self.score_x}")
        self.label_d.config(text=f"Draws: {self.score_draw}")
        self.label_o.config(text=f"{name_o}: {self.score_o}")

    def check_winner(self, player):
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] == player:
                self.winning_line = [a, b, c] 
                return True
        return False

    def animate_win(self, player):
        def flash(count):
            if count <= 0: 
                msg = f"Player {player} Wins!" if self.game_mode == "PvP" else ("You Win!" if player == "X" else "Computer Wins!")
                self.show_game_over_screen(msg)
                return
            
            is_highlight = (count % 2 != 0)
            color = self.colors["win_highlight"] if is_highlight else self.colors["taken_bg"]
            
            for i in self.winning_line:
                self.buttons[i].config(bg=color)
            
            self.root.after(200, lambda: flash(count - 1))

        flash(6)
        self.status_label.config(text=f"Winner: {player}")

    # --- Overlay System ---
    def show_game_over_screen(self, message):
        overlay = tk.Frame(self.grid_container, bg=self.colors["overlay_bg"], 
                           bd=3, relief="solid") 
        
        overlay.place(relx=0.5, rely=0.5, anchor="center", width=320, height=200)

        tk.Label(overlay, text="GAME OVER", font=("Verdana", 14, "bold"), 
                 bg=self.colors["overlay_bg"], fg=self.colors["text"]).pack(pady=(25, 5))
        
        tk.Label(overlay, text=message, font=("Verdana", 12), 
                 bg=self.colors["overlay_bg"], fg=self.colors["x_color"]).pack(pady=5)

        btn_style = {"font": ("Verdana", 10), "width": 15, "bd": 0, "fg": "white"}
        
        tk.Button(overlay, text="Play Again", bg=self.colors["menu_btn_bg"], **btn_style,
                  command=self.reset_board).pack(pady=10)
        
        tk.Button(overlay, text="Main Menu", bg="#555", **btn_style,
                  command=self.show_main_menu).pack(pady=5)

    # --- AI Logic ---
    def computer_logic(self):
        if not self.game_active: return
        avail = [i for i, x in enumerate(self.board) if x == " "]
        if not avail: return

        move = -1
        if self.game_mode == "Easy":
            move = random.choice(avail)
        elif self.game_mode == "Hard":
            move = self.find_best_move("O", avail)
            if move == -1: move = self.find_best_move("X", avail)
            if move == -1 and 4 in avail: move = 4
            if move == -1:
                corners = [c for c in [0,2,6,8] if c in avail]
                if corners: move = random.choice(corners)
            if move == -1: move = random.choice(avail)
            
        self.play_sound("click")
        self.make_move(move, "O")

    def find_best_move(self, player, avail):
        for i in avail:
            self.board[i] = player
            if self.check_winner(player):
                self.board[i] = " "
                return i
            self.board[i] = " "
        return -1

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()