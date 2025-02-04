import tkinter as tk
from tkinter import messagebox

PLAYER = 'X'
COMPUTER = 'O'

#
BG_COLOR = "#D9A066"  # Fond beige/orangé inspiré de l'image
GRID_COLOR = "black"  # Couleur de la grille
PLAYER_COLOR = "blue"  # Bleu pour le joueur
COMPUTER_COLOR = "red"  # Rouge pour l'ordinateur
TITLE_COLOR = "black"  # Couleur du titre en noir gras
BUTTON_COLOR = "white"  # Couleur des boutons


board = [[' ' for _ in range(3)] for _ in range(3)]

def reset_board():
    """Réinitialise le plateau de jeu."""
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=' ', state=tk.NORMAL, fg=GRID_COLOR, bg=BUTTON_COLOR)

def check_winner():
    """Vérifie s'il y a un gagnant."""
   
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
   
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
   
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    return None

def check_free_spaces():
    """Retourne le nombre de cases libres."""
    return sum(row.count(' ') for row in board)

def player_move(row, col):
    """Gère le mouvement du joueur."""
    if board[row][col] == ' ':
        board[row][col] = PLAYER
        buttons[row][col].config(text=PLAYER, fg=PLAYER_COLOR, state=tk.DISABLED)
        winner = check_winner()
        if winner == PLAYER:
            display_result("Vous avez gagné !")
            reset_board()
        elif check_free_spaces() == 0:
            display_result("Match nul !")
            reset_board()
        else:
            computer_move()

def computer_move():
    """Gère le mouvement de l'ordinateur."""
   
    move = can_win(COMPUTER)
    if move:
        row, col = move
    else:
        
        move = can_win(PLAYER)
        if move:
            row, col = move
        else:
        
            if board[1][1] == ' ':
                row, col = 1, 1
            else:
               
                corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
                for r, c in corners:
                    if board[r][c] == ' ':
                        row, col = r, c
                        break
                else:
                
                    sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
                    for r, c in sides:
                        if board[r][c] == ' ':
                            row, col = r, c
                            break

    board[row][col] = COMPUTER
    buttons[row][col].config(text=COMPUTER, fg=COMPUTER_COLOR, state=tk.DISABLED)
    winner = check_winner()
    if winner == COMPUTER:
        display_result("Vous avez perdu !")
        reset_board()
    elif check_free_spaces() == 0:
        display_result("Match nul !")
        reset_board()

def can_win(symbol):
    """Vérifie si un joueur peut gagner au prochain coup."""
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = symbol
                if check_winner() == symbol:
                    board[i][j] = ' '  
                    return (i, j)
                board[i][j] = ' '  
    return None

def display_result(message):
    """Affiche un message de résultat en gras et en grande taille."""
    result_window = tk.Toplevel(root)
    result_window.title("Résultat")
    result_label = tk.Label(result_window, text=message, font=('Arial', 24, 'bold'), fg="black")
    result_label.pack(pady=20)
    ok_button = tk.Button(result_window, text="OK", command=result_window.destroy, font=('Arial', 14))
    ok_button.pack(pady=10)


root = tk.Tk()
root.title("Tic-Tac-Toe")
root.configure(bg=BG_COLOR)


window_width = 600  
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")


title_label = tk.Label(
    root, text="Bienvenue dans le jeu Tic-Tac-Toe", font=('Arial', 16, 'bold'),
    fg=TITLE_COLOR, bg=BG_COLOR
)
title_label.grid(row=0, column=0, columnspan=3, pady=10)  # Titre en haut


buttons = [[None for _ in range(3)] for _ in range(3)]
for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(
            root, text=' ', font=('Arial', 20), width=5, height=2,
            command=lambda r=row, c=col: player_move(r, c),
            bg=BUTTON_COLOR, fg=GRID_COLOR, relief=tk.RAISED, borderwidth=2
        )
        buttons[row][col].grid(row=row + 1, column=col, padx=5, pady=5)

#
creator_label = tk.Label(
    root, text="Jeu créé par Amine El-baydaouy", font=('Arial', 14, 'bold'),
    fg="black", bg=BG_COLOR, relief=tk.SOLID, borderwidth=2
)
creator_label.grid(row=1, column=3, rowspan=1, padx=20, pady=10)  

description_label = tk.Label(
    root, text="Le jeu Tic-Tac-Toe consiste à aligner trois symboles identiques, soit en ligne, en colonne ou en diagonale. Le premier joueur à y parvenir gagne la partie. Bonne chance !",
    font=('Arial', 12), fg="dimgray", bg=BG_COLOR, wraplength=180, justify="left"
)
description_label.grid(row=2, column=3, rowspan=2, padx=20, pady=10, sticky="n")


thanks_label = tk.Label(
    root, text="Merci d'avoir joué !", font=('Arial', 14, 'italic'),
    fg="black", bg=BG_COLOR
)
thanks_label.grid(row=4, column=0, columnspan=4, pady=10)  


exit_button = tk.Button(
    root, text="EXIT", font=('Arial', 14), command=root.quit,
    bg="white", fg="black", relief=tk.FLAT
)
exit_button.grid(row=5, column=0, columnspan=4, pady=10, sticky="we")

reset_button = tk.Button(
    root, text="Réinitialiser", font=('Arial', 14), command=reset_board,
    bg=TITLE_COLOR, fg="white", relief=tk.FLAT
)
reset_button.grid(row=6, column=0, columnspan=4, pady=10, sticky="we")

root.mainloop()








