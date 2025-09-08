# strategies.py

RECOMMENDATION_MAP = {
    'H': "Hit",
    'S': "Stand",
    'D': "Double Down",
    'P': "Split"
}

# --- Playing Strategies ---

BASIC_STRATEGY = {
    'hard': {
        17: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 1: 'S'},
        16: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        15: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        14: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        13: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        12: {2: 'H', 3: 'H', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        11: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'D', 1: 'D'},
        10: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'H', 1: 'H'},
        9: {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        8: {2: 'H', 3: 'H', 4: 'H', 5: 'H', 6: 'H', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
    },
    'soft': {
        19: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 1: 'S'},
        18: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'S', 8: 'S', 9: 'H', 10: 'H', 1: 'H'},
        17: {2: 'H', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        16: {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        15: {2: 'H', 3: 'H', 4: 'D', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        14: {2: 'H', 3: 'H', 4: 'H', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        13: {2: 'H', 3: 'H', 4: 'H', 5: 'D', 6: 'D', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
    },
    'pairs': {
        1: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'P', 9: 'P', 10: 'P', 1: 'P'},
        10: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'S', 8: 'S', 9: 'S', 10: 'S', 1: 'S'},
        9: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'S', 8: 'P', 9: 'P', 10: 'S', 1: 'S'},
        8: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'P', 9: 'P', 10: 'P', 1: 'P'},
        7: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        6: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        5: {2: 'D', 3: 'D', 4: 'D', 5: 'D', 6: 'D', 7: 'D', 8: 'D', 9: 'D', 10: 'H', 1: 'H'},
        4: {2: 'H', 3: 'H', 4: 'H', 5: 'P', 6: 'P', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        3: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
        2: {2: 'P', 3: 'P', 4: 'P', 5: 'P', 6: 'P', 7: 'P', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},
    }
}

TEAM_STRATEGY = {
    'hard': {**BASIC_STRATEGY['hard'],
             # More aggressive hitting to take dealer's potential good cards
             16: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},  # Always hit vs 7+
             15: {2: 'S', 3: 'S', 4: 'S', 5: 'S', 6: 'S', 7: 'H', 8: 'H', 9: 'H', 10: 'H', 1: 'H'},  # Always hit vs 7+
             },
    'soft': {**BASIC_STRATEGY['soft']},
    'pairs': {**BASIC_STRATEGY['pairs']}
}

PLAYING_STRATEGIES = {
    "Basic": BASIC_STRATEGY,
    "Team Play": TEAM_STRATEGY
}


def get_recommendation(player_hand, dealer_upcard_value, strategy_name="Basic", ignore_pairs=False):
    strategy = PLAYING_STRATEGIES.get(strategy_name, BASIC_STRATEGY)
    action_code = 'H'

    if not ignore_pairs and len(player_hand.cards) == 2 and player_hand.cards[0][0] == player_hand.cards[1][0]:
        pair_value = player_hand.cards[0][0]
        if pair_value > 10: pair_value = 10
        if pair_value in strategy['pairs']:
            action_code = strategy['pairs'][pair_value].get(dealer_upcard_value, 'H')
    else:
        is_soft = any(val == 1 for val, _ in player_hand.cards) and player_hand.hand_value > sum(
            c[0] for c in player_hand.cards if c[0] != 1) + 1
        if is_soft:
            if player_hand.hand_value in strategy['soft']:
                action_code = strategy['soft'][player_hand.hand_value].get(dealer_upcard_value, 'H')
        elif player_hand.hand_value in strategy['hard']:
            action_code = strategy['hard'][player_hand.hand_value].get(dealer_upcard_value, 'H')

    if player_hand.hand_value >= 21:
        action_code = 'S'
    elif player_hand.hand_value <= 8:
        action_code = 'H'

    return RECOMMENDATION_MAP.get(action_code, "Hit")


# --- Betting Strategies ---

def flat_betting(player, default_bet):
    return default_bet


def martingale(player, default_bet):
    if player.previous_bet_won is False:
        return player.last_bet_amount * 2
    return default_bet


def paroli(player, default_bet):
    if player.previous_bet_won is True:
        return player.last_bet_amount * 2
    return default_bet


def one_three_two_six(player, default_bet):
    if player.previous_bet_won is False:
        player.win_streak = 0
        return default_bet

    player.win_streak += 1
    multipliers = {1: 1, 2: 3, 3: 2, 4: 6}
    multiplier = multipliers.get(player.win_streak, 1)
    if player.win_streak > 4:
        player.win_streak = 1  # Reset after completing sequence

    return default_bet * multiplier


BETTING_STRATEGIES = {
    "Flat": flat_betting,
    "Martingale": martingale,
    "Paroli": paroli,
    "1-3-2-6": one_three_two_six
}


def get_bet_amount(player, default_bet, strategy_name="Flat"):
    func = BETTING_STRATEGIES.get(strategy_name, flat_betting)
    bet_amount = func(player, default_bet)
    return min(bet_amount, player.balance)