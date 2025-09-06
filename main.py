import tkinter as tk
import random
from deck import Deck
from player import Player
from dealer import Dealer
from blackjack_strategy import get_recommendation

class BlackjackSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Simulator")

        self.deck = Deck()
        self.players = []
        self.dealer = Dealer(self.root) # Pass root for dealer's GUI elements

        self.current_player_index = 0
        self.num_players = 1 # Default

        self.create_widgets()
        self.setup_game_settings() # Call a new method for initial settings

    def create_widgets(self):
        # Settings Frame
        self.settings_frame = tk.LabelFrame(self.root, text="Game Settings", padx=10, pady=10)
        self.settings_frame.pack(pady=5)

        tk.Label(self.settings_frame, text="Number of Players (1-7):").grid(row=0, column=0, sticky="w")
        self.num_players_entry = tk.Entry(self.settings_frame, width=5)
        self.num_players_entry.insert(0, "1")
        self.num_players_entry.grid(row=0, column=1, sticky="w")

        tk.Label(self.settings_frame, text="Starting Balance per Player:").grid(row=1, column=0, sticky="w")
        self.starting_balance_entry = tk.Entry(self.settings_frame, width=10)
        self.starting_balance_entry.insert(0, "1000")
        self.starting_balance_entry.grid(row=1, column=1, sticky="w")

        tk.Label(self.settings_frame, text="Default Bet per Player:").grid(row=2, column=0, sticky="w")
        self.default_bet_entry = tk.Entry(self.settings_frame, width=10)
        self.default_bet_entry.insert(0, "10")
        self.default_bet_entry.grid(row=2, column=1, sticky="w")

        self.start_button = tk.Button(self.settings_frame, text="Start Game", command=self.setup_game)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Main Game Frame (initially hidden)
        self.game_frame = tk.Frame(self.root)
        # self.game_frame.pack() # Pack only after settings are done

        # Dealer Frame (inside game_frame)
        self.dealer_frame = tk.LabelFrame(self.game_frame, text="Dealer", padx=10, pady=10)
        self.dealer_frame.pack(fill="x", padx=10, pady=5)
        self.dealer.create_gui_elements(self.dealer_frame) # Let dealer create its own labels

        # Player Container Frame (inside game_frame)
        self.player_container = tk.Frame(self.game_frame)
        self.player_container.pack(pady=5)

        # Control Frame (inside game_frame)
        self.control_frame = tk.Frame(self.game_frame)
        self.control_frame.pack(pady=5)
        tk.Button(self.control_frame, text="Hit", command=self.hit).pack(side="left", padx=3)
        tk.Button(self.control_frame, text="Stand", command=self.stand).pack(side="left", padx=3)
        tk.Button(self.control_frame, text="Double Down", command=self.double_down).pack(side="left", padx=3)
        tk.Button(self.control_frame, text="Split", command=self.split).pack(side="left", padx=3)
        self.deal_button = tk.Button(self.control_frame, text="Deal New Round", command=self.deal_initial_hands, state=tk.DISABLED)
        self.deal_button.pack(side="left", padx=3)

        # Status bar at bottom
        self.status_bar = tk.Label(self.root, text="Game: Enter settings and click Start Game", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_game_settings(self):
        # This method is called initially to show settings
        self.settings_frame.pack()
        self.game_frame.pack_forget() # Ensure game frame is not packed yet

    def setup_game(self):
        try:
            self.num_players = int(self.num_players_entry.get())
            if not (1 <= self.num_players <= 7):
                raise ValueError("Number of players must be between 1 and 7.")

            starting_balance = int(self.starting_balance_entry.get())
            if starting_balance <= 0:
                raise ValueError("Starting balance must be positive.")

            default_bet = int(self.default_bet_entry.get())
            if default_bet <= 0:
                raise ValueError("Default bet must be positive.")

        except ValueError as e:
            self.status_bar.config(text=f"Error: {e}", fg="red")
            return

        # Hide settings, show game
        self.settings_frame.pack_forget()
        self.game_frame.pack()
        self.status_bar.config(text="Game: Settings applied. Click 'Deal New Round' to start.", fg="black")
        self.deal_button.config(state=tk.NORMAL) # Enable deal button

        # Clear existing players
        for widget in self.player_container.winfo_children():
            widget.destroy()
        self.players.clear()

        # Create Player objects
        for i in range(self.num_players):
            player = Player(self.player_container, i, starting_balance, default_bet)
            self.players.append(player)
            # Configure grid for player frames
            self.player_container.grid_columnconfigure(i, weight=1)

        self.deal_initial_hands() # Automatically deal first round

    def deal_initial_hands(self):
        self.deck = Deck() # New deck for each round
        self.deck.shuffle()
        self.dealer.reset()

        for player in self.players:
            player.reset()
            player.place_bet() # Player places bet
            player.add_card(self.deck.deal_card())
            player.add_card(self.deck.deal_card())
            player.update_gui() # Update GUI after cards and bet

        # Deal dealer's hand
        self.dealer.add_card(self.deck.deal_card()) # Up card
        self.dealer.add_card(self.deck.deal_card(hidden=True)) # Hole card
        self.dealer.update_gui()

        self.current_player_index = 0
        self.status_bar.config(text="Game: Dealing cards...", fg="black")
        self.enable_player_controls(True)
        self.deal_button.config(state=tk.DISABLED)
        self.check_current_player_status() # Start first player's turn

    def check_current_player_status(self):
        if self.current_player_index < len(self.players):
            current_player = self.players[self.current_player_index]
            current_player.status = "active" # Ensure status is active for turn
            current_player.update_gui() # Highlight current player

            # Update recommendation for the current player
            dealer_upcard_value = self.dealer.get_up_card()[0] # Get value of dealer's up card
            recommendation = get_recommendation(current_player.get_hand(), dealer_upcard_value)
            current_player.recommendation_label.config(text=f"Rec: {recommendation}")

            self.status_bar.config(text=f"Game: Player {self.current_player_index + 1}'s turn.", fg="black")

            # Check for immediate Blackjack
            if current_player.get_hand_value() == 21 and len(current_player.get_hand()) == 2:
                current_player.has_blackjack = True
                self.status_bar.config(text=f"Game: Player {self.current_player_index + 1} has Blackjack!", fg="green")
                self.root.after(1000, self.stand) # Auto-stand for Blackjack
        else:
            self.dealer_play()

    def hit(self):
        if self.current_player_index < len(self.players):
            current_player = self.players[self.current_player_index]
            if current_player.status == "active":
                card = self.deck.deal_card()
                current_player.add_card(card)
                current_player.update_gui()

                if current_player.is_busted:
                    current_player.status = "bust"
                    current_player.update_gui()
                    self.status_bar.config(text=f"Game: Player {self.current_player_index + 1} BUSTS!", fg="red")
                    self.root.after(1000, self.next_player_turn) # Move to next player after a short delay
                else:
                    # Update recommendation after hit
                    dealer_upcard_value = self.dealer.get_up_card()[0]
                    recommendation = get_recommendation(current_player.get_hand(), dealer_upcard_value)
                    current_player.recommendation_label.config(text=f"Rec: {recommendation}")
            else:
                self.status_bar.config(text="Game: Not your turn or already stood/busted.", fg="orange")

    def stand(self):
        if self.current_player_index < len(self.players):
            current_player = self.players[self.current_player_index]
            if current_player.status == "active":
                current_player.status = "stand"
                current_player.update_gui()
                self.status_bar.config(text=f"Game: Player {self.current_player_index + 1} stands.", fg="blue")
                self.root.after(500, self.next_player_turn) # Short delay before next turn
            else:
                self.status_bar.config(text="Game: Not your turn or already stood/busted.", fg="orange")

    def double_down(self):
        if self.current_player_index < len(self.players):
            current_player = self.players[self.current_player_index]
            if current_player.status == "active" and len(current_player.get_hand()) == 2:
                if current_player.balance >= current_player.bet * 2:
                    current_player.double_bet()
                    card = self.deck.deal_card()
                    current_player.add_card(card)
                    current_player.status = "stand" # Auto-stand after double down
                    current_player.update_gui()
                    self.status_bar.config(text=f"Game: Player {self.current_player_index + 1} doubled down.", fg="purple")
                    self.root.after(500, self.next_player_turn)
                else:
                    self.status_bar.config(text="Game: Not enough balance to double down.", fg="red")
            else:
                self.status_bar.config(text="Game: Can only double down on first two cards.", fg="orange")

    def split(self):
        self.status_bar.config(text="Game: Split functionality not yet implemented.", fg="orange")
        # This will be more complex, requiring new Player objects for split hands

    def next_player_turn(self):
        self.current_player_index += 1
        self.check_current_player_status()

    def enable_player_controls(self, enable):
        state = tk.NORMAL if enable else tk.DISABLED
        for btn in self.control_frame.winfo_children():
            if btn != self.deal_button: # Don't disable the deal button
                btn.config(state=state)

    def dealer_play(self):
        self.enable_player_controls(False) # Disable player controls during dealer's turn
        self.status_bar.config(text="Game: Dealer's turn...", fg="black")
        self.dealer.reveal_hole_card()
        self.dealer.update_gui() # Show revealed card

        # Check if all players busted or have blackjack (no need for dealer to play)
        all_players_busted_or_blackjack = True
        for player in self.players:
            if not player.is_busted and not player.has_blackjack:
                all_players_busted_or_blackjack = False
                break

        if all_players_busted_or_blackjack:
            self.status_bar.config(text="Game: All players busted or have Blackjack. Dealer does not play.", fg="blue")
            self.root.after(1000, self.show_results)
            return

        # Dealer hits on 16 or less, stands on 17 or more
        self._dealer_hit_loop()

    def _dealer_hit_loop(self):
        dealer_total = self.dealer.get_hand_value()
        if dealer_total < 17:
            card = self.deck.deal_card()
            self.dealer.add_card(card)
            self.dealer.update_gui()
            self.status_bar.config(text=f"Game: Dealer hits. Hand: {self.dealer.get_hand_value()}", fg="black")
            self.root.after(1000, self._dealer_hit_loop) # Continue hitting after delay
        else:
            self.status_bar.config(text=f"Game: Dealer stands at {dealer_total}.", fg="blue")
            self.root.after(1000, self.show_results) # Proceed to results after dealer stands

    def show_results(self):
        dealer_total = self.dealer.get_hand_value()
        dealer_busted = self.dealer.is_busted

        self.status_bar.config(text="Game: Determining results...", fg="black")

        for player in self.players:
            player_total = player.get_hand_value()
            result_text = ""
            result_color = "black"

            if player.is_busted:
                player.lose_bet()
                result_text = "BUST! Lost"
                result_color = "red"
            elif player.has_blackjack:
                if dealer_total == 21 and len(self.dealer.get_hand()) == 2: # Dealer also has Blackjack
                    player.push_bet()
                    result_text = "Push (Blackjack)"
                    result_color = "blue"
                else:
                    player.blackjack_payout()
                    result_text = "Blackjack! Win (3:2)"
                    result_color = "green"
            elif dealer_busted:
                player.win_bet()
                result_text = "Win (Dealer Busts)"
                result_color = "green"
            elif player_total > dealer_total:
                player.win_bet()
                result_text = "Win"
                result_color = "green"
            elif player_total < dealer_total:
                player.lose_bet()
                result_text = "Lost"
                result_color = "red"
            else: # player_total == dealer_total
                player.push_bet()
                result_text = "Push"
                result_color = "blue"
            
            player.result_label.config(text=result_text, fg=result_color)
            player.update_gui() # Update balance and bet display

        self.status_bar.config(text="Game: Round over. Click 'Deal New Round' for next game.", fg="black")
        self.deal_button.config(state=tk.NORMAL) # Enable deal button for next round

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackSimulator(root)
    root.mainloop()