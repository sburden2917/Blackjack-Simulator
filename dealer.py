import tkinter as tk
from hand_utils import calculate_hand_value
from constants import BG_COLOR, WHITE, RED_SUIT_COLOR, BLACK_SUIT_COLOR, DARK_GREEN

class Dealer:
    def __init__(self, root):
        self.root = root
        self.hand = []
        self.hand_value = 0
        self.is_busted = False
        self.has_blackjack = False
        self.hole_card_hidden = True

        self.frame = None
        self.hand_container = None
        self.title_label = None

    def create_gui_elements(self, frame):
        self.frame = frame
        self.frame.config(bg=BG_COLOR, fg=WHITE, font=("Arial", 10, "bold"))
        self.title_label = tk.Label(self.frame, text="Dealer's Hand", font=("Arial", 10, "bold"), fg=WHITE, bg=BG_COLOR)
        self.title_label.pack()
        self.hand_container = tk.Frame(self.frame, bg=BG_COLOR)
        self.hand_container.pack(pady=5)

    def add_card(self, card):
        self.hand.append(card)
        self._calculate_hand_value()

    def _calculate_hand_value(self):
        self.hand_value, self.is_busted, self.has_blackjack = calculate_hand_value(self.hand)

    def get_hand_value(self):
        return self.hand_value

    def get_hand(self):
        return self.hand

    def get_up_card(self):
        return self.hand[0] if self.hand else None

    def reset(self):
        self.hand = []
        self.hand_value = 0
        self.is_busted = False
        self.has_blackjack = False
        self.hole_card_hidden = True
        if self.hand_container:
            self.update_gui()

    def reveal_hole_card(self):
        self.hole_card_hidden = False

    def update_gui(self):
        if not self.hand_container:
            return

        for widget in self.hand_container.winfo_children():
            widget.destroy()

        displayed_value = ""
        if not self.hole_card_hidden:
            displayed_value = f"({self.hand_value})"
        elif self.hand:
            up_card_val = self.hand[0][0]
            displayed_value = f"({11 if up_card_val == 1 else up_card_val})"
        
        self.title_label.config(text=f"Dealer's Hand {displayed_value}")

        if not self.hand:
            placeholder = tk.Frame(self.hand_container, height=50, bg=BG_COLOR)
            placeholder.pack()
            return

        for i, card in enumerate(self.hand):
            if self.hole_card_hidden and i == 1:
                card_label = tk.Label(self.hand_container, text="", width=4, height=2, bg=DARK_GREEN, relief="raised", borderwidth=2)
            else:
                _, card_repr = card
                suit = card_repr[-1]
                color = RED_SUIT_COLOR if suit in ['♥', '♦'] else BLACK_SUIT_COLOR
                card_label = tk.Label(self.hand_container, text=card_repr, font=("Arial", 24, "bold"), fg=color, bg="white", padx=5, pady=5, relief="raised", borderwidth=2)
            card_label.pack(side="left", padx=2, pady=2)
