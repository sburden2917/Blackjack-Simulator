import tkinter as tk
from blackjack_strategy import PLAYING_STRATEGIES, BETTING_STRATEGIES
from hand_utils import calculate_hand_value
from statistics import PlayerStatistics
from strategy_explanation import get_strategy_explanation, get_hand_type_description
from constants import (
    BG_COLOR, WHITE, RED_SUIT_COLOR, BLACK_SUIT_COLOR, YELLOW, DARK_GREEN,
    STATUS_ACTIVE, STATUS_STAND, STATUS_BUST, STATUS_BLACKJACK, GREEN, RED
)


class Hand:
    def __init__(self, bet_amount):
        self.cards = []
        self.hand_value = 0
        self.is_busted = False
        self.status = STATUS_ACTIVE
        self.bet = bet_amount
        self.has_blackjack = False
        self.result_text = ""
        self.result_color = "black"
        self.is_surrendered = False
        self.insurance_bet = 0

    def add_card(self, card):
        self.cards.append(card)
        self._calculate_hand_value()

    def _calculate_hand_value(self):
        self.hand_value, self.is_busted, self.has_blackjack = calculate_hand_value(self.cards)


class Player:
    def __init__(self, master, player_index, initial_balance=1000, default_bet=10):
        self.player_index = player_index
        self.hands = []
        self.balance = initial_balance
        self.starting_balance = initial_balance  # Track starting balance for P/L calculation
        self.default_bet = default_bet

        # Strategy and skill attributes
        self.skill_level = tk.DoubleVar(value=1.0)
        self.playing_strategy = tk.StringVar(value=list(PLAYING_STRATEGIES.keys())[0])
        self.betting_strategy = tk.StringVar(value=list(BETTING_STRATEGIES.keys())[0])
        self.previous_bet_won = None
        self.last_bet_amount = default_bet
        self.win_streak = 0
        
        # Statistics tracking
        self.stats = PlayerStatistics()
        self.last_recommendation = None
        self.last_action_taken = None
        self.last_hand_type = None

        # GUI elements
        self.frame = tk.LabelFrame(master, text=f"Player {player_index + 1}", padx=5, pady=5, bg=BG_COLOR, fg=WHITE,
                                   font=("Arial", 10, "bold"))
        self.frame.grid(row=0, column=player_index, padx=5, pady=5, sticky="nsew")

        # --- Settings inside the player frame ---
        settings_frame = tk.Frame(self.frame, bg=BG_COLOR)
        settings_frame.pack(pady=5, fill="x")

        tk.Label(settings_frame, text="Skill:", font=("Arial", 8), bg=BG_COLOR, fg=WHITE).grid(row=0, column=0,
                                                                                                  sticky="w")
        skill_scale = tk.Scale(settings_frame, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL,
                               variable=self.skill_level, bg=BG_COLOR, fg=WHITE, troughcolor=DARK_GREEN,
                               highlightthickness=0)
        skill_scale.grid(row=0, column=1, sticky="ew")

        tk.Label(settings_frame, text="Play:", font=("Arial", 8), bg=BG_COLOR, fg=WHITE).grid(row=1, column=0,
                                                                                                 sticky="w")
        play_menu = tk.OptionMenu(settings_frame, self.playing_strategy, *PLAYING_STRATEGIES.keys())
        play_menu.config(font=("Arial", 8), width=8)
        play_menu.grid(row=1, column=1, sticky="ew", pady=1)

        tk.Label(settings_frame, text="Bet:", font=("Arial", 8), bg=BG_COLOR, fg=WHITE).grid(row=2, column=0,
                                                                                                sticky="w")
        bet_menu = tk.OptionMenu(settings_frame, self.betting_strategy, *BETTING_STRATEGIES.keys())
        bet_menu.config(font=("Arial", 8), width=8)
        bet_menu.grid(row=2, column=1, sticky="ew", pady=1)

        settings_frame.grid_columnconfigure(1, weight=1)

        self.hand_container = tk.Frame(self.frame, bg=BG_COLOR)
        self.hand_container.pack(pady=5)

        self.balance_label = tk.Label(self.frame, text=f"Balance: ${self.balance:.2f}", font=("Arial", 9), bg=BG_COLOR,
                                      fg=WHITE)
        self.balance_label.pack(anchor="w")

        self.profit_loss_label = tk.Label(self.frame, text="P/L: $0.00", font=("Arial", 9, "bold"), bg=BG_COLOR,
                                          fg=WHITE)
        self.profit_loss_label.pack(anchor="w")
        
        # Statistics display
        stats_frame = tk.Frame(self.frame, bg=BG_COLOR)
        stats_frame.pack(anchor="w", pady=2)
        
        from help_text import WIN_RATE_EXPLANATION, RTP_EXPLANATION, STRATEGY_ADHERENCE_EXPLANATION
        
        # Win Rate with tooltip
        win_rate_container = tk.Frame(stats_frame, bg=BG_COLOR)
        win_rate_container.pack(side="left", padx=5)
        self.win_rate_label = tk.Label(win_rate_container, text="Win Rate: -", font=("Arial", 8), bg=BG_COLOR, fg=WHITE,
                                       cursor="hand2")
        self.win_rate_label.pack()
        self.win_rate_label.bind("<Button-1>", lambda e: self._show_help("Win Rate", WIN_RATE_EXPLANATION))
        
        # RTP with tooltip
        rtp_container = tk.Frame(stats_frame, bg=BG_COLOR)
        rtp_container.pack(side="left", padx=5)
        self.rtp_label = tk.Label(rtp_container, text="RTP: -", font=("Arial", 8), bg=BG_COLOR, fg=WHITE,
                                 cursor="hand2")
        self.rtp_label.pack()
        self.rtp_label.bind("<Button-1>", lambda e: self._show_help("Return to Player (RTP)", RTP_EXPLANATION))
        
        # Strategy Adherence with tooltip
        adherence_container = tk.Frame(stats_frame, bg=BG_COLOR)
        adherence_container.pack(side="left", padx=5)
        self.adherence_label = tk.Label(adherence_container, text="Strategy: -", font=("Arial", 8), bg=BG_COLOR, fg=WHITE,
                                        cursor="hand2")
        self.adherence_label.pack()
        self.adherence_label.bind("<Button-1>", lambda e: self._show_help("Strategy Adherence", STRATEGY_ADHERENCE_EXPLANATION))

        self.recommendation_label = tk.Label(self.frame, text="Rec: -", fg=YELLOW, font=("Arial", 10, "italic"),
                                             bg=BG_COLOR)
        self.recommendation_label.pack()
        
        # Strategy explanation label
        self.explanation_label = tk.Label(self.frame, text="", fg=WHITE, font=("Arial", 8), bg=BG_COLOR, wraplength=200,
                                          justify="left")
        self.explanation_label.pack(anchor="w", padx=5, pady=2)
        
        # Hand type indicator
        self.hand_type_label = tk.Label(self.frame, text="", font=("Arial", 9, "bold"), bg=BG_COLOR, fg=YELLOW)
        self.hand_type_label.pack(anchor="w", padx=5)
        
        # Probability display
        self.probability_label = tk.Label(self.frame, text="", font=("Arial", 7), bg=BG_COLOR, fg=WHITE,
                                         wraplength=200, justify="left")
        self.probability_label.pack(anchor="w", padx=5, pady=2)

    def place_bet(self, get_bet_amount_func):
        amount = get_bet_amount_func(self, self.default_bet, self.betting_strategy.get())
        if self.balance >= amount:
            self.balance -= amount
            self.last_bet_amount = amount
            new_hand = Hand(amount)
            self.hands.append(new_hand)
            self._update_profit_loss()  # Update P/L immediately after bet
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
        self._update_profit_loss()
        self._update_statistics_display()

        if not self.hands:
            placeholder = tk.Frame(self.hand_container, height=100, bg=BG_COLOR)
            placeholder.pack()
            self.recommendation_label.config(text="Rec: -")
            self.explanation_label.config(text="")
            self.hand_type_label.config(text="")
            return

        for i, hand in enumerate(self.hands):
            hand_frame = tk.Frame(self.hand_container, bg=BG_COLOR)
            hand_frame.pack(pady=5)

            title_text = f"Hand {i + 1} ({hand.hand_value}) - Bet: ${hand.bet}"
            title_label = tk.Label(hand_frame, text=title_text, font=("Arial", 10, "bold"), fg=WHITE, bg=BG_COLOR)
            title_label.pack()

            cards_frame = tk.Frame(hand_frame, bg=BG_COLOR)
            cards_frame.pack()

            for _, card_repr in hand.cards:
                suit = card_repr[-1]
                color = RED_SUIT_COLOR if suit in ['♥', '♦'] else BLACK_SUIT_COLOR
                card_label = tk.Label(cards_frame, text=card_repr, font=("Arial", 24, "bold"), fg=color, bg="white",
                                      padx=5, pady=5, relief="raised", borderwidth=2)
                card_label.pack(side="left", padx=2, pady=2)

            if hand.result_text:
                result_label = tk.Label(hand_frame, text=hand.result_text, font=("Arial", 10, "bold"),
                                        fg=hand.result_color, bg=BG_COLOR)
                result_label.pack()

    def record_win(self, hand, payout_multiplier=1):
        winnings = hand.bet * payout_multiplier
        net_winnings = winnings  # Net profit from this hand
        self.balance += winnings + hand.bet
        self.previous_bet_won = True
        self.win_streak += 1
        
        # Track statistics
        was_mistake = self._was_strategy_mistake(hand)
        result = "blackjack" if hand.has_blackjack else "win"
        self.stats.record_hand(result, hand.bet, net_winnings, was_mistake)

    def record_loss(self, hand):
        self.previous_bet_won = False
        self.win_streak = 0
        
        # Track statistics
        was_mistake = self._was_strategy_mistake(hand)
        result = "bust" if hand.is_busted else "loss"
        self.stats.record_hand(result, hand.bet, -hand.bet, was_mistake)

    def record_push(self, hand):
        self.balance += hand.bet
        self.previous_bet_won = None
        
        # Track statistics
        was_mistake = self._was_strategy_mistake(hand)
        self.stats.record_hand("push", hand.bet, 0, was_mistake)
    
    def record_action(self, action: str):
        """Record a player action for statistics."""
        self.stats.record_action(action)
        self.last_action_taken = action
    
    def _was_strategy_mistake(self, hand) -> bool:
        """Check if the last action was a strategy mistake."""
        if self.last_recommendation is None or self.last_action_taken is None:
            return False
        
        # Map actions to recommendations
        action_map = {
            "hit": "Hit",
            "stand": "Stand",
            "double": "Double Down",
            "split": "Split"
        }
        
        expected_action = action_map.get(self.last_action_taken.lower(), "")
        return expected_action != self.last_recommendation
    
    def set_recommendation(self, recommendation: str, explanation: str, hand_type: str, hand_type_desc: str):
        """Set the current recommendation and explanation."""
        self.last_recommendation = recommendation
        self.last_hand_type = hand_type
        self.recommendation_label.config(text=f"Rec: {recommendation}", fg=YELLOW)
        self.explanation_label.config(text=explanation)
        self.hand_type_label.config(text=hand_type_desc)

    def _update_profit_loss(self):
        """Update the profit/loss label for this player."""
        profit_loss = self.balance - self.starting_balance
        color = GREEN if profit_loss > 0 else RED if profit_loss < 0 else WHITE
        self.profit_loss_label.config(text=f"P/L: ${profit_loss:+.2f}", fg=color)
    
    def _update_statistics_display(self):
        """Update the statistics display labels."""
        win_rate = self.stats.get_win_rate()
        rtp = self.stats.get_rtp()
        adherence = self.stats.get_strategy_adherence()
        
        self.win_rate_label.config(text=f"Win: {win_rate:.1f}%")
        
        # Color code RTP
        if rtp >= 100:
            rtp_color = GREEN
        elif rtp >= 95:
            rtp_color = YELLOW
        else:
            rtp_color = RED
        self.rtp_label.config(text=f"RTP: {rtp:.1f}%", fg=rtp_color)
        
        # Color code adherence
        if adherence >= 95:
            adherence_color = GREEN
        elif adherence >= 80:
            adherence_color = YELLOW
        else:
            adherence_color = RED
        
        self.adherence_label.config(
            text=f"Strategy: {adherence:.1f}%",
            fg=adherence_color
        )
    
    def _show_help(self, title, text):
        """Show help window with explanation."""
        help_window = tk.Toplevel(self.frame.winfo_toplevel())
        help_window.title(f"Help: {title}")
        help_window.configure(bg=BG_COLOR)
        help_window.geometry("500x400")
        
        # Title
        title_label = tk.Label(help_window, text=title, font=("Arial", 14, "bold"),
                              bg=BG_COLOR, fg=WHITE)
        title_label.pack(pady=10)
        
        # Text with scrolling
        text_frame = tk.Frame(help_window, bg=BG_COLOR)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        text_widget = tk.Text(text_frame, wrap="word", font=("Arial", 10),
                             bg=BG_COLOR, fg=WHITE, yscrollcommand=scrollbar.set,
                             padx=10, pady=10, relief="flat")
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")
        
        # Close button
        close_button = tk.Button(help_window, text="Close", command=help_window.destroy,
                                 font=("Arial", 10))
        close_button.pack(pady=10)