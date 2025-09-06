import tkinter as tk

class Dealer:
    def __init__(self, root):
        self.root = root
        self.hand = []
        self.hand_value = 0
        self.is_busted = False
        self.hole_card_hidden = True

        self.frame = None
        self.hand_container = None
        self.title_label = None

    def create_gui_elements(self, frame):
        self.frame = frame
        self.frame.config(bg="#087830", fg="white", font=("Arial", 10, "bold"))
        self.title_label = tk.Label(self.frame, text="Dealer's Hand", font=("Arial", 10, "bold"), fg="white", bg="#087830")
        self.title_label.pack()
        self.hand_container = tk.Frame(self.frame, bg="#087830")
        self.hand_container.pack(pady=5)

    def add_card(self, card):
        self.hand.append(card)
        self._calculate_hand_value()

    def _calculate_hand_value(self):
        total = 0
        aces = 0
        for val, _ in self.hand:
            if val == 1:  # Ace
                aces += 1
            else:
                total += val

        for _ in range(aces):
            if total + 11 <= 21:
                total += 11
            else:
                total += 1

        self.hand_value = total
        self.is_busted = self.hand_value > 21

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
            placeholder = tk.Frame(self.hand_container, height=50, bg="#087830")
            placeholder.pack()
            return

        for i, card in enumerate(self.hand):
            if self.hole_card_hidden and i == 1:
                card_label = tk.Label(self.hand_container, text="", width=4, height=2, bg="#065c25", relief="raised", borderwidth=2)
            else:
                _, card_repr = card
                suit = card_repr[-1]
                color = "red" if suit in ['♥', '♦'] else "black"
                card_label = tk.Label(self.hand_container, text=card_repr, font=("Arial", 24, "bold"), fg=color, bg="white", padx=5, pady=5, relief="raised", borderwidth=2)
            card_label.pack(side="left", padx=2, pady=2)
