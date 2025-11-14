import tkinter as tk
import random
from deck import Deck
from player import Player, Hand
from dealer import Dealer
from blackjack_strategy import get_recommendation, get_bet_amount
from statistics import CardCounting
from strategy_explanation import get_strategy_explanation, get_hand_type_description
from probability_calculator import get_action_probabilities, calculate_bust_probability
from casino_rules import CasinoRules
from bankroll_manager import BankrollManager
from session_stats import SessionStatistics
from constants import (
    BG_COLOR, WHITE, GREEN, RED, BLUE, YELLOW, DEFAULT_NUM_DECKS,
    BLACKJACK_PAYOUT_MULTIPLIER, DEFAULT_AUTOPLAY_SPEED, AUTOPLAY_RESULTS_DELAY,
    STATUS_ACTIVE, STATUS_STAND, STATUS_BUST, STATUS_BLACKJACK, DEALER_STAND_VALUE
)


class BlackjackSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Simulator")
        self.root.configure(bg=BG_COLOR)

        self.deck = Deck(num_decks=DEFAULT_NUM_DECKS)
        self.deck.shuffle()  # Shuffle initial deck
        self.players = []
        self.dealer = Dealer(self.root)
        
        # Card counting - persists across rounds until deck reshuffles
        self.card_counter = CardCounting(num_decks=DEFAULT_NUM_DECKS)
        
        # Casino rules
        self.casino_rules = CasinoRules()

        self.current_player_index = 0
        self.current_hand_index = 0
        self.autoplay = False
        self.autoplay_speed = DEFAULT_AUTOPLAY_SPEED
        self.total_starting_balance = 0
        self.round_number = 0
        self.insurance_offered = False
        self.tutorial_mode = False
        
        # Session statistics
        self.session_stats = SessionStatistics()

        self.create_widgets()
        self.setup_game_settings()

    def create_widgets(self):
        # Settings Frame
        self.settings_frame = tk.LabelFrame(self.root, text="Game Settings", padx=10, pady=10, bg=BG_COLOR, fg=WHITE,
                                            font=("Arial", 10, "bold"))
        self.settings_frame.pack(pady=10, padx=10)

        tk.Label(self.settings_frame, text="Number of Players (1-7):", bg=BG_COLOR, fg=WHITE).grid(row=0, column=0,
                                                                                                      sticky="w",
                                                                                                      pady=2)
        self.num_players_entry = tk.Entry(self.settings_frame, width=5)
        self.num_players_entry.insert(0, "1")
        self.num_players_entry.grid(row=0, column=1, sticky="w")

        tk.Label(self.settings_frame, text="Starting Balance per Player:", bg=BG_COLOR, fg=WHITE).grid(row=1,
                                                                                                          column=0,
                                                                                                          sticky="w",
                                                                                                          pady=2)
        self.starting_balance_entry = tk.Entry(self.settings_frame, width=10)
        self.starting_balance_entry.insert(0, "1000")
        self.starting_balance_entry.grid(row=1, column=1, sticky="w")

        tk.Label(self.settings_frame, text="Default Bet per Player:", bg=BG_COLOR, fg=WHITE).grid(row=2, column=0,
                                                                                                     sticky="w", pady=2)
        self.default_bet_entry = tk.Entry(self.settings_frame, width=10)
        self.default_bet_entry.insert(0, "10")
        self.default_bet_entry.grid(row=2, column=1, sticky="w")
        
        # Casino rules
        rules_frame = tk.LabelFrame(self.settings_frame, text="Casino Rules", bg=BG_COLOR, fg=WHITE, padx=5, pady=5)
        rules_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.soft_17_var = tk.BooleanVar(value=False)
        tk.Checkbutton(rules_frame, text="Dealer Hits Soft 17", variable=self.soft_17_var,
                      bg=BG_COLOR, fg=WHITE, selectcolor=BG_COLOR).grid(row=0, column=0, sticky="w", padx=5)
        
        self.insurance_var = tk.BooleanVar(value=True)
        tk.Checkbutton(rules_frame, text="Insurance Available", variable=self.insurance_var,
                      bg=BG_COLOR, fg=WHITE, selectcolor=BG_COLOR).grid(row=0, column=1, sticky="w", padx=5)
        
        self.surrender_var = tk.BooleanVar(value=True)
        tk.Checkbutton(rules_frame, text="Surrender Available", variable=self.surrender_var,
                      bg=BG_COLOR, fg=WHITE, selectcolor=BG_COLOR).grid(row=1, column=0, sticky="w", padx=5)
        
        self.tutorial_var = tk.BooleanVar(value=False)
        tk.Checkbutton(rules_frame, text="Tutorial Mode", variable=self.tutorial_var,
                      bg=BG_COLOR, fg=WHITE, selectcolor=BG_COLOR).grid(row=1, column=1, sticky="w", padx=5)

        self.start_button = tk.Button(self.settings_frame, text="Start Game", command=self.setup_game)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Main Game Frame
        self.game_frame = tk.Frame(self.root, bg=BG_COLOR)

        self.dealer_frame = tk.LabelFrame(self.game_frame, text="Dealer", padx=10, pady=10, bg=BG_COLOR, fg=WHITE)
        self.dealer_frame.pack(fill="x", padx=10, pady=5)
        self.dealer.create_gui_elements(self.dealer_frame)

        self.player_container = tk.Frame(self.game_frame, bg=BG_COLOR)
        self.player_container.pack(pady=5)

        # Stats Frame
        stats_frame = tk.Frame(self.game_frame, bg=BG_COLOR)
        stats_frame.pack(pady=5)
        self.profit_loss_label = tk.Label(stats_frame, text="", font=("Arial", 12, "bold"), bg=BG_COLOR, fg=WHITE)
        self.profit_loss_label.pack(side="left", padx=20)
        self.round_label = tk.Label(stats_frame, text="", font=("Arial", 12, "bold"), bg=BG_COLOR, fg=WHITE)
        self.round_label.pack(side="left", padx=20)
        
        # Card counting display
        count_frame = tk.Frame(stats_frame, bg=BG_COLOR)
        count_frame.pack(side="left", padx=20)
        
        from help_text import CARD_COUNTING_EXPLANATION
        
        count_label = tk.Label(count_frame, text="Card Count:", font=("Arial", 10), bg=BG_COLOR, fg=WHITE,
                              cursor="hand2")
        count_label.pack(side="left", padx=5)
        count_label.bind("<Button-1>", lambda e: self._show_count_help())
        
        self.running_count_label = tk.Label(count_frame, text="RC: 0", font=("Arial", 10, "bold"), bg=BG_COLOR, fg=WHITE,
                                            cursor="hand2")
        self.running_count_label.pack(side="left", padx=5)
        self.running_count_label.bind("<Button-1>", lambda e: self._show_count_help())
        
        self.true_count_label = tk.Label(count_frame, text="TC: 0.0", font=("Arial", 10, "bold"), bg=BG_COLOR, fg=WHITE,
                                        cursor="hand2")
        self.true_count_label.pack(side="left", padx=5)
        self.true_count_label.bind("<Button-1>", lambda e: self._show_count_help())
        
        self.count_status_label = tk.Label(count_frame, text="", font=("Arial", 10), bg=BG_COLOR, fg=YELLOW,
                                           cursor="hand2")
        self.count_status_label.pack(side="left", padx=5)
        self.count_status_label.bind("<Button-1>", lambda e: self._show_count_help())
        
        # Cards remaining display
        self.cards_remaining_label = tk.Label(stats_frame, text="Cards: 416", font=("Arial", 10), bg=BG_COLOR, fg=WHITE)
        self.cards_remaining_label.pack(side="left", padx=20)
        
        # Strategy chart button
        self.strategy_chart_button = tk.Button(stats_frame, text="Strategy Chart", command=self.show_strategy_chart,
                                                font=("Arial", 9))
        self.strategy_chart_button.pack(side="left", padx=10)
        
        # Session stats and export buttons
        self.session_stats_button = tk.Button(stats_frame, text="Session Stats", command=self.show_session_stats,
                                              font=("Arial", 9))
        self.session_stats_button.pack(side="left", padx=5)
        
        self.export_button = tk.Button(stats_frame, text="Export Stats", command=self.export_statistics,
                                       font=("Arial", 9))
        self.export_button.pack(side="left", padx=5)

        self.control_frame = tk.Frame(self.game_frame, bg=BG_COLOR)
        self.control_frame.pack(pady=10)

        self.hit_button = tk.Button(self.control_frame, text="Hit", command=self.hit)
        self.hit_button.pack(side="left", padx=3)
        self.stand_button = tk.Button(self.control_frame, text="Stand", command=self.stand)
        self.stand_button.pack(side="left", padx=3)
        self.double_down_button = tk.Button(self.control_frame, text="Double Down", command=self.double_down)
        self.double_down_button.pack(side="left", padx=3)
        self.split_button = tk.Button(self.control_frame, text="Split", command=self.split)
        self.split_button.pack(side="left", padx=3)
        self.surrender_button = tk.Button(self.control_frame, text="Surrender", command=self.surrender,
                                          state=tk.DISABLED)
        self.surrender_button.pack(side="left", padx=3)
        self.insurance_button = tk.Button(self.control_frame, text="Insurance", command=self.take_insurance,
                                         state=tk.DISABLED)
        self.insurance_button.pack(side="left", padx=3)
        self.decline_insurance_button = tk.Button(self.control_frame, text="No Insurance", command=self.decline_insurance,
                                                 state=tk.DISABLED)
        self.decline_insurance_button.pack(side="left", padx=3)
        self.deal_button = tk.Button(self.control_frame, text="Deal New Round", command=self.deal_initial_hands,
                                     state=tk.DISABLED)
        self.deal_button.pack(side="left", padx=3)
        self.autoplay_button = tk.Button(self.control_frame, text="Autoplay Off", command=self.toggle_autoplay,
                                         bg="#555", fg=WHITE)
        self.autoplay_button.pack(side="left", padx=10)
        self.main_menu_button = tk.Button(self.control_frame, text="Main Menu", command=self.go_to_main_menu)
        self.main_menu_button.pack(side="left", padx=10)

        self.status_bar = tk.Label(self.root, text="Game: Enter settings and click Start Game", bd=1, relief=tk.SUNKEN,
                                   anchor=tk.W, bg=BG_COLOR, fg=WHITE)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def go_to_main_menu(self):
        if self.autoplay:
            self.toggle_autoplay()
        self.setup_game_settings()

    def toggle_autoplay(self):
        self.autoplay = not self.autoplay
        state = "On" if self.autoplay else "Off"
        color = GREEN if self.autoplay else "#555"
        self.autoplay_button.config(text=f"Autoplay {state}", bg=color)

        if self.autoplay and self.deal_button.cget('state') == tk.DISABLED:
            self.check_current_player_status()
        elif self.autoplay and self.deal_button.cget('state') == tk.NORMAL:
            self.deal_initial_hands()

    def setup_game_settings(self):
        self.settings_frame.pack()
        self.game_frame.pack_forget()

    def setup_game(self):
        if self.autoplay:
            self.toggle_autoplay()

        try:
            num_players = int(self.num_players_entry.get())
            if not (1 <= num_players <= 7):
                raise ValueError("Number of players must be between 1 and 7.")
            starting_balance = int(self.starting_balance_entry.get())
            if starting_balance <= 0:
                raise ValueError("Starting balance must be positive.")
            default_bet = int(self.default_bet_entry.get())
            if default_bet <= 0:
                raise ValueError("Default bet must be positive.")
        except ValueError as e:
            self.status_bar.config(text=f"Error: {e}", fg=RED)
            return

        self.total_starting_balance = starting_balance * num_players
        self.round_number = 0
        self.profit_loss_label.config(text="Total P/L: $0.00", fg=WHITE)
        self.round_label.config(text="Round: 0")

        self.settings_frame.pack_forget()
        self.game_frame.pack()
        self.status_bar.config(text="Game: Settings applied. Click 'Deal New Round' to start.", fg=WHITE)
        self.deal_button.config(state=tk.NORMAL)

        for widget in self.player_container.winfo_children():
            widget.destroy()
        self.players.clear()

        for i in range(num_players):
            player = Player(self.player_container, i, starting_balance, default_bet)
            self.players.append(player)
            self.player_container.grid_columnconfigure(i, weight=1, uniform="player")
            # Initialize P/L display
            player._update_profit_loss()

        self.enable_player_controls(False)

    def deal_initial_hands(self):
        self.round_number += 1
        self.round_label.config(text=f"Round: {self.round_number}")
        
        # Only create new deck if current deck is empty or nearly empty
        if len(self.deck) < 52:  # Less than one deck remaining
            # Reshuffle - reset card counter
            self.deck = Deck(num_decks=DEFAULT_NUM_DECKS)
            self.deck.shuffle()
            self.card_counter.reset()
            self.status_bar.config(text="Game: Deck reshuffled. Card count reset.", fg=YELLOW)
        # Otherwise, continue using the same deck (card count persists)
        
        self.dealer.reset()

        all_players_can_bet = True
        for player in self.players:
            player.reset()
            if not player.place_bet(get_bet_amount):
                self.status_bar.config(
                    text=f"Player {player.player_index + 1} has insufficient funds. Autoplay stopped.", fg=RED)
                if self.autoplay:
                    self.toggle_autoplay()
                all_players_can_bet = False
        if not all_players_can_bet: return

        for player in self.players:
            card1 = self.deck.deal_card()
            card2 = self.deck.deal_card()
            player.hands[0].add_card(card1)
            player.hands[0].add_card(card2)
            # Count the cards
            self.card_counter.count_card(card1[0])
            self.card_counter.count_card(card2[0])
            player.update_gui()

        dealer_card1 = self.deck.deal_card()
        dealer_card2 = self.deck.deal_card()
        self.dealer.add_card(dealer_card1)
        self.dealer.add_card(dealer_card2)
        # Count dealer's up card (only the visible one initially)
        self.card_counter.count_card(dealer_card1[0])
        self.dealer.update_gui()
        self._update_count_display()
        
        # Check for insurance opportunity
        self.insurance_offered = self.casino_rules.should_offer_insurance(dealer_card1[0])
        if self.insurance_offered:
            self._offer_insurance()

        self.current_player_index = 0
        self.current_hand_index = 0
        self.status_bar.config(text="Game: Dealing cards...", fg=WHITE)

        self.deal_button.config(state=tk.DISABLED)

        self.check_current_player_status()

    def check_current_player_status(self):
        if self.current_player_index >= len(self.players):
            self.dealer_play()
            return

        current_player = self.players[self.current_player_index]

        if self.current_hand_index >= len(current_player.hands):
            self.next_turn_or_hand()
            return

        current_hand = current_player.hands[self.current_hand_index]
        if current_hand.status != STATUS_ACTIVE:
            self.next_turn_or_hand()
            return

        current_player.update_gui()

        dealer_upcard_value = self.dealer.get_up_card()[0]
        recommendation = get_recommendation(current_hand, dealer_upcard_value, current_player.playing_strategy.get())
        
        # Get hand type and explanation
        hand_type, hand_type_desc = get_hand_type_description(current_hand, dealer_upcard_value)
        pair_value = None
        if hand_type == "pair":
            pair_value = current_hand.cards[0][0] if current_hand.cards[0][0] <= 10 else 10
        
        explanation = get_strategy_explanation(
            current_hand.hand_value,
            dealer_upcard_value,
            hand_type,
            recommendation,
            is_pair=(hand_type == "pair"),
            pair_value=pair_value
        )
        
        # Set recommendation with explanation
        current_player.set_recommendation(recommendation, explanation, hand_type, hand_type_desc)
        
        # Calculate and display probabilities
        is_soft = (hand_type == "soft")
        can_double = self.is_action_possible('double')
        can_split = self.is_action_possible('split')
        
        try:
            probabilities = get_action_probabilities(
                current_hand.hand_value,
                dealer_upcard_value,
                is_soft,
                can_double,
                can_split
            )
            
            # Update probability display in player panel
            prob_text = " | ".join([f"{action}: {prob*100:.1f}%" for action, (prob, _) in probabilities.items()])
            if hasattr(current_player, 'probability_label'):
                current_player.probability_label.config(text=prob_text[:100])  # Limit length
        except:
            pass  # Skip if probability calculation fails
        
        # Visual mistake highlighting in tutorial mode
        if self.tutorial_mode and current_player.last_action_taken:
            self._highlight_mistakes(current_player, recommendation)

        player_id_str = f"Player {self.current_player_index + 1}"
        hand_id_str = f", Hand {self.current_hand_index + 1}" if len(current_player.hands) > 1 else ""
        self.status_bar.config(text=f"Game: {player_id_str}{hand_id_str}'s turn.", fg=WHITE)

        if current_hand.has_blackjack:
            current_hand.status = STATUS_BLACKJACK
            self.root.after(self.autoplay_speed, self.next_turn_or_hand)
            return
        elif current_hand.hand_value == 21:
            current_hand.status = STATUS_STAND
            self.root.after(self.autoplay_speed, self.next_turn_or_hand)
            return

        # Handle insurance offer (only for first player, first hand)
        if self.insurance_offered and self.current_player_index == 0 and self.current_hand_index == 0:
            # Insurance decision needed
            if self.autoplay:
                # Autoplay: automatically decline insurance (basic strategy recommends declining)
                self.root.after(self.autoplay_speed, self.decline_insurance)
            else:
                # Manual play: show insurance buttons
                self.enable_player_controls(False)
                self.insurance_button.config(state=tk.NORMAL)
                self.decline_insurance_button.config(state=tk.NORMAL)
        else:
            # Normal play - enable standard controls
            if self.autoplay:
                self.perform_autoplay_action(recommendation)
            else:
                self.enable_player_controls(True)

    def perform_autoplay_action(self, recommendation):
        self.enable_player_controls(False)
        player, hand = self.get_current_hand()

        action_map = {
            "Hit": self.hit,
            "Stand": self.stand,
            "Double Down": self.double_down,
            "Split": self.split
        }

        final_recommendation = recommendation
        if random.random() > player.skill_level.get():
            if recommendation == "Hit":
                final_recommendation = "Stand"
            elif recommendation == "Stand":
                final_recommendation = "Hit"
            else:
                final_recommendation = "Hit"
            player.recommendation_label.config(text=f"Rec: {recommendation} (Mistake: {final_recommendation})")

        action_func = action_map.get(final_recommendation)

        if final_recommendation == "Double Down" and not self.is_action_possible('double'):
            action_func = self.hit
        elif final_recommendation == "Split" and not self.is_action_possible('split'):
            new_rec = get_recommendation(hand, self.dealer.get_up_card()[0], player.playing_strategy.get(),
                                         ignore_pairs=True)
            action_func = action_map.get(new_rec, self.hit)

        if action_func:
            self.root.after(self.autoplay_speed, action_func)

    def next_turn_or_hand(self):
        # Disable insurance after first player (insurance only offered once per round)
        if self.current_player_index == 0:
            self.insurance_offered = False
            self.insurance_button.config(state=tk.DISABLED)
            self.decline_insurance_button.config(state=tk.DISABLED)
        
        self.current_hand_index += 1
        if self.current_player_index < len(self.players):
            current_player = self.players[self.current_player_index]
            if self.current_hand_index >= len(current_player.hands):
                self.current_player_index += 1
                self.current_hand_index = 0

        self.check_current_player_status()

    def get_current_hand(self):
        if self.current_player_index < len(self.players):
            player = self.players[self.current_player_index]
            if self.current_hand_index < len(player.hands):
                return player, player.hands[self.current_hand_index]
        return None, None

    def hit(self):
        player, hand = self.get_current_hand()
        if player and hand and hand.status == STATUS_ACTIVE:
            card = self.deck.deal_card()
            hand.add_card(card)
            # Count the card
            self.card_counter.count_card(card[0])
            self._update_count_display()
            player.record_action("hit")
            player.update_gui()

            if hand.is_busted:
                hand.status = STATUS_BUST
                player.update_gui()
                # Disable controls immediately when bust occurs
                self.enable_player_controls(False)
                # Proceed to next player/dealer
                self.root.after(self.autoplay_speed, self.next_turn_or_hand)
            else:
                self.check_current_player_status()

    def stand(self):
        player, hand = self.get_current_hand()
        if player and hand and hand.status == STATUS_ACTIVE:
            hand.status = STATUS_STAND
            player.record_action("stand")
            player.update_gui()
            self.root.after(self.autoplay_speed, self.next_turn_or_hand)

    def double_down(self):
        if not self.is_action_possible('double'):
            if self.autoplay: self.hit()
            return
        player, hand = self.get_current_hand()
        player.balance -= hand.bet
        hand.bet *= 2
        card = self.deck.deal_card()
        hand.add_card(card)
        # Count the card
        self.card_counter.count_card(card[0])
        self._update_count_display()
        hand.status = STATUS_STAND if not hand.is_busted else STATUS_BUST
        player.record_action("double")
        player.update_gui()
        self.root.after(self.autoplay_speed, self.next_turn_or_hand)

    def split(self):
        if not self.is_action_possible('split'):
            if self.autoplay: self.hit()
            return
        player, hand = self.get_current_hand()
        player.balance -= hand.bet
        new_hand = Hand(hand.bet)
        new_hand.add_card(hand.cards.pop(1))
        player.hands.insert(self.current_hand_index + 1, new_hand)
        card1 = self.deck.deal_card()
        card2 = self.deck.deal_card()
        hand.add_card(card1)
        new_hand.add_card(card2)
        # Count the cards
        self.card_counter.count_card(card1[0])
        self.card_counter.count_card(card2[0])
        self._update_count_display()
        player.record_action("split")
        player.update_gui()
        self.check_current_player_status()

    def is_action_possible(self, action):
        player, hand = self.get_current_hand()
        if not player or not hand or hand.status != STATUS_ACTIVE:
            return False
        if hand.is_surrendered:
            return False
        if action == 'double':
            return len(hand.cards) == 2 and player.balance >= hand.bet
        if action == 'split':
            return player.can_split(hand) and player.balance >= hand.bet
        if action == 'surrender':
            return (self.casino_rules.can_surrender(len(hand.cards), self.dealer.get_up_card()[0]) and
                   not self.insurance_offered)  # Can't surrender if insurance was offered
        return True

    def enable_player_controls(self, enable):
        if self.autoplay:
            enable = False

        state = tk.NORMAL if enable else tk.DISABLED
        self.hit_button.config(state=state)
        self.stand_button.config(state=state)
        self.double_down_button.config(state=tk.NORMAL if enable and self.is_action_possible('double') else tk.DISABLED)
        self.split_button.config(state=tk.NORMAL if enable and self.is_action_possible('split') else tk.DISABLED)
        self.surrender_button.config(state=tk.NORMAL if enable and self.is_action_possible('surrender') else tk.DISABLED)
        self.insurance_button.config(state=tk.NORMAL if self.insurance_offered and self.current_player_index == 0 else tk.DISABLED)
        self.decline_insurance_button.config(state=tk.NORMAL if self.insurance_offered and self.current_player_index == 0 else tk.DISABLED)

    def dealer_play(self):
        self.enable_player_controls(False)
        self.status_bar.config(text="Game: Dealer's turn...", fg=WHITE)
        self.dealer.reveal_hole_card()
        self.dealer.update_gui()

        all_busted = all(all(hand.is_busted for hand in p.hands) for p in self.players)
        if all_busted:
            self.root.after(self.autoplay_speed, self.show_results)
            return

        self.root.after(self.autoplay_speed, self._dealer_hit_loop)

    def _dealer_hit_loop(self):
        dealer_value = self.dealer.get_hand_value()
        # Check if dealer has soft hand
        has_ace = any(c[0] == 1 for c in self.dealer.hand)
        is_soft = has_ace and dealer_value > sum(c[0] for c in self.dealer.hand if c[0] != 1) + 1
        
        should_hit = not self.casino_rules.get_dealer_stand_value(dealer_value, is_soft)
        
        if should_hit:
            card = self.deck.deal_card()
            self.dealer.add_card(card)
            self.card_counter.count_card(card[0])
            self._update_count_display()
            self.dealer.update_gui()
            self.root.after(self.autoplay_speed, self._dealer_hit_loop)
        else:
            # Count dealer's hole card when revealed
            if len(self.dealer.hand) == 2 and not self.dealer.hole_card_hidden:
                self.card_counter.count_card(self.dealer.hand[1][0])
                self._update_count_display()
            self.root.after(self.autoplay_speed, self.show_results)

    def show_results(self):
        dealer_total = self.dealer.get_hand_value()
        dealer_busted = self.dealer.is_busted
        dealer_has_blackjack = self.dealer.has_blackjack

        for i, player in enumerate(self.players):
            for j, hand in enumerate(player.hands):
                if hand.is_surrendered:
                    # Surrendered hand - lose half bet
                    player.balance += hand.bet / 2
                    hand.result_text = "Surrendered (Lose 50%)"
                    hand.result_color = YELLOW
                    player.record_loss(hand)
                elif hand.is_busted:
                    player.record_loss(hand)
                    hand.result_text = "Bust! Lost"
                    hand.result_color = RED
                elif hand.has_blackjack:
                    if dealer_has_blackjack:
                        player.record_push(hand)
                        hand.result_text = "Push (Blackjack)"
                        hand.result_color = BLUE
                        # Insurance pays if taken
                        if hand.insurance_bet > 0:
                            player.balance += hand.insurance_bet * 3  # 2:1 payout
                            hand.result_text += " + Insurance Win"
                    else:
                        player.record_win(hand, payout_multiplier=BLACKJACK_PAYOUT_MULTIPLIER)
                        hand.result_text = "Blackjack! Win (3:2)"
                        hand.result_color = GREEN
                        # Insurance loses if taken
                        if hand.insurance_bet > 0:
                            hand.result_text += " (Insurance Lost)"
                elif dealer_has_blackjack:
                    # Dealer has blackjack, player doesn't - insurance pays
                    player.record_loss(hand)
                    hand.result_text = "Lost (Dealer Blackjack)"
                    hand.result_color = RED
                    if hand.insurance_bet > 0:
                        player.balance += hand.insurance_bet * 3  # 2:1 payout
                        hand.result_text += " + Insurance Win"
                elif dealer_busted:
                    player.record_win(hand)
                    hand.result_text = "Win (Dealer Busts)"
                    hand.result_color = GREEN
                elif hand.hand_value > dealer_total:
                    player.record_win(hand)
                    hand.result_text = "Win"
                    hand.result_color = GREEN
                elif hand.hand_value < dealer_total:
                    player.record_loss(hand)
                    hand.result_text = "Lost"
                    hand.result_color = RED
                else:  # Push
                    player.record_push(hand)
                    hand.result_text = "Push"
                    hand.result_color = BLUE
            player.update_gui()

        current_total_balance = sum(p.balance for p in self.players)
        profit_loss = current_total_balance - self.total_starting_balance

        color = GREEN if profit_loss > 0 else RED if profit_loss < 0 else WHITE
        self.profit_loss_label.config(text=f"Total P/L: ${profit_loss:+.2f}", fg=color)

        self.enable_player_controls(False)
        
        # Record round statistics
        players_data = []
        for player in self.players:
            players_data.append({
                'player_index': player.player_index,
                'balance': player.balance,
                'win_rate': player.stats.get_win_rate(),
                'rtp': player.stats.get_rtp(),
                'strategy_adherence': player.stats.get_strategy_adherence()
            })
        self.session_stats.record_round(self.round_number, players_data, profit_loss)
        if self.autoplay:
            self.root.after(AUTOPLAY_RESULTS_DELAY, self.deal_initial_hands)
        else:
            self.deal_button.config(state=tk.NORMAL)
    
    def _update_count_display(self):
        """Update the card counting display."""
        running_count = self.card_counter.running_count
        cards_remaining = len(self.deck)
        # Update total cards for accurate true count calculation
        self.card_counter.total_cards = cards_remaining + self.card_counter.cards_seen
        true_count = self.card_counter.get_true_count(cards_remaining)
        status = self.card_counter.get_count_status()
        decks_remaining = cards_remaining / 52.0
        
        # Color code running count
        if running_count >= 2:
            rc_color = GREEN
        elif running_count <= -2:
            rc_color = RED
        else:
            rc_color = WHITE
        
        # Color code true count
        if true_count >= 2:
            tc_color = GREEN
        elif true_count <= -2:
            tc_color = RED
        else:
            tc_color = WHITE
        
        self.running_count_label.config(text=f"RC: {running_count:+d}", fg=rc_color)
        self.true_count_label.config(text=f"TC: {true_count:+.1f}", fg=tc_color)
        self.count_status_label.config(text=status, fg=YELLOW if true_count >= 1 else WHITE)
        self.cards_remaining_label.config(text=f"Cards: {cards_remaining} ({decks_remaining:.1f} decks)")
        
        # Bet recommendation based on count
        if self.players and len(self.players) > 0:
            base_bet = self.players[0].default_bet
            recommended_bet = self.card_counter.get_betting_unit(base_bet)
            if recommended_bet != base_bet:
                # Show bet recommendation in status bar if count is favorable
                if true_count >= 2:
                    self.status_bar.config(
                        text=f"Count Favorable! Recommended bet: ${recommended_bet:.2f} (TC: {true_count:+.1f})",
                        fg=GREEN
                    )
    
    def show_strategy_chart(self):
        """Display basic strategy chart in a new window."""
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Basic Strategy Chart")
        chart_window.configure(bg=BG_COLOR)
        
        # Create a scrollable frame
        canvas = tk.Canvas(chart_window, bg=BG_COLOR)
        scrollbar = tk.Scrollbar(chart_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add strategy chart content
        from blackjack_strategy import BASIC_STRATEGY
        
        tk.Label(scrollable_frame, text="BASIC STRATEGY CHART", font=("Arial", 16, "bold"),
                bg=BG_COLOR, fg=WHITE).pack(pady=10)
        
        # Hard hands
        tk.Label(scrollable_frame, text="HARD HANDS", font=("Arial", 12, "bold"),
                bg=BG_COLOR, fg=YELLOW).pack(pady=5)
        self._create_strategy_table(scrollable_frame, BASIC_STRATEGY['hard'], "hard")
        
        # Soft hands
        tk.Label(scrollable_frame, text="SOFT HANDS", font=("Arial", 12, "bold"),
                bg=BG_COLOR, fg=YELLOW).pack(pady=5)
        self._create_strategy_table(scrollable_frame, BASIC_STRATEGY['soft'], "soft")
        
        # Pairs
        tk.Label(scrollable_frame, text="PAIRS", font=("Arial", 12, "bold"),
                bg=BG_COLOR, fg=YELLOW).pack(pady=5)
        self._create_strategy_table(scrollable_frame, BASIC_STRATEGY['pairs'], "pairs")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_strategy_table(self, parent, strategy_dict, hand_type):
        """Create a strategy table display."""
        dealer_cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 1]  # 1 = Ace
        dealer_labels = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"]
        
        # Create header
        header_frame = tk.Frame(parent, bg=BG_COLOR)
        header_frame.pack(pady=5)
        tk.Label(header_frame, text="Your Hand", font=("Arial", 9, "bold"), bg=BG_COLOR, fg=WHITE, width=12).grid(row=0, column=0, padx=2)
        for i, label in enumerate(dealer_labels):
            tk.Label(header_frame, text=label, font=("Arial", 9, "bold"), bg=BG_COLOR, fg=WHITE, width=4).grid(row=0, column=i+1, padx=1)
        
        # Create rows
        for hand_value in sorted(strategy_dict.keys(), reverse=True):
            row_frame = tk.Frame(parent, bg=BG_COLOR)
            row_frame.pack(pady=1)
            tk.Label(row_frame, text=str(hand_value), font=("Arial", 8), bg=BG_COLOR, fg=WHITE, width=12).grid(row=0, column=0, padx=2)
            for i, dealer_card in enumerate(dealer_cards):
                action = strategy_dict[hand_value].get(dealer_card, 'H')
                color_map = {'H': WHITE, 'S': GREEN, 'D': YELLOW, 'P': BLUE}
                action_map = {'H': 'H', 'S': 'S', 'D': 'D', 'P': 'P'}
                tk.Label(row_frame, text=action_map[action], font=("Arial", 8, "bold"),
                        bg=BG_COLOR, fg=color_map.get(action, WHITE), width=4).grid(row=0, column=i+1, padx=1)
        
        # Legend
        legend_frame = tk.Frame(parent, bg=BG_COLOR)
        legend_frame.pack(pady=5)
        tk.Label(legend_frame, text="Legend: ", font=("Arial", 8), bg=BG_COLOR, fg=WHITE).pack(side="left")
        tk.Label(legend_frame, text="H=Hit ", font=("Arial", 8), bg=BG_COLOR, fg=WHITE).pack(side="left")
        tk.Label(legend_frame, text="S=Stand ", font=("Arial", 8), bg=BG_COLOR, fg=GREEN).pack(side="left")
        tk.Label(legend_frame, text="D=Double ", font=("Arial", 8), bg=BG_COLOR, fg=YELLOW).pack(side="left")
        tk.Label(legend_frame, text="P=Split", font=("Arial", 8), bg=BG_COLOR, fg=BLUE).pack(side="left")
    
    def _show_count_help(self):
        """Show card counting help window."""
        from help_text import CARD_COUNTING_EXPLANATION
        help_window = tk.Toplevel(self.root)
        help_window.title("Help: Card Counting")
        help_window.configure(bg=BG_COLOR)
        help_window.geometry("550x450")
        
        # Title
        title_label = tk.Label(help_window, text="Card Counting (Hi-Lo System)", font=("Arial", 14, "bold"),
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
        
        text_widget.insert("1.0", CARD_COUNTING_EXPLANATION)
        text_widget.config(state="disabled")
        
        # Close button
        close_button = tk.Button(help_window, text="Close", command=help_window.destroy,
                                 font=("Arial", 10))
        close_button.pack(pady=10)
    
    def _offer_insurance(self):
        """Offer insurance to all players when dealer shows Ace."""
        self.status_bar.config(text="Game: Insurance available! Dealer shows Ace.", fg=YELLOW)
        # Insurance button will be enabled by enable_player_controls
    
    def take_insurance(self):
        """Player takes insurance bet."""
        player, hand = self.get_current_hand()
        if not player or not hand:
            return
        
        insurance_bet = hand.bet / 2
        if player.balance >= insurance_bet:
            player.balance -= insurance_bet
            hand.insurance_bet = insurance_bet
            self.status_bar.config(text=f"Game: Player {self.current_player_index + 1} took insurance.", fg=WHITE)
            player.update_gui()
        
        # After insurance decision, disable insurance buttons and enable normal controls
        self.insurance_offered = False
        self.insurance_button.config(state=tk.DISABLED)
        self.decline_insurance_button.config(state=tk.DISABLED)
        if not self.autoplay:
            self.enable_player_controls(True)
    
    def decline_insurance(self):
        """Player declines insurance - proceed with hand."""
        # Insurance decision made, disable insurance buttons and enable normal controls
        self.insurance_offered = False
        self.insurance_button.config(state=tk.DISABLED)
        self.decline_insurance_button.config(state=tk.DISABLED)
        
        # After declining insurance, proceed with normal play
        if self.autoplay:
            # In autoplay, continue with the current player's turn
            self.check_current_player_status()
        else:
            self.enable_player_controls(True)
    
    def surrender(self):
        """Player surrenders hand."""
        player, hand = self.get_current_hand()
        if not player or not hand or hand.status != STATUS_ACTIVE:
            return
        
        if not self.is_action_possible('surrender'):
            return
        
        hand.is_surrendered = True
        hand.status = STATUS_STAND
        player.update_gui()
        self.status_bar.config(text=f"Game: Player {self.current_player_index + 1} surrendered.", fg=YELLOW)
        self.root.after(self.autoplay_speed, self.next_turn_or_hand)
    
    def _highlight_mistakes(self, player, optimal_action):
        """Highlight when player makes a mistake."""
        if not player.last_action_taken:
            return
        
        action_map = {
            "hit": "Hit",
            "stand": "Stand",
            "double": "Double Down",
            "split": "Split"
        }
        
        player_action = action_map.get(player.last_action_taken.lower(), "")
        if player_action and player_action != optimal_action:
            # Mistake made - highlight in UI
            mistake_msg = f"⚠ Mistake: You chose {player_action}, but optimal is {optimal_action}"
            if hasattr(player, 'mistake_label'):
                player.mistake_label.config(text=mistake_msg, fg=RED)
            else:
                # Create mistake label if it doesn't exist
                mistake_label = tk.Label(player.frame, text=mistake_msg, font=("Arial", 8, "bold"),
                                        bg=BG_COLOR, fg=RED)
                mistake_label.pack(anchor="w", padx=5, pady=2)
                player.mistake_label = mistake_label
    
    def show_session_stats(self):
        """Display session statistics window."""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Session Statistics")
        stats_window.configure(bg=BG_COLOR)
        stats_window.geometry("600x500")
        
        summary = self.session_stats.get_session_summary()
        
        # Title
        tk.Label(stats_window, text="SESSION STATISTICS", font=("Arial", 16, "bold"),
                bg=BG_COLOR, fg=WHITE).pack(pady=10)
        
        # Summary frame
        summary_frame = tk.Frame(stats_window, bg=BG_COLOR)
        summary_frame.pack(pady=10, padx=20, fill="x")
        
        stats_text = f"""
Total Rounds: {summary.get('total_rounds', 0)}
Total P/L: ${summary.get('total_pl', 0):+.2f}
Average P/L per Round: ${summary.get('avg_pl_per_round', 0):+.2f}

Wins: {summary.get('wins', 0)}
Losses: {summary.get('losses', 0)}
Pushes: {summary.get('pushes', 0)}
Win Rate: {summary.get('win_rate', 0):.1f}%

Session Duration: {summary.get('session_duration', 'N/A')}
        """
        
        tk.Label(summary_frame, text=stats_text.strip(), font=("Arial", 11),
                bg=BG_COLOR, fg=WHITE, justify="left").pack(anchor="w")
        
        # Close button
        tk.Button(stats_window, text="Close", command=stats_window.destroy,
                 font=("Arial", 10)).pack(pady=10)
    
    def export_statistics(self):
        """Export session statistics to file."""
        try:
            import tkinter.filedialog as fd
            
            # Ask user for file location
            filename = fd.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                if filename.endswith('.csv'):
                    exported = self.session_stats.export_to_csv(filename)
                else:
                    exported = self.session_stats.export_to_json(filename)
                
                self.status_bar.config(text=f"Statistics exported to {exported}", fg=GREEN)
        except Exception as e:
            self.status_bar.config(text=f"Export failed: {str(e)}", fg=RED)
    
    def _show_tutorial_intro(self):
        """Show tutorial introduction when tutorial mode is enabled."""
        from tutorial_mode import TUTORIAL_LESSONS
        
        tutorial_window = tk.Toplevel(self.root)
        tutorial_window.title("Tutorial Mode")
        tutorial_window.configure(bg=BG_COLOR)
        tutorial_window.geometry("600x500")
        
        current_lesson = [0]  # Use list to allow modification in nested function
        
        def show_lesson(lesson_num):
            if lesson_num >= len(TUTORIAL_LESSONS):
                tutorial_window.destroy()
                return
            
            lesson = TUTORIAL_LESSONS[lesson_num]
            current_lesson[0] = lesson_num
            
            # Clear previous content
            for widget in content_frame.winfo_children():
                widget.destroy()
            
            # Title
            tk.Label(content_frame, text=lesson['title'], font=("Arial", 14, "bold"),
                    bg=BG_COLOR, fg=YELLOW).pack(pady=10)
            
            # Content
            text_widget = tk.Text(content_frame, wrap="word", font=("Arial", 10),
                                 bg=BG_COLOR, fg=WHITE, padx=20, pady=10, height=15)
            text_widget.pack(fill="both", expand=True, padx=20, pady=10)
            text_widget.insert("1.0", lesson['content'])
            text_widget.config(state="disabled")
            
            # Navigation buttons
            nav_frame = tk.Frame(content_frame, bg=BG_COLOR)
            nav_frame.pack(pady=10)
            
            if lesson_num > 0:
                tk.Button(nav_frame, text="Previous", command=lambda: show_lesson(lesson_num - 1),
                         font=("Arial", 10)).pack(side="left", padx=5)
            
            if lesson_num < len(TUTORIAL_LESSONS) - 1:
                tk.Button(nav_frame, text="Next", command=lambda: show_lesson(lesson_num + 1),
                         font=("Arial", 10)).pack(side="left", padx=5)
            else:
                tk.Button(nav_frame, text="Start Playing!", command=tutorial_window.destroy,
                         font=("Arial", 10), bg=GREEN).pack(side="left", padx=5)
        
        content_frame = tk.Frame(tutorial_window, bg=BG_COLOR)
        content_frame.pack(fill="both", expand=True)
        
        show_lesson(0)


if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackSimulator(root)
    root.mainloop()