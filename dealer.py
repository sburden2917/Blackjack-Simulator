class Dealer:
    def __init__(self):
        self.hand = []
        self.hand_value = 0
        self.is_busted = False

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

    def get_hand_value(self):
        return self.hand_value

    def get_hand(self):
        return self.hand

    def get_up_card(self):
        if self.hand:
            return self.hand[0]
        return None

    def reset(self):
        self.hand = []
        self.hand_value = 0
        self.is_busted = False