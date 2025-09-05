
import tkinter as tk
import random

def create_gui():
  root = tk.Tk()
  root.title("Blackjack Simulator")

  # --- GUI Elements ---
  # Label and Entry for Player's Bet
  bet_label = tk.Label(root, text="Player's Bet:")
  bet_label.pack()
  bet_entry = tk.Entry(root)
  bet_entry.pack()

  # Label and Entry for Player's Hand
  hand_label = tk.Label(root, text="Player's Hand:")
  hand_label.pack()
  hand_entry = tk.Entry(root)
  hand_entry.pack()

  # Label and Entry for Dealer's Hand
  dealer_label = tk.Label(root, text="Dealer's Hand:")
  dealer_label.pack()
  dealer_entry = tk.Entry(root)
  dealer_entry.pack()

  # Buttons
  hit_button = tk.Button(root, text="Hit", command=lambda: print("Hit Button Clicked"))
  hit_button.pack()
  stand_button = tk.Button(root, text="Stand", command=lambda: print("Stand Button Clicked"))
  stand_button.pack()

  return root