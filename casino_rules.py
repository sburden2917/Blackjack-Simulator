"""Casino rule variations and configurations."""

from typing import Dict, Optional
from constants import DEALER_STAND_VALUE


class CasinoRules:
    """Manages casino rule variations."""
    
    def __init__(self):
        # Dealer rules
        self.dealer_hits_soft_17 = False  # True = dealer hits soft 17
        self.dealer_peeks_for_blackjack = True  # Dealer checks for blackjack before play
        
        # Player options
        self.insurance_available = True  # Insurance bet available
        self.surrender_available = True  # Surrender option available
        self.surrender_type = "late"  # "early" or "late" surrender
        self.double_after_split = True  # Can double after splitting
        self.resplit_aces = False  # Can resplit aces
        self.blackjack_pays_3to2 = True  # True = 3:2, False = 6:5
        
        # Other rules
        self.max_splits = 4  # Maximum number of splits allowed
        
    def get_dealer_stand_value(self, dealer_hand_value: int, is_soft: bool) -> bool:
        """Determine if dealer should stand based on rules."""
        if dealer_hand_value >= 18:
            return True
        if dealer_hand_value == 17:
            if is_soft and self.dealer_hits_soft_17:
                return False  # Hit soft 17
            return True  # Stand on hard 17 or soft 17 (if rule says stand)
        return False  # Hit on 16 or less
    
    def should_offer_insurance(self, dealer_upcard_value: int) -> bool:
        """Check if insurance should be offered."""
        return self.insurance_available and dealer_upcard_value == 1  # Ace
    
    def can_surrender(self, hand_cards: int, dealer_upcard_value: int) -> bool:
        """Check if surrender is available."""
        if not self.surrender_available:
            return False
        # Surrender only available on first two cards
        if hand_cards != 2:
            return False
        # Late surrender: after dealer checks for blackjack
        # Early surrender: before dealer checks
        return True
    
    def get_insurance_payout(self) -> float:
        """Get insurance payout (typically 2:1)."""
        return 2.0
    
    def get_blackjack_payout_multiplier(self) -> float:
        """Get blackjack payout multiplier."""
        return 1.5 if self.blackjack_pays_3to2 else 1.2  # 3:2 or 6:5
    
    def get_house_edge_impact(self) -> Dict[str, float]:
        """Get house edge impact of each rule (in percentage points)."""
        impact = {}
        
        if self.dealer_hits_soft_17:
            impact["Dealer Hits Soft 17"] = +0.22  # Increases house edge
        else:
            impact["Dealer Stands on Soft 17"] = 0.0
        
        if self.surrender_available:
            if self.surrender_type == "late":
                impact["Late Surrender"] = -0.08  # Reduces house edge
            else:
                impact["Early Surrender"] = -0.39  # Better for player
        
        if not self.double_after_split:
            impact["No Double After Split"] = +0.14
        
        if not self.resplit_aces:
            impact["No Resplit Aces"] = +0.03
        
        if not self.blackjack_pays_3to2:
            impact["Blackjack Pays 6:5"] = +1.39  # Much worse for player
        
        return impact

