"""Help text and explanations for blackjack simulator metrics."""

RTP_EXPLANATION = """Return to Player (RTP) Percentage

RTP shows what percentage of your total bets you've won back.

• 100% = Break even (won back exactly what you bet)
• >100% = Profitable session (won more than you bet)
• <100% = Losing session (won less than you bet)

Example: If you bet $1000 total and won $950 back, RTP = 95%
This means you lost 5% of your total bets.

With perfect basic strategy, RTP should be around 99.5% over many hands.
House edge is typically 0.5% with optimal play."""

STRATEGY_ADHERENCE_EXPLANATION = """Strategy Adherence Percentage

This shows how often you follow the mathematically optimal basic strategy.

• 100% = Perfect play (always follow recommendations)
• 95-99% = Excellent (rare mistakes)
• 80-94% = Good (some mistakes)
• <80% = Needs improvement (frequent mistakes)

Color coding:
• Green (95%+) = Excellent strategy play
• Yellow (80-94%) = Good, but room for improvement
• Red (<80%) = Too many mistakes - study basic strategy

Even small deviations from optimal strategy can significantly
reduce your RTP and increase the house edge."""

CARD_COUNTING_EXPLANATION = """Card Counting (Hi-Lo System)

Card counting tracks the ratio of high to low cards remaining in the deck.

Running Count (RC):
• Starts at 0 when deck is shuffled
• +1 for low cards (2-6)
• 0 for neutral cards (7-9)
• -1 for high cards (10, J, Q, K, A)
• Positive = More low cards seen (good for player)
• Negative = More high cards seen (bad for player)

True Count (TC):
• Running Count ÷ Decks Remaining
• More accurate than running count
• Accounts for how many cards are left
• TC +2 or higher = Favorable situation
• TC -2 or lower = Unfavorable situation

Status:
• Favorable (TC ≥ +2) = Player advantage, bet more
• Slightly Favorable (TC ≥ +1) = Small player edge
• Neutral (TC -1 to +1) = Even game
• Slightly Unfavorable (TC ≤ -1) = Small house edge
• Unfavorable (TC ≤ -2) = Strong house edge, bet minimum

Card counting can give players a 0.5-1% edge when done correctly."""

WIN_RATE_EXPLANATION = """Win Rate Percentage

Shows the percentage of non-push hands that you've won.

Formula: Wins ÷ (Wins + Losses) × 100

• 50% = Break even (winning as many as you lose)
• >50% = Winning more hands than losing
• <50% = Losing more hands than winning

Note: Win rate doesn't account for bet sizes or blackjack payouts.
A 50% win rate with perfect strategy can still be profitable due to
3:2 blackjack payouts and double downs."""

