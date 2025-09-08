import tkinter as tk
from blackjack_strategy import PLAYING_STRATEGIES, BETTING_STRATEGIES


class Hand:
    def __init__(self, bet_amount):
        self.cards = []
        self.hand_value = 0
        self.is_busted = False
        self.status = "active"  # active, stand, bust, blackjack
        self.bet = bet_amount
        self.has_blackjack = False
        self.result_text = ""
        self.result_color = "black"

    def add_card(self, card):
        self.cards.append(card)
        self._calculate_hand_value()

    def _calculate_hand_value(self):
        total = 0
        aces = sum(1 for val, _ in self.cards if val == 1)
        non_ace_total = sum(val for val, _ in self.cards if val != 1)
        total = non_ace_total
        for _ in range(aces):
            if total + 11 <= 21:
                total += 11
            else:
                total += 1
        self.hand_value = total
        self.is_busted = self.hand_value > 21
        if len(self.cards) == 2 and self.hand_value == 21:
            self.has_blackjack = True


class Player:
    def __init__(self, master, player_index, initial_balance=1000, default_bet=10):
        self.player_index = player_index
        self.hands = []
        self.balance = initial_balance
        self.default_bet = default_bet

        # Strategy and skill attributes
        self.skill_level = tk.DoubleVar(value=1.0)
        self.playing_strategy = tk.StringVar(value=list(PLAYING_STRATEGIES.keys())[0])
        self.betting_strategy = tk.StringVar(value=list(BETTING_STRATEGIES.keys())[0])
        self.previous_bet_won = None
        self.last_bet_amount = default_bet
        self.win_streak = 0

        # GUI elements
        self.frame = tk.LabelFrame(master, text=f"Player {player_index + 1}", padx=5, pady=5, bg="#087830", fg="white",
                                   font=("Arial", 10, "bold"))
        self.frame.grid(row=0, column=player_index, padx=5, pady=5, sticky="nsew")

        # --- Settings inside the player frame ---
        settings_frame = tk.Frame(self.frame, bg="#087830")
        settings_frame.pack(pady=5, fill="x")

        tk.Label(settings_frame, text="Skill:", font=("Arial", 8), bg="#087830", fg="white").grid(row=0, column=0,
                                                                                                  sticky="w")
        skill_scale = tk.Scale(settings_frame, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL,
                               variable=self.skill_level, bg="#087830", fg="white", troughcolor="#065c25",
                               highlightthickness=0)
        skill_scale.grid(row=0, column=1, sticky="ew")

        tk.Label(settings_frame, text="Play:", font=("Arial", 8), bg="#087830", fg="white").grid(row=1, column=0,
                                                                                                 sticky="w")
        play_menu = tk.OptionMenu(settings_frame, self.playing_strategy, *PLAYING_STRATEGIES.keys())
        play_menu.config(font=("Arial", 8), width=8)
        play_menu.grid(row=1, column=1, sticky="ew", pady=1)

        tk.Label(settings_frame, text="Bet:", font=("Arial", 8), bg="#087830", fg="white").grid(row=2, column=0,
                                                                                                sticky="w")
        bet_menu = tk.OptionMenu(settings_frame, self.betting_strategy, *BETTING_STRATEGIES.keys())
        bet_menu.config(font=("Arial", 8), width=8)
        bet_menu.grid(row=2, column=1, sticky="ew", pady=1)

        settings_frame.grid_columnconfigure(1, weight=1)

        self.hand_container = tk.Frame(self.frame, bg="#087830")
        self.hand_container.pack(pady=5)

        self.balance_label = tk.Label(self.frame, text=f"Balance: ${self.balance}", font=("Arial", 9), bg="#087830",
                                      fg="white")
        self.balance_label.pack(anchor="w")

        self.recommendation_label = tk.Label(self.frame, text="Rec: -", fg="#ffc107", font=("Arial", 10, "italic"),
                                             bg="#087830")
        self.recommendation_label.pack()

    def place_bet(self, get_bet_amount_func):
        amount = get_bet_amount_func(self, self.default_bet, self.betting_strategy.get())
        if self.balance >= amount:
            self.balance -= amount
            self.last_bet_amount = amount
            new_hand = Hand(amount)
            self.hands.append(new_hand)
            return True
        return False

    def reset(self):
        self.hands.clear()
        self.update_gui()

    def can_split(self, hand):
        return len(hand.cards) == 2 and hand.cards[0][0] == hand.cards[1][0]

    def update_gui(self):
        for widget in self.hand_container.winfo_children():
            widget.destroy()

        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

        if not self.hands:
            placeholder = tk.Frame(self.hand_container, height=100, bg="#087830")
            placeholder.pack()
            self.recommendation_label.config(text="Rec: -")
            return

        for i, hand in enumerate(self.hands):
            hand_frame = tk.Frame(self.hand_container, bg="#087830")
            hand_frame.pack(pady=5)

            title_text = f"Hand {i + 1} ({hand.hand_value}) - Bet: ${hand.bet}"
            title_label = tk.Label(hand_frame, text=title_text, font=("Arial", 10, "bold"), fg="white", bg="#087830")
            title_label.pack()

            cards_frame = tk.Frame(hand_frame, bg="#087830")
            cards_frame.pack()

            for _, card_repr in hand.cards:
                suit = card_repr[-1]
                color = "red" if suit in ['♥', '♦'] else "black"
                card_label = tk.Label(cards_frame, text=card_repr, font=("Arial", 24, "bold"), fg=color, bg="white",
                                      padx=5, pady=5, relief="raised", borderwidth=2)
                card_label.pack(side="left", padx=2, pady=2)

            if hand.result_text:
                result_label = tk.Label(hand_frame, text=hand.result_text, font=("Arial", 10, "bold"),
                                        fg=hand.result_color, bg="#087830")
                result_label.pack()

    def record_win(self, hand, payout_multiplier=1):
        winnings = hand.bet * payout_multiplier
        self.balance += winnings + hand.bet
        self.previous_bet_won = True

    def record_loss(self, hand):
        self.previous_bet_won = False
        self.win_streak = 0

    def record_push(self, hand):
        self.balance += hand.bet
        self.previous_bet_won = None