"""Tutorial mode with step-by-step guidance."""

from typing import List, Dict


TUTORIAL_LESSONS = [
    {
        'title': 'Welcome to Blackjack!',
        'content': """Welcome to the Blackjack Tutorial!

In this tutorial, you'll learn:
1. Basic blackjack rules
2. How to read your hand
3. When to Hit, Stand, Double, or Split
4. Understanding the dealer's hand
5. Basic strategy fundamentals

Click "Next" to begin your first lesson."""
    },
    {
        'title': 'Understanding Your Hand',
        'content': """Your Hand Value:

• Number cards (2-10) = face value
• Face cards (J, Q, K) = 10
• Ace = 1 or 11 (whichever is better)

Goal: Get as close to 21 as possible without going over.

Examples:
• 7 + 8 = 15
• Ace + 5 = 16 (soft) or 6 (hard)
• 10 + 10 = 20
• Ace + 10 = 21 (Blackjack!)"""
    },
    {
        'title': 'Basic Actions',
        'content': """Available Actions:

HIT: Take another card
• Use when your hand is weak (under 17)
• Risk: You might bust (go over 21)

STAND: Keep your current hand
• Use when you have a strong hand (17+)
• No risk of busting

DOUBLE DOWN: Double your bet, take ONE card
• Only available on first two cards
• Use when you have a strong hand (9, 10, 11)
• Doubles your bet, but you can only take one card

SPLIT: Split a pair into two hands
• Only available when you have a pair
• Each hand gets its own bet
• Play each hand separately"""
    },
    {
        'title': 'The Dealer',
        'content': """Dealer Rules:

• Dealer must hit until reaching 17 or higher
• Dealer must stand on 17 or higher
• One card is hidden (hole card) until all players finish

Key Strategy Insight:
When dealer shows a weak card (2-6), they're likely to bust.
Stand on weaker hands (12-16) when dealer shows 2-6.

When dealer shows a strong card (7-Ace), they're likely to make 17-21.
You need a strong hand (17+) to beat them."""
    },
    {
        'title': 'Basic Strategy Basics',
        'content': """Basic Strategy Rules:

1. Always split Aces and 8s
2. Never split 10s or 5s
3. Double on 11 vs dealer 2-10
4. Double on 10 vs dealer 2-9
5. Stand on 17+ vs any dealer card
6. Hit on 12-16 vs dealer 7-Ace
7. Stand on 12-16 vs dealer 2-6

Remember: Basic strategy minimizes the house edge to about 0.5%"""
    },
    {
        'title': 'Insurance - When Dealer Shows Ace',
        'content': """Insurance Bet:

When dealer shows an Ace, you can bet on whether they have blackjack.

• Cost: Half your original bet
• Payout: 2:1 if dealer has blackjack
• Strategy: Generally NOT recommended (house edge ~7%)

Only take insurance if you're counting cards and the count is very high (+3 or more).

For basic strategy players: Always decline insurance."""
    },
    {
        'title': 'Surrender',
        'content': """Surrender Option:

Surrender allows you to give up half your bet and fold your hand.

• Available: Only on your first two cards
• Cost: Lose 50% of your bet
• When to use: When you have a very weak hand (15-16) vs dealer's strong card (9, 10, Ace)

Examples:
• 16 vs 10: Surrender (better than playing)
• 15 vs 9: Surrender
• 16 vs 7: Don't surrender (dealer might bust)

Surrender reduces house edge by about 0.08%"""
    },
    {
        'title': 'Card Counting Basics',
        'content': """Card Counting (Hi-Lo System):

Card counting tracks the ratio of high to low cards.

Running Count:
• +1 for low cards (2-6)
• 0 for neutral (7-9)
• -1 for high cards (10, J, Q, K, A)

True Count = Running Count ÷ Decks Remaining

When True Count is +2 or higher:
• Player has advantage
• Bet more (2x, 4x, 6x base bet)

When True Count is negative:
• House has advantage
• Bet minimum

Card counting can give players a 0.5-1% edge when done correctly."""
    },
    {
        'title': 'Practice Tips',
        'content': """Practice Tips:

1. Always follow basic strategy recommendations
2. Watch your RTP (Return to Player) - aim for 99%+
3. Monitor your Strategy Adherence - aim for 95%+
4. Learn from mistakes - review when you deviate
5. Practice card counting with the running/true count display
6. Use the Strategy Chart as a reference
7. Start with flat betting, then try count-based betting

Remember: Even with perfect strategy, you'll have losing sessions.
The goal is to minimize losses and maximize wins over time."""
    }
]


def get_tutorial_lesson(lesson_number: int) -> Dict:
    """Get a tutorial lesson by number."""
    if 0 <= lesson_number < len(TUTORIAL_LESSONS):
        return TUTORIAL_LESSONS[lesson_number]
    return None


def get_tutorial_hint(situation: str) -> str:
    """Get a contextual hint for the current situation."""
    hints = {
        'weak_hand': "Your hand is weak. Consider hitting to improve, but watch for bust risk.",
        'strong_hand': "You have a strong hand. Consider standing to avoid busting.",
        'dealer_weak': "Dealer shows a weak card (2-6). They're likely to bust. Consider standing on weaker hands.",
        'dealer_strong': "Dealer shows a strong card (7-Ace). You need a good hand to beat them.",
        'pair': "You have a pair! Check if splitting is recommended. Always split Aces and 8s.",
        'soft_hand': "You have a soft hand (Ace counted as 11). You can't bust on the next card!",
        'double_opportunity': "You have a good double opportunity (9, 10, or 11). Doubling doubles your bet but you only get one card."
    }
    return hints.get(situation, "Follow the basic strategy recommendation for best results.")

