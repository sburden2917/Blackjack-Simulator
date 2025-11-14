"""Probability calculations for blackjack decisions."""

from typing import Dict, Tuple
import math


def calculate_bust_probability(hand_value: int, is_soft: bool = False) -> float:
    """Calculate probability of busting on next card.
    
    Simplified calculation based on remaining cards in deck.
    For a full deck, probability of busting is:
    - Cards that would cause bust / Total cards remaining
    """
    if hand_value >= 21:
        return 0.0  # Already at or over 21
    
    if is_soft:
        # Soft hands can't bust on next card (ace can become 1)
        if hand_value <= 11:
            return 0.0
        # If soft hand value is 12-20, only 10-value cards can bust
        # (and only if ace becomes 1, making it hard)
        if hand_value == 12:
            return 0.0  # Can't bust
        elif hand_value <= 20:
            # Only busts if we get a card that makes ace = 1 and total > 21
            # This is complex, simplified: very low probability
            return 0.0
    
    # Hard hand bust probability
    # Cards that would cause bust: any card that makes total > 21
    cards_that_bust = 0
    
    if hand_value <= 11:
        return 0.0  # Can't bust
    elif hand_value == 12:
        # Only 10-value cards bust (10, J, Q, K) = 16 cards out of 52
        cards_that_bust = 16
    elif hand_value == 13:
        # 9, 10-value cards bust = 20 cards
        cards_that_bust = 20
    elif hand_value == 14:
        # 8, 9, 10-value cards bust = 24 cards
        cards_that_bust = 24
    elif hand_value == 15:
        # 7, 8, 9, 10-value cards bust = 28 cards
        cards_that_bust = 28
    elif hand_value == 16:
        # 6, 7, 8, 9, 10-value cards bust = 32 cards
        cards_that_bust = 32
    elif hand_value == 17:
        # 5, 6, 7, 8, 9, 10-value cards bust = 36 cards
        cards_that_bust = 36
    elif hand_value == 18:
        # 4, 5, 6, 7, 8, 9, 10-value cards bust = 40 cards
        cards_that_bust = 40
    elif hand_value == 19:
        # 3, 4, 5, 6, 7, 8, 9, 10-value cards bust = 44 cards
        cards_that_bust = 44
    elif hand_value == 20:
        # 2, 3, 4, 5, 6, 7, 8, 9, 10-value cards bust = 48 cards
        cards_that_bust = 48
    else:
        return 1.0  # Already over 21
    
    # Simplified: assume full deck (52 cards)
    # In reality, this should account for cards already seen
    return cards_that_bust / 52.0


def calculate_win_probability(player_value: int, dealer_upcard: int, is_soft: bool = False) -> float:
    """Estimate win probability based on player hand and dealer upcard.
    
    This is a simplified calculation. Real probability requires
    complex simulation of all possible outcomes.
    """
    # Simplified win probability estimates
    if player_value > 21:
        return 0.0
    if player_value == 21:
        return 0.95  # Very high win probability
    
    # Base win probability on hand value
    base_win_prob = {
        20: 0.85, 19: 0.75, 18: 0.65, 17: 0.55,
        16: 0.45, 15: 0.35, 14: 0.25, 13: 0.20,
        12: 0.15, 11: 0.10, 10: 0.08, 9: 0.05,
        8: 0.03, 7: 0.02, 6: 0.01, 5: 0.01
    }
    
    prob = base_win_prob.get(player_value, 0.0)
    
    # Adjust based on dealer upcard
    if dealer_upcard in [2, 3, 4, 5, 6]:
        # Dealer weak card - increase win probability
        prob += 0.15
    elif dealer_upcard in [7, 8, 9]:
        # Dealer medium card - slight decrease
        prob -= 0.05
    elif dealer_upcard in [10, 1]:  # 10 or Ace
        # Dealer strong card - decrease win probability
        prob -= 0.20
    
    # Soft hands have slightly better odds
    if is_soft:
        prob += 0.05
    
    return max(0.0, min(1.0, prob))


def get_action_probabilities(
    player_hand_value: int,
    dealer_upcard: int,
    is_soft: bool = False,
    can_double: bool = False,
    can_split: bool = False
) -> Dict[str, Tuple[float, str]]:
    """Get probability estimates for different actions.
    
    Returns dict with action -> (probability, description)
    """
    bust_prob = calculate_bust_probability(player_hand_value, is_soft)
    win_prob = calculate_win_probability(player_hand_value, dealer_upcard, is_soft)
    
    results = {}
    
    # Hit probability
    hit_win_prob = win_prob * (1 - bust_prob)  # Win if don't bust
    results["Hit"] = (hit_win_prob, f"Bust risk: {bust_prob*100:.1f}%")
    
    # Stand probability
    results["Stand"] = (win_prob, f"Current win chance: {win_prob*100:.1f}%")
    
    # Double down (if possible)
    if can_double:
        # Double has same win prob as hit, but with 2x bet
        results["Double Down"] = (hit_win_prob, f"2x bet, {hit_win_prob*100:.1f}% win chance")
    
    # Split (if possible)
    if can_split:
        # Splitting generally improves odds for pairs
        split_win_prob = win_prob + 0.10  # Rough estimate
        results["Split"] = (min(1.0, split_win_prob), "Creates two hands")
    
    return results

