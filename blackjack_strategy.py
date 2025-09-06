# blackjack_strategy.py

# Basic Strategy Chart (Simplified for demonstration)
# 'H': Hit, 'S': Stand, 'D': Double Down, 'P': Split

# Hard Totals (no Ace, or Ace counted as 1)
HARD_TOTALS = {
    17: {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'S', '8': 'S', '9': 'S', '10': 'S', 'A': 'S'},
    16: {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    15: {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    14: {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    13: {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    12: {'2': 'H', '3': 'H', '4': 'S', '5': 'S', '6': 'S', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    11: {'2': 'D', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'D', '8': 'D', '9': 'D', '10': 'D', 'A': 'D'},
    10: {'2': 'D', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'D', '8': 'D', '9': 'D', '10': 'H', 'A': 'H'},
    9: {'2': 'H', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    8: {'2': 'H', '3': 'H', '4': 'H', '5': 'H', '6': 'H', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    # ... and so on for lower totals
}

# Soft Totals (with an Ace counted as 11)
SOFT_TOTALS = {
    19: {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'S', '8': 'S', '9': 'S', '10': 'S', 'A': 'S'},  # A,8
    18: {'2': 'S', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'S', '8': 'S', '9': 'H', '10': 'H', 'A': 'H'},  # A,7
    17: {'2': 'H', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},  # A,6
    16: {'2': 'H', '3': 'H', '4': 'D', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},  # A,5
    15: {'2': 'H', '3': 'H', '4': 'D', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},  # A,4
    14: {'2': 'H', '3': 'H', '4': 'H', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},  # A,3
    13: {'2': 'H', '3': 'H', '4': 'H', '5': 'D', '6': 'D', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},  # A,2
    # ... and so on for lower totals
}

# Pairs
PAIRS = {
    'A': {'2': 'P', '3': 'P', '4': 'P', '5': 'P', '6': 'P', '7': 'P', '8': 'P', '9': 'P', '10': 'P', 'A': 'P'},
    '10': {'2': 'S', '3': 'S', '4': 'S', '5': 'S', '6': 'S', '7': 'S', '8': 'S', '9': 'S', '10': 'S', 'A': 'S'},
    '9': {'2': 'P', '3': 'P', '4': 'P', '5': 'P', '6': 'P', '7': 'S', '8': 'P', '9': 'P', '10': 'S', 'A': 'S'},
    '8': {'2': 'P', '3': 'P', '4': 'P', '5': 'P', '6': 'P', '7': 'P', '8': 'P', '9': 'P', '10': 'P', 'A': 'P'},
    '7': {'2': 'P', '3': 'P', '4': 'P', '5': 'P', '6': 'P', '7': 'P', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '6': {'2': 'P', '3': 'P', '4': 'P', '5': 'P', '6': 'P', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '5': {'2': 'D', '3': 'D', '4': 'D', '5': 'D', '6': 'D', '7': 'D', '8': 'D', '9': 'D', '10': 'D', 'A': 'D'},
    # Treat as hard 10
    '4': {'2': 'H', '3': 'H', '4': 'H', '5': 'P', '6': 'P', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '3': {'2': 'P', '3': 'P', '4': 'P', '5': 'P', '6': 'P', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
    '2': {'2': 'P', '3': 'P', '4': 'P', '5': 'P', '6': 'P', '7': 'H', '8': 'H', '9': 'H', '10': 'H', 'A': 'H'},
}


def get_recommendation(player_hand, dealer_upcard_value):
    """
    Provides a basic strategy recommendation for a given player hand and dealer upcard.
    Assumes standard rules (no surrender, no re-splitting Aces, etc. for simplicity).
    """
    player_total = 0
    num_aces = 0
    is_pair = False
    first_card_value = None

    if len(player_hand) == 2:
        if player_hand[0][0] == player_hand[1][0]:
            is_pair = True
            first_card_value = player_hand[0][1]  # 'A', 'K', 'Q', 'J', '10', '9', etc.

    for val, _ in player_hand:
        if val == 1:  # Ace
            num_aces += 1
            player_total += 11  # Assume 11 initially
        else:
            player_total += val

    # Adjust for Aces if total > 21
    while player_total > 21 and num_aces > 0:
        player_total -= 10  # Change Ace from 11 to 1
        num_aces -= 1

    # Determine if it's a soft total (has an Ace counted as 11)
    is_soft = (num_aces > 0 and player_total <= 21)

    # Convert dealer upcard value to string for dictionary lookup
    dealer_upcard_str = str(dealer_upcard_value)
    if dealer_upcard_value == 1:  # Ace
        dealer_upcard_str = 'A'
    elif dealer_upcard_value >= 10:  # 10, J, Q, K
        dealer_upcard_str = '10'

    # 1. Check for Pairs
    if is_pair and str(first_card_value) in PAIRS:
        return PAIRS[str(first_card_value)].get(dealer_upcard_str, 'H')  # Default to Hit if not found

    # 2. Check for Soft Totals
    if is_soft and player_total in SOFT_TOTALS:
        return SOFT_TOTALS[player_total].get(dealer_upcard_str, 'H')

    # 3. Check for Hard Totals
    if player_total in HARD_TOTALS:
        return HARD_TOTALS[player_total].get(dealer_upcard_str, 'H')

    # Default for totals not covered (e.g., 11 or less, always hit/double)
    if player_total <= 11:
        return 'H'  # Always hit on 11 or less unless it's a double down opportunity (handled by specific 9,10,11 rules)

    return 'H'  # Fallback if no specific rule found