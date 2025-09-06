import tkinter as tk

class Player:
    def __init__(self, master, player_index, initial_balance=1000, default_bet=10):
        self.player_index = player_index
        self.hand = []
        self.hand_value = 0
        self.is_busted = False
        self.status = "active" # active, stand, bust, blackjack
        self.balance = initial_balance
        self.bet = default_bet
        self.has_blackjack = False

        # GUI elements for this player
        self.frame = tk.LabelFrame(master, text=f"Player {player_index + 1}", padx=5, pady=5)
        self.frame.grid(row=0, column=player_index, padx=5, pady=5, sticky="nsew")

        # Bet display
        self.bet_label = tk.Label(self.frame, text=f"Bet: ${self.bet}", font=("Arial", 9))
        self.bet_label.pack(anchor="w")

        # Balance display
        self.balance_label = tk.Label(self.frame, text=f"Balance: ${self.balance}", font=("Arial", 9))
        self.balance_label.pack(anchor="w")

        self.hand_label = tk.Label(self.frame, text="Hand: [ ] = 0", font=("Arial", 10))
        self.hand_label.pack()

        self.status_label = tk.Label(self.frame, text="Status: Active", fg="black")
        self.status_label.pack()

        self.recommendation_label = tk.Label(self.frame, text="Rec: -", fg="purple")
        self.recommendation_label.pack()

        self.result_label = tk.Label(self.frame, text="", font=("Arial", 10, "bold"))
        self.result_label.pack()

    def add_card(self, card):
        self.hand.append(card)
        self._calculate_hand_value()

    def _calculate_hand_value(self):
        total = 0
        aces = 0
        for val, _ in self.hand:
            if val == 1: # Ace
                aces += 1
            else:
                total += val

        # Add aces, treating them as 11 if possible without busting
        for _ in range(aces):
            if total + 11 <= 21:
                total += 11
            else:
                total += 1 # Treat as 1

        self.hand_value = total
        self.is_busted = self.hand_value > 21
        self.has_blackjack = (len(self.hand) == 2 and self.hand_value == 21)

    def get_hand_value(self):
        return self.hand_value

    def get_hand(self):
        return self.hand

    def reset(self):
        self.hand = []
        self.hand_value = 0
        self.is_busted = False
        self.status = "active"
        self.has_blackjack = False
        self.bet = 0 # Bet is placed at the start of the round
        self.update_gui() # Clear GUI elements

    def place_bet(self, amount):
        if self.balance >= amount:
            self.bet = amount
            self.balance -= amount
            self.update_gui()
            return True
        else:
            self.bet = 0
            return False # Not enough balance

    def win_bet(self, payout_multiplier=1):
        winnings = self.bet * payout_multiplier
        self.balance += winnings + self.bet # Return original bet + winnings
        self.bet = 0
        self.update_gui()
        return winnings

    def lose_bet(self):
        self.bet = 0 # Bet is lost
        self.update_gui()

    def push_bet(self):
        self.balance += self.bet # Return original bet
        self.bet = 0
        self.update_gui()

    def update_gui(self):
        # Update hand display
        hand_str = ", ".join([card_repr for val, card_repr in self.hand])
        self.hand_label.config(text=f"Hand: [{hand_str}] = {self.hand_value}")

        # Update status
        self.status_label.config(text=f"Status: {self.status.capitalize()}",
                                 fg="red" if self.is_busted else "blue" if self.status == "stand" else "black")

        # Update balance and bet
        self.balance_label.config(text=f"Balance: ${self.balance}")
        self.bet_label.config(text=f"Bet: ${self.bet}")

        # Clear recommendation and result for new round
        if self.status == "active":
            self.recommendation_label.config(text="Rec: -")
            self.result_label.config(text="")