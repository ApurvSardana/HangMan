import tkinter as tk
from tkinter import messagebox, font
import subprocess
import time
import threading
import os
import sys

class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(background=self.cget("activebackground"))

    def on_leave(self, e):
        self.config(background=self.cget("background"))

class HangmanGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hangman Game")
        self.root.configure(bg="#1a1a2e")  # Dark blue background
        self.root.attributes('-fullscreen', True)
        
        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=48, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=24)
        self.letter_font = font.Font(family="Helvetica", size=36, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=16)
        
        # Initialize game files
        self.initialize_files()
        
        # Create UI elements
        self.create_ui()
        
        # Start game process
        self.game_process = None
        self.start_game()
        
        # Start UI update thread
        self.update_thread = threading.Thread(target=self.update_ui_loop, daemon=True)
        self.update_thread.start()
        
        # Bind escape key to exit
        self.root.bind('<Escape>', lambda e: self.quit_game())
        
    def initialize_files(self):
        """Initialize game files with proper permissions."""
        try:
            with open("input.txt", "w") as f:
                pass
            with open("game_state.txt", "w") as f:
                pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize game files: {str(e)}")
            sys.exit(1)
            
    def create_ui(self):
        """Create all UI elements."""
        # Main container with padding
        main_container = tk.Frame(self.root, bg="#1a1a2e", padx=40, pady=40)
        main_container.pack(expand=True, fill="both")
        
        # Title with gradient effect
        title_frame = tk.Frame(main_container, bg="#1a1a2e")
        title_frame.pack(pady=(0, 40))
        
        self.title_label = tk.Label(
            title_frame,
            text="HANGMAN",
            font=self.title_font,
            fg="#e94560",  # Vibrant red
            bg="#1a1a2e"
        )
        self.title_label.pack()
        
        # Game info frame
        info_frame = tk.Frame(main_container, bg="#1a1a2e")
        info_frame.pack(pady=(0, 30))
        
        self.turns_label = tk.Label(
            info_frame,
            text="Turns Left: 5",
            font=self.label_font,
            fg="#e94560",
            bg="#1a1a2e"
        )
        self.turns_label.pack()
        
        # Word display with custom styling
        self.word_frame = tk.Frame(main_container, bg="#1a1a2e")
        self.word_frame.pack(pady=30)
        
        # Initialize with empty list - will be populated when word is known
        self.letter_labels = []
            
        # Input area
        input_container = tk.Frame(main_container, bg="#1a1a2e")
        input_container.pack(pady=30)
        
        self.guess_entry = tk.Entry(
            input_container,
            font=self.letter_font,
            width=3,
            justify="center",
            bg="#16213e",  # Darker blue
            fg="white",
            insertbackground="white", 
            relief=tk.FLAT,
            bd=0
        )
        self.guess_entry.pack(side=tk.LEFT, padx=10)
        self.guess_entry.bind("<Return>", self.submit_guess)
        
        self.submit_button = ModernButton(
            input_container,
            text="GUESS",
            command=self.submit_guess,
            font=self.button_font,
            bg="#e94560",
            fg="white",
            activebackground="#ff6b81"
        )
        self.submit_button.pack(side=tk.LEFT, padx=10)
        
        # Control buttons
        control_frame = tk.Frame(main_container, bg="#1a1a2e")
        control_frame.pack(pady=20)
        
        self.restart_button = ModernButton(
            control_frame,
            text="NEW GAME",
            command=self.reset_game,
            font=self.button_font,
            bg="#0f3460",  # Dark blue
            fg="white",
            activebackground="#1f4287"
        )
        self.restart_button.pack(side=tk.LEFT, padx=10)
        
        self.exit_button = ModernButton(
            control_frame,
            text="EXIT",
            command=self.quit_game,
            font=self.button_font,
            bg="#e94560",
            fg="white",
            activebackground="#ff6b81"
        )
        self.exit_button.pack(side=tk.LEFT, padx=10)

    def create_letter_labels(self, word_length):
        """Create the exact number of letter labels needed for the word."""
        # Clear existing labels
        for label in self.letter_labels:
            label.destroy()
        self.letter_labels.clear()
        
        # Create new labels
        for _ in range(word_length):
            lbl = tk.Label(
                self.word_frame,
                text="_",
                font=self.letter_font,
                fg="white",
                bg="#16213e",  # Darker blue
                padx=15,
                pady=10,
                relief=tk.FLAT
            )
            lbl.pack(side=tk.LEFT, padx=5)
            self.letter_labels.append(lbl)
        
    def start_game(self):
        """Start the C++ game process."""
        try:
            self.game_process = subprocess.Popen(
                ["./hangman.exe"],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start game: {str(e)}")
            self.quit_game()
            
    def reset_game(self):
        """Reset the game state."""
        try:
            # Clear game files
            with open("input.txt", "w") as f:
                pass
            with open("game_state.txt", "w") as f:
                pass
                
            # Restart game process
            if self.game_process:
                self.game_process.terminate()
            self.start_game()
            
            # Reset UI
            for label in self.letter_labels:
                label.config(text="_")
            self.turns_label.config(text="Turns Left: 5")
            self.guess_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset game: {str(e)}")
            
    def submit_guess(self, event=None):
        """Submit a letter guess."""
        guess = self.guess_entry.get().strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Invalid Input", "Please enter a single letter!")
            return
            
        try:
            with open("input.txt", "w") as f:
                f.write(guess)
            self.guess_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit guess: {str(e)}")
            
    def update_ui_loop(self):
        """Continuously update the UI based on game state."""
        while True:
            try:
                with open("game_state.txt", "r") as f:
                    lines = f.readlines()
                    if len(lines) >= 3:
                        word, answer, turns = lines[0].strip(), lines[1].strip(), int(lines[2].strip())
                        
                        # Create letter labels if not already created or if word length changed
                        if len(self.letter_labels) != len(word):
                            self.create_letter_labels(len(word))
                        
                        # Update letter display
                        for i, letter in enumerate(answer):
                            if i < len(self.letter_labels):
                                self.letter_labels[i].config(text=letter)
                                
                        # Update turns with color change based on remaining turns
                        turns_color = "#e94560" if turns > 2 else "#ff6b81" if turns > 0 else "#ff4757"
                        self.turns_label.config(text=f"Turns Left: {turns}", fg=turns_color)
                        
                        # Check game over conditions
                        if turns == 0:
                            messagebox.showinfo("Game Over", f"You lost! The word was: {word}")
                            self.quit_game()
                            break
                        elif answer == word:
                            messagebox.showinfo("Victory!", "You guessed it right!")
                            self.quit_game()
                            break
                            
            except Exception as e:
                print(f"Error updating UI: {str(e)}")
                
            time.sleep(0.1)  # Update every 100ms
            
    def quit_game(self):
        """Clean up and exit the game."""
        if self.game_process:
            self.game_process.terminate()
        self.root.quit()
        
    def run(self):
        """Start the game."""
        self.root.mainloop()

if __name__ == "__main__":
    game = HangmanGame()
    game.run()