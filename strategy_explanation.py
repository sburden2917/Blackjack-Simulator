"""Strategy explanation system for blackjack recommendations."""

from typing import Tuple, Optional


def get_strategy_explanation(
    player_hand_value: int,
    dealer_upcard: int,
    hand_type: str,  # 'hard', 'soft', 'pair'
    recommendation: str,
    is_pair: bool = False,
    pair_value: Optional[int] = None
) -> str:
    """Get explanation for why a strategy recommendation is made."""
    
    explanations = {
        'hard': _get_hard_explanation,
        'soft': _get_soft_explanation,
        'pair': _get_pair_explanation
    }
    
    explain_func = explanations.get(hand_type, _get_hard_explanation)
    return explain_func(player_hand_value, dealer_upcard, recommendation, is_pair, pair_value)


def _get_hard_explanation(hand_value: int, dealer_upcard: int, recommendation: str, is_pair: bool, pair_value: Optional[int]) -> str:
    """Explain hard hand strategy."""
    
    if recommendation == "Stand":
        if hand_value >= 17:
            return f"Stand on {hand_value}: You have a strong hand. The dealer must hit until 17+, giving you a good chance to win."
        elif hand_value in [13, 14, 15, 16]:
            if dealer_upcard in [2, 3, 4, 5, 6]:
                return f"Stand on {hand_value} vs {dealer_upcard}: Dealer shows a weak card (2-6) and must hit. They have a high bust probability (~35-42%), so standing is optimal."
            else:
                return f"Stand on {hand_value}: Even though dealer shows {dealer_upcard}, your hand is strong enough that hitting risks busting."
        elif hand_value == 12:
            if dealer_upcard in [4, 5, 6]:
                return f"Stand on 12 vs {dealer_upcard}: Dealer shows a weak card and must hit. Standing gives you the best chance to win."
    
    elif recommendation == "Hit":
        if hand_value <= 11:
            return f"Hit on {hand_value}: Your hand is too weak. You need more cards to have a chance to beat the dealer."
        elif hand_value in [12, 13, 14, 15, 16]:
            if dealer_upcard >= 7:
                return f"Hit on {hand_value} vs {dealer_upcard}: Dealer shows a strong card (7-Ace). They're likely to make 17-21, so you must improve your hand."
        elif hand_value >= 17:
            return f"Hit on {hand_value}: This is unusual - you should typically stand on 17+."
    
    elif recommendation == "Double Down":
        if hand_value == 11:
            return f"Double on 11 vs {dealer_upcard}: You have a strong chance to get 21. Doubling maximizes your win when you're likely to improve."
        elif hand_value == 10:
            if dealer_upcard <= 9:
                return f"Double on 10 vs {dealer_upcard}: High probability of getting 20, which beats most dealer hands. Double to maximize winnings."
        elif hand_value == 9:
            if dealer_upcard in [3, 4, 5, 6]:
                return f"Double on 9 vs {dealer_upcard}: Dealer shows a weak card. You have good odds of improving to 19-20."
    
    return f"{recommendation} on {hand_value} vs {dealer_upcard}: This is the mathematically optimal play."


def _get_soft_explanation(hand_value: int, dealer_upcard: int, recommendation: str, is_pair: bool, pair_value: Optional[int]) -> str:
    """Explain soft hand strategy."""
    
    if recommendation == "Stand":
        if hand_value >= 19:
            return f"Stand on soft {hand_value}: You have a very strong hand. The ace gives you flexibility, but standing is optimal here."
        elif hand_value == 18:
            if dealer_upcard in [7, 8]:
                return f"Stand on soft 18 vs {dealer_upcard}: Dealer shows a strong card. Your soft 18 is good enough to stand."
    
    elif recommendation == "Hit":
        if hand_value <= 17:
            return f"Hit on soft {hand_value}: Your soft hand can't bust on the next card. Take advantage and improve your hand."
        elif hand_value == 18:
            if dealer_upcard >= 9:
                return f"Hit on soft 18 vs {dealer_upcard}: Dealer shows a very strong card (9-Ace). You need to improve to compete."
    
    elif recommendation == "Double Down":
        if hand_value in [13, 14, 15, 16, 17, 18]:
            if dealer_upcard in [4, 5, 6]:
                return f"Double on soft {hand_value} vs {dealer_upcard}: Dealer shows a weak card. Your soft hand can't bust, making this a great double opportunity."
        elif hand_value == 19:
            if dealer_upcard == 6:
                return f"Double on soft 19 vs 6: Dealer shows a weak card. Soft 19 is strong, and doubling maximizes your advantage."
    
    return f"{recommendation} on soft {hand_value} vs {dealer_upcard}: Optimal play for a soft hand."


def _get_pair_explanation(hand_value: int, dealer_upcard: int, recommendation: str, is_pair: bool, pair_value: Optional[int]) -> str:
    """Explain pair splitting strategy."""
    
    if pair_value is None:
        pair_value = hand_value
    
    if recommendation == "Split":
        if pair_value == 1:  # Aces
            return f"Always split Aces: Two chances at 21 (blackjack) is much better than one. This is one of the most profitable plays in blackjack."
        elif pair_value in [8, 8]:
            return f"Split 8s vs {dealer_upcard}: Two 8s make 16, a weak hand. Splitting gives you two chances to improve from a bad situation."
        elif pair_value in [2, 3, 6, 7, 9]:
            if dealer_upcard <= 6:
                return f"Split {pair_value}s vs {dealer_upcard}: Dealer shows a weak card. Splitting gives you two opportunities to beat them."
        elif pair_value == 4:
            if dealer_upcard in [5, 6]:
                return f"Split 4s vs {dealer_upcard}: Dealer shows a weak card. Two 4s (14) is weak, but splitting gives you better odds."
    
    elif recommendation == "Stand":
        if pair_value == 10:
            return f"Never split 10s: Two 10s make 20, an excellent hand. Splitting would be giving up a strong position."
        elif pair_value == 5:
            return f"Don't split 5s: Two 5s make 10, a great doubling hand. Treat it as a 10 instead of splitting."
    
    elif recommendation == "Double Down":
        if pair_value == 5:
            return f"Double on pair of 5s vs {dealer_upcard}: Treat as a 10 and double down for maximum value."
    
    return f"{recommendation} on pair of {pair_value}s vs {dealer_upcard}: Optimal pair strategy."


def get_hand_type_description(hand, dealer_upcard: int) -> Tuple[str, str]:
    """Get hand type and description."""
    if len(hand.cards) == 2 and hand.cards[0][0] == hand.cards[1][0]:
        pair_value = hand.cards[0][0]
        if pair_value > 10:
            pair_value = 10
        return "pair", f"Pair of {pair_value}s"
    
    has_ace = any(c[0] == 1 for c in hand.cards)
    if has_ace and hand.hand_value > sum(c[0] for c in hand.cards if c[0] != 1) + 1:
        return "soft", f"Soft {hand.hand_value}"
    
    return "hard", f"Hard {hand.hand_value}"

