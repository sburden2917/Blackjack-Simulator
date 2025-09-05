import tkinter as tk
import random


class BlackjackSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Simulator - 7-Player Table")
        self.players = []  # Players 1-7
        self.dealer_hand = []
        self.num_players = 1
        self.player_status = {}  # Track status: "active", "stand", "bust"
        self.create_widgets()
        self.setup_game()

    def create_widgets(self):
        tk.Label(self.root, text="Players:").pack(pady=(10, 0))
        self.player_count = tk.IntVar(value=1)
        tk.OptionMenu(self.root, self.player_count, *range(1, 8),
                      command=self.update_players).pack()

        self.player_container = tk.Frame(self.root)
        self.player_container.pack(pady=10, fill="x")

        self.dealer_frame = tk.LabelFrame(self.root, text="Dealer", padx=10, pady=10)
        self.dealer_frame.pack(fill="x", padx=10, pady=5)
        self.dealer_label = tk.Label(self.dealer_frame, text="Hand: [ ] = 0", font=("Arial", 10))
        self.dealer_label.pack()
        self.dealer_status = tk.Label(self.dealer_frame, text="Dealer: Waiting...")
        self.dealer_status.pack()

        # Status bar at bottom (removed as per requirement)
        self.status_bar = tk.Label(self.root, text="Game: Deal cards", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(self.root, text="Actions:").pack()
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=5)
        tk.Button(self.control_frame, text="Double Down", command=self.double_down).pack(side="left", padx=3)
        tk.Button(self.control_frame, text="Split", command=self.split).pack(side="left", padx=3)

    def setup_game(self):
        self.update_players(1)

    def update_players(self, num):
        self.num_players = num
        for widget in self.player_container.winfo_children():
            widget.destroy()

        self.players = []
        self.player_status = {}
        for i in range(num):
            player_frame = tk.LabelFrame(self.player_container, text=f"Player {i + 1}")
            player_frame.pack(fill="x", padx=10, pady=3, anchor="w")

            # Create three-column layout: Bet | Hand | Recommendation/Result
            player_info_frame = tk.Frame(player_frame)
            player_info_frame.pack(fill="x", padx=5, pady=2)

            # Left: Bet amount ($10 fixed for simplicity)
            bet_label = tk.Label(player_info_frame, text="Bet: $10", anchor="w", width=10)
            bet_label.pack(side="left", padx=5)

            # Middle: Hand display
            hand_label = tk.Label(player_info_frame, text="Hand: [ ] = 0", font=("Arial", 10), width=25)
            hand_label.pack(side="left", padx=5)

            # Right: Recommendation and Result
            rec_label = tk.Label(player_info_frame, text="Recommendation: ", anchor="e", width=20)
            rec_label.pack(side="right", padx=5)
            result_label = tk.Label(player_info_frame, text="Result: ", anchor="e", width=15)
            result_label.pack(side="right", padx=5)

            # Status label (below the three-column layout)
            status_label = tk.Label(player_frame, text="Status: Active", fg="black")
            status_label.pack(pady=(0, 5))

            # Buttons
            btn_frame = tk.Frame(player_frame)
            btn_frame.pack(pady=5)
            tk.Button(btn_frame, text="Hit", command=lambda p=i: self.hit(p)).pack(side="left", padx=3)
            tk.Button(btn_frame, text="Stand", command=lambda p=i: self.stand(p)).pack(side="left", padx=3)

            self.players.append({
                'hand': [],
                'hand_label': hand_label,
                'status_label': status_label,
                'recommendation_label': rec_label,
                'result_label': result_label,
                'index': i
            })
            self.player_status[i] = "active"

        self.deal_initial_hands()

    def deal_initial_hands(self):
        for player in self.players:
            player['hand'] = [self.get_card() for _ in range(2)]
            self.update_player_hand(player['index'])

        self.dealer_hand = [self.get_card(), self.get_card()]
        self.update_dealer_hand()
        self.status_bar.config(text="Game: Cards dealt. Players take turns.")

    def get_card(self):
        num = random.randint(1, 13)
        if num == 1:
            return (1, 'A')
        elif 11 <= num <= 13:
            return (10, ['J', 'Q', 'K'][num - 11])
        else:
            return (num, str(num))

    def update_player_hand(self, player_index):
        player = self.players[player_index]
        display_hand = [card[1] for card in player['hand']]
        total = self.calculate_hand(player['hand'])
        player['hand_label'].config(text=f"Hand: {display_hand} = {total}")

        if total > 21:
            player['status_label'].config(text="Status: BUST!", fg="red")
            self.player_status[player_index] = "bust"
            self.check_all_players_done()

    def update_dealer_hand(self):
        hidden = [self.dealer_hand[0][1], "?"]
        total = self.calculate_hand(self.dealer_hand)
        self.dealer_label.config(text=f"Hand: {hidden} = {self.dealer_hand[0][0]}")
        self.dealer_status.config(text="Dealer: Waiting...")

    def calculate_hand(self, hand):
        total = 0
        aces = 0
        for val, _ in hand:
            if val == 1:
                aces += 1
            else:
                total += val

        for _ in range(aces):
            if total + 11 <= 21:
                total += 11
            else:
                total += 1
        return total

    def hit(self, player_index):
        self.players[player_index]['hand'].append(self.get_card())
        self.update_player_hand(player_index)

    def stand(self, player_index):
        self.player_status[player_index] = "stand"
        self.players[player_index]['status_label'].config(text="Status: Stand", fg="blue")
        
        # Update recommendation after player stands
        dealer_upcard = self.dealer_hand[0][0]
        rec = self.get_basic_strategy_recommendation(self.players[player_index]['hand'], dealer_upcard)
        self.players[player_index]['recommendation_label'].config(text=f"Recommendation: {rec}")
        
        self.check_all_players_done()

    def get_basic_strategy_recommendation(self, hand, dealer_upcard):
        """Simple basic strategy implementation"""
        total = self.calculate_hand(hand)
        
        # Dealer upcard 2-6: Stand on 12+ (weak dealer)
        if dealer_upcard <= 6:
            return "Stand" if total >= 12 else "Hit"
        # Dealer upcard 7-A: Stand on 17+ (strong dealer)
        else:
            return "Stand" if total >= 17 else "Hit"

    def check_all_players_done(self):
        """Check if all players have stood or busted"""
        if all(status in ["stand", "bust"] for status in self.player_status.values()):
            self.dealer_play()

    def dealer_play(self):
        self.status_bar.config(text="Game: Dealer's turn...")
        self.dealer_status.config(text="Dealer: Playing...")

        # Reveal dealer hand
        self.dealer_label.config(text=f"Hand: {self.dealer_hand} = {self.calculate_hand(self.dealer_hand)}")
        self.dealer_status.config(text="Dealer: Playing...")

        # Dealer hits until 17+
        while self.calculate_hand(self.dealer_hand) < 17:
            self.dealer_hand.append(self.get_card())
            self.dealer_label.config(text=f"Hand: {self.dealer_hand} = {self.calculate_hand(self.dealer_hand)}")
            self.root.update_idletasks()
            self.root.after(500)  # Slow animation

        # Final results - now displayed next to each player
        self.show_results()

    def show_results(self):
        dealer_total = self.calculate_hand(self.dealer_hand)
        
        # Update dealer display
        self.dealer_label.config(text=f"Hand: {self.dealer_hand} = {dealer_total}")
        self.dealer_status.config(text=f"Dealer: Final Hand = {dealer_total}")

        # Update results for each player (now displayed next to each player)
        for player in self.players:
            player_total = self.calculate_hand(player['hand'])
            if player_total > 21:
                result = "Bust"
            elif dealer_total > 21:
                result = "Win"
            elif player_total > dealer_total:
                result = "Win"
            elif player_total < dealer_total:
                result = "Loss"
            else:
                result = "Push"
            
            player['result_label'].config(text=f"Result: {result}")

    def double_down(self):
        for player in self.players:
            if len(player['hand']) == 2:
                self.hit(player['index'])

    def split(self):
        for player in self.players:
            if len(player['hand']) == 2 and player['hand'][0][0] == player['hand'][1][0]:
                card = player['hand'].pop()
                player['hand'].append(card)
                self.hit(player['index'])


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("650x550")
    app = BlackjackSimulator(root)
    root.mainloop()