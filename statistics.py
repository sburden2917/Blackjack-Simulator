"""Statistics tracking for blackjack simulator."""

from collections import defaultdict
from typing import Dict, List, Optional


class PlayerStatistics:
    """Track statistics for a single player."""
    
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0
        self.busts = 0
        self.doubles = 0
        self.splits = 0
        self.total_hands = 0
        self.total_bet = 0.0
        self.total_winnings = 0.0
        self.strategy_mistakes = 0
        self.strategy_correct = 0
        self.hands_played = []
        
    def record_hand(self, result: str, bet: float, winnings: float, was_mistake: bool = False):
        """Record a hand result."""
        self.total_hands += 1
        self.total_bet += bet
        self.total_winnings += winnings
        
        if result == "win":
            self.wins += 1
        elif result == "loss":
            self.losses += 1
        elif result == "push":
            self.pushes += 1
        elif result == "blackjack":
            self.blackjacks += 1
        elif result == "bust":
            self.busts += 1
            
        if was_mistake:
            self.strategy_mistakes += 1
        else:
            self.strategy_correct += 1
            
        self.hands_played.append({
            'result': result,
            'bet': bet,
            'winnings': winnings,
            'was_mistake': was_mistake
        })
    
    def record_action(self, action: str):
        """Record a player action."""
        if action == "double":
            self.doubles += 1
        elif action == "split":
            self.splits += 1
    
    def get_win_rate(self) -> float:
        """Calculate win rate (excluding pushes)."""
        total_outcomes = self.wins + self.losses
        if total_outcomes == 0:
            return 0.0
        return (self.wins / total_outcomes) * 100
    
    def get_rtp(self) -> float:
        """Calculate Return to Player percentage."""
        if self.total_bet == 0:
            return 0.0
        return (self.total_winnings / self.total_bet) * 100
    
    def get_strategy_adherence(self) -> float:
        """Calculate strategy adherence percentage."""
        total_decisions = self.strategy_correct + self.strategy_mistakes
        if total_decisions == 0:
            return 100.0
        return (self.strategy_correct / total_decisions) * 100
    
    def get_profit_loss(self) -> float:
        """Calculate total profit/loss."""
        return self.total_winnings - self.total_bet
    
    def get_summary(self) -> Dict:
        """Get summary statistics."""
        return {
            'wins': self.wins,
            'losses': self.losses,
            'pushes': self.pushes,
            'blackjacks': self.blackjacks,
            'busts': self.busts,
            'doubles': self.doubles,
            'splits': self.splits,
            'total_hands': self.total_hands,
            'win_rate': self.get_win_rate(),
            'rtp': self.get_rtp(),
            'strategy_adherence': self.get_strategy_adherence(),
            'profit_loss': self.get_profit_loss(),
            'total_bet': self.total_bet,
            'total_winnings': self.total_winnings
        }


class CardCounting:
    """Hi-Lo card counting system."""
    
    # Hi-Lo values
    CARD_VALUES = {
        1: -1,   # Ace
        2: 1,    # 2
        3: 1,    # 3
        4: 1,    # 4
        5: 1,    # 5
        6: 1,    # 6
        7: 0,    # 7
        8: 0,    # 8
        9: 0,    # 9
        10: -1,  # 10, J, Q, K
    }
    
    def __init__(self, num_decks: int = 8):
        self.num_decks = num_decks
        self.running_count = 0
        self.cards_seen = 0
        self.total_cards = num_decks * 52  # Will be updated as deck is used
        
    def reset(self):
        """Reset counting."""
        self.running_count = 0
        self.cards_seen = 0
        
    def count_card(self, card_value: int):
        """Count a card that's been seen."""
        if card_value > 10:
            card_value = 10
        self.running_count += self.CARD_VALUES.get(card_value, 0)
        self.cards_seen += 1
        
    def get_true_count(self, cards_remaining: int = None) -> float:
        """Calculate true count (running count / decks remaining).
        
        Args:
            cards_remaining: Current number of cards in deck. If None, calculates from total_cards.
        """
        if cards_remaining is not None:
            decks_remaining = cards_remaining / 52.0
        else:
            decks_remaining = (self.total_cards - self.cards_seen) / 52.0
        
        if decks_remaining <= 0:
            return 0.0
        return self.running_count / decks_remaining
    
    def get_betting_unit(self, base_unit: float) -> float:
        """Get recommended bet size based on true count."""
        true_count = self.get_true_count()
        if true_count <= 0:
            return base_unit
        elif true_count <= 1:
            return base_unit
        elif true_count <= 2:
            return base_unit * 2
        elif true_count <= 3:
            return base_unit * 4
        elif true_count <= 4:
            return base_unit * 6
        else:
            return base_unit * 8
    
    def get_count_status(self) -> str:
        """Get human-readable count status."""
        true_count = self.get_true_count()
        if true_count >= 2:
            return "Favorable"
        elif true_count >= 1:
            return "Slightly Favorable"
        elif true_count >= -1:
            return "Neutral"
        elif true_count >= -2:
            return "Slightly Unfavorable"
        else:
            return "Unfavorable"

