import tkinter as tk
import random
from deck import Deck
from player import Player, Hand
from dealer import Dealer
from blackjack_strategy import get_recommendation, get_bet_amount

class BlackjackSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Simulator")
        self.root.configure(bg="#087830")

        self.deck = Deck()
        self.players = []
        self.dealer = Dealer(self.root)

        self.current_player_index = 0
        self.current_hand_index = 0
        self.autoplay = False
        self.autoplay_speed = 250
        self.total_starting_balance = 0
        self.round_number = 0

        self.create_widgets()
        self.setup_game_settings()

    def create_widgets(self):
        # Settings Frame
        self.settings_frame = tk.LabelFrame(self.root, text="Game Settings", padx=10, pady=10, bg="#087830", fg="white", font=("Arial", 10, "bold"))
        self.settings_frame.pack(pady=10, padx=10)

        tk.Label(self.settings_frame, text="Number of Players (1-7):", bg="#087830", fg="white").grid(row=0, column=0, sticky="w", pady=2)
        self.num_players_entry = tk.Entry(self.settings_frame, width=5)
        self.num_players_entry.insert(0, "1")
        self.num_players_entry.grid(row=0, column=1, sticky="w")

        tk.Label(self.settings_frame, text="Starting Balance per Player:", bg="#087830", fg="white").grid(row=1, column=0, sticky="w", pady=2)
        self.starting_balance_entry = tk.Entry(self.settings_frame, width=10)
        self.starting_balance_entry.insert(0, "1000")
        self.starting_balance_entry.grid(row=1, column=1, sticky="w")

        tk.Label(self.settings_frame, text="Default Bet per Player:", bg="#087830", fg="white").grid(row=2, column=0, sticky="w", pady=2)
        self.default_bet_entry = tk.Entry(self.settings_frame, width=10)
        self.default_bet_entry.insert(0, "10")
        self.default_bet_entry.grid(row=2, column=1, sticky="w")

        self.start_button = tk.Button(self.settings_frame, text="Start Game", command=self.setup_game)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Main Game Frame
        self.game_frame = tk.Frame(self.root, bg="#087830")

        self.dealer_frame = tk.LabelFrame(self.game_frame, text="Dealer", padx=10, pady=10, bg="#087830", fg="white")
        self.dealer_frame.pack(fill="x", padx=10, pady=5)
        self.dealer.create_gui_elements(self.dealer_frame)

        self.player_container = tk.Frame(self.game_frame, bg="#087830")
        self.player_container.pack(pady=5)

        # Stats Frame
        stats_frame = tk.Frame(self.game_frame, bg="#087830")
        stats_frame.pack(pady=5)
        self.profit_loss_label = tk.Label(stats_frame, text="", font=("Arial", 12, "bold"), bg="#087830", fg="white")
        self.profit_loss_label.pack(side="left", padx=20)
        self.round_label = tk.Label(stats_frame, text="", font=("Arial", 12, "bold"), bg="#087830", fg="white")
        self.round_label.pack(side="left", padx=20)

        self.control_frame = tk.Frame(self.game_frame, bg="#087830")
        self.control_frame.pack(pady=10)
        
        self.hit_button = tk.Button(self.control_frame, text="Hit", command=self.hit)
        self.hit_button.pack(side="left", padx=3)
        self.stand_button = tk.Button(self.control_frame, text="Stand", command=self.stand)
        self.stand_button.pack(side="left", padx=3)
        self.double_down_button = tk.Button(self.control_frame, text="Double Down", command=self.double_down)
        self.double_down_button.pack(side="left", padx=3)
        self.split_button = tk.Button(self.control_frame, text="Split", command=self.split)
        self.split_button.pack(side="left", padx=3)
        self.deal_button = tk.Button(self.control_frame, text="Deal New Round", command=self.deal_initial_hands, state=tk.DISABLED)
        self.deal_button.pack(side="left", padx=3)
        self.autoplay_button = tk.Button(self.control_frame, text="Autoplay Off", command=self.toggle_autoplay, bg="#555", fg="white")
        self.autoplay_button.pack(side="left", padx=10)

        self.status_bar = tk.Label(self.root, text="Game: Enter settings and click Start Game", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#087830", fg="white")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def toggle_autoplay(self):
        self.autoplay = not self.autoplay
        state = "On" if self.autoplay else "Off"
        color = "#4caf50" if self.autoplay else "#555"
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
            self.status_bar.config(text=f"Error: {e}", fg="#ff6b6b")
            return

        self.total_starting_balance = starting_balance * num_players
        self.round_number = 0
        self.profit_loss_label.config(text="Total P/L: $0.00", fg="white")
        self.round_label.config(text="Round: 0")

        self.settings_frame.pack_forget()
        self.game_frame.pack()
        self.status_bar.config(text="Game: Settings applied. Click 'Deal New Round' to start.", fg="white")
        self.deal_button.config(state=tk.NORMAL)

        for widget in self.player_container.winfo_children():
            widget.destroy()
        self.players.clear()

        for i in range(num_players):
            player = Player(self.player_container, i, starting_balance, default_bet)
            self.players.append(player)
            self.player_container.grid_columnconfigure(i, weight=1, uniform="player")
        
        self.enable_player_controls(False)

    def deal_initial_hands(self):
        self.round_number += 1
        self.round_label.config(text=f"Round: {self.round_number}")
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer.reset()
        
        all_players_can_bet = True
        for player in self.players:
            player.reset()
            if not player.place_bet(get_bet_amount):
                self.status_bar.config(text=f"Player {player.player_index + 1} has insufficient funds. Autoplay stopped.", fg="#ff6b6b")
                if self.autoplay:
                    self.toggle_autoplay()
                all_players_can_bet = False
        if not all_players_can_bet: return

        for player in self.players:
            player.hands[0].add_card(self.deck.deal_card())
            player.hands[0].add_card(self.deck.deal_card())
            player.update_gui()

        self.dealer.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())
        self.dealer.update_gui()

        self.current_player_index = 0
        self.current_hand_index = 0
        self.status_bar.config(text="Game: Dealing cards...", fg="white")
        
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
        if current_hand.status != "active":
            self.next_turn_or_hand()
            return

        current_player.update_gui()

        dealer_upcard_value = self.dealer.get_up_card()[0]
        recommendation = get_recommendation(current_hand, dealer_upcard_value, current_player.playing_strategy.get())
        current_player.recommendation_label.config(text=f"Recommendation: {recommendation}")

        player_id_str = f"Player {self.current_player_index + 1}"
        hand_id_str = f", Hand {self.current_hand_index + 1}" if len(current_player.hands) > 1 else ""
        self.status_bar.config(text=f"Game: {player_id_str}{hand_id_str}'s turn.", fg="white")

        if current_hand.has_blackjack:
            current_hand.status = "blackjack"
            self.root.after(self.autoplay_speed, self.next_turn_or_hand)
            return
        elif current_hand.hand_value == 21:
             current_hand.status = "stand"
             self.root.after(self.autoplay_speed, self.next_turn_or_hand)
             return

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
            new_rec = get_recommendation(hand, self.dealer.get_up_card()[0], player.playing_strategy.get(), ignore_pairs=True)
            action_func = action_map.get(new_rec, self.hit)

        if action_func:
            self.root.after(self.autoplay_speed, action_func)

    def next_turn_or_hand(self):
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
        if player and hand and hand.status == "active":
            hand.add_card(self.deck.deal_card())
            player.update_gui()

            if hand.is_busted:
                hand.status = "bust"
                player.update_gui()
                self.root.after(self.autoplay_speed, self.next_turn_or_hand)
            else:
                self.check_current_player_status()

    def stand(self):
        player, hand = self.get_current_hand()
        if player and hand and hand.status == "active":
            hand.status = "stand"
            player.update_gui()
            self.root.after(self.autoplay_speed, self.next_turn_or_hand)

    def double_down(self):
        if not self.is_action_possible('double'):
            if self.autoplay: self.hit()
            return
        player, hand = self.get_current_hand()
        player.balance -= hand.bet
        hand.bet *= 2
        hand.add_card(self.deck.deal_card())
        hand.status = "stand" if not hand.is_busted else "bust"
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
        hand.add_card(self.deck.deal_card())
        new_hand.add_card(self.deck.deal_card())
        player.update_gui()
        self.check_current_player_status()

    def is_action_possible(self, action):
        player, hand = self.get_current_hand()
        if not player or not hand or hand.status != 'active':
            return False
        if action == 'double':
            return len(hand.cards) == 2 and player.balance >= hand.bet
        if action == 'split':
            return player.can_split(hand) and player.balance >= hand.bet
        return True

    def enable_player_controls(self, enable):
        if self.autoplay:
            enable = False

        state = tk.NORMAL if enable else tk.DISABLED
        self.hit_button.config(state=state)
        self.stand_button.config(state=state)
        self.double_down_button.config(state=tk.NORMAL if enable and self.is_action_possible('double') else tk.DISABLED)
        self.split_button.config(state=tk.NORMAL if enable and self.is_action_possible('split') else tk.DISABLED)

    def dealer_play(self):
        self.enable_player_controls(False)
        self.status_bar.config(text="Game: Dealer's turn...", fg="white")
        self.dealer.reveal_hole_card()
        self.dealer.update_gui()

        all_busted = all(all(hand.is_busted for hand in p.hands) for p in self.players)
        if all_busted:
            self.root.after(self.autoplay_speed, self.show_results)
            return

        self.root.after(self.autoplay_speed, self._dealer_hit_loop)

    def _dealer_hit_loop(self):
        if self.dealer.get_hand_value() < 17:
            self.dealer.add_card(self.deck.deal_card())
            self.dealer.update_gui()
            self.root.after(self.autoplay_speed, self._dealer_hit_loop)
        else:
            self.root.after(self.autoplay_speed, self.show_results)

    def show_results(self):
        dealer_total = self.dealer.get_hand_value()
        dealer_busted = self.dealer.is_busted
        dealer_has_blackjack = len(self.dealer.hand) == 2 and dealer_total == 21

        for i, player in enumerate(self.players):
            for j, hand in enumerate(player.hands):
                if hand.is_busted:
                    player.record_loss(hand)
                    hand.result_text = "Bust! Lost"
                    hand.result_color = "#ff6b6b"
                elif hand.has_blackjack:
                    if dealer_has_blackjack:
                        player.record_push(hand)
                        hand.result_text = "Push (Blackjack)"
                        hand.result_color = "#4a90e2"
                    else:
                        player.record_win(hand, payout_multiplier=1.5)
                        hand.result_text = "Blackjack! Win (3:2)"
                        hand.result_color = "#4caf50"
                elif dealer_busted:
                    player.record_win(hand)
                    hand.result_text = "Win (Dealer Busts)"
                    hand.result_color = "#4caf50"
                elif hand.hand_value > dealer_total:
                    player.record_win(hand)
                    hand.result_text = "Win"
                    hand.result_color = "#4caf50"
                elif hand.hand_value < dealer_total:
                    player.record_loss(hand)
                    hand.result_text = "Lost"
                    hand.result_color = "#ff6b6b"
                else:  # Push
                    player.record_push(hand)
                    hand.result_text = "Push"
                    hand.result_color = "#4a90e2"
            player.update_gui()

        current_total_balance = sum(p.balance for p in self.players)
        profit_loss = current_total_balance - self.total_starting_balance
        
        color = "#4caf50" if profit_loss > 0 else "#ff6b6b" if profit_loss < 0 else "white"
        self.profit_loss_label.config(text=f"Total P/L: ${profit_loss:+.2f}", fg=color)

        self.enable_player_controls(False)
        if self.autoplay:
            self.root.after(2000, self.deal_initial_hands)
        else:
            self.deal_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackSimulator(root)
    root.mainloop()
