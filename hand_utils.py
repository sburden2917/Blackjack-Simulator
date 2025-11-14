"""Utility functions for hand value calculations."""

def calculate_hand_value(cards):
    """
    Calculate the value of a blackjack hand.
    
    Args:
        cards: List of tuples (value, card_repr) representing cards
        
    Returns:
        tuple: (hand_value, is_busted, has_blackjack)
    """
    total = 0
    aces = sum(1 for val, _ in cards if val == 1)
    non_ace_total = sum(val for val, _ in cards if val != 1)
    total = non_ace_total
    
    for _ in range(aces):
        if total + 11 <= 21:
            total += 11
        else:
            total += 1
    
    is_busted = total > 21
    has_blackjack = len(cards) == 2 and total == 21
    
    return total, is_busted, has_blackjack

