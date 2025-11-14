"""Bankroll management and bet sizing recommendations."""

from typing import Dict, Tuple
from statistics import CardCounting


class BankrollManager:
    """Manages bankroll and provides bet sizing recommendations."""
    
    def __init__(self, initial_bankroll: float):
        self.initial_bankroll = initial_bankroll
        self.current_bankroll = initial_bankroll
        self.base_unit = initial_bankroll / 100  # 1% of bankroll as base unit
        
    def update_bankroll(self, new_balance: float):
        """Update current bankroll."""
        self.current_bankroll = new_balance
        # Recalculate base unit (but don't go below original)
        self.base_unit = max(self.initial_bankroll / 100, self.current_bankroll / 100)
    
    def get_kelly_bet(self, advantage: float, bankroll: float = None) -> float:
        """Calculate optimal bet using Kelly Criterion.
        
        Args:
            advantage: Player advantage as decimal (e.g., 0.01 = 1%)
            bankroll: Current bankroll (defaults to current_bankroll)
        
        Returns:
            Optimal bet size
        """
        if bankroll is None:
            bankroll = self.current_bankroll
        
        if advantage <= 0:
            return self.base_unit  # No advantage, bet minimum
        
        # Kelly formula: f = (bp - q) / b
        # Simplified for blackjack: f = advantage / variance
        # Using variance of ~1.26 for blackjack
        variance = 1.26
        kelly_fraction = advantage / variance
        
        # Conservative: use 1/4 Kelly to reduce risk
        conservative_fraction = kelly_fraction * 0.25
        
        return max(self.base_unit, bankroll * conservative_fraction)
    
    def get_count_based_bet(self, true_count: float, base_bet: float, 
                            card_counter: CardCounting = None) -> float:
        """Get recommended bet based on true count.
        
        Args:
            true_count: Current true count
            base_bet: Base betting unit
            card_counter: Optional card counter for advanced calculations
        
        Returns:
            Recommended bet size
        """
        if true_count <= 0:
            return base_bet  # Bet minimum when count is negative or neutral
        
        # Betting ramp based on true count
        if true_count <= 1:
            return base_bet
        elif true_count <= 2:
            return base_bet * 2
        elif true_count <= 3:
            return base_bet * 4
        elif true_count <= 4:
            return base_bet * 6
        elif true_count <= 5:
            return base_bet * 8
        else:
            return base_bet * 10  # Max bet at TC +5 or higher
    
    def get_bankroll_percentage_bet(self, percentage: float = 1.0) -> float:
        """Get bet as percentage of bankroll.
        
        Args:
            percentage: Percentage of bankroll to bet (default 1%)
        
        Returns:
            Bet amount
        """
        return max(self.base_unit, self.current_bankroll * (percentage / 100))
    
    def calculate_risk_of_ruin(self, bet_size: float, win_rate: float = 0.48, 
                              rtp: float = 0.995) -> float:
        """Calculate risk of ruin (probability of losing entire bankroll).
        
        Simplified calculation.
        
        Args:
            bet_size: Size of each bet
            win_rate: Win rate (default 48% for basic strategy)
            rtp: Return to player (default 99.5%)
        
        Returns:
            Risk of ruin as percentage
        """
        if bet_size >= self.current_bankroll:
            return 100.0  # Betting entire bankroll = 100% risk
        
        # Simplified risk of ruin calculation
        # ROR ≈ ((1 - advantage) / (1 + advantage)) ^ (bankroll / bet_size)
        advantage = (rtp - 100) / 100  # Convert to decimal
        
        if advantage >= 0:
            return 0.0  # Positive expectation = no risk of ruin
        
        try:
            ratio = (1 - abs(advantage)) / (1 + abs(advantage))
            exponent = self.current_bankroll / bet_size
            ror = (ratio ** exponent) * 100
            return min(100.0, max(0.0, ror))
        except:
            return 50.0  # Default if calculation fails
    
    def get_bet_recommendation(self, true_count: float, base_bet: float,
                               card_counter: CardCounting = None) -> Dict[str, any]:
        """Get comprehensive bet recommendation.
        
        Returns:
            Dict with bet recommendations and analysis
        """
        count_bet = self.get_count_based_bet(true_count, base_bet, card_counter)
        
        # Calculate advantage from true count
        # Rough estimate: +1 TC ≈ +0.5% advantage
        advantage = true_count * 0.005
        kelly_bet = self.get_kelly_bet(advantage)
        
        # Recommended bet is minimum of count-based and Kelly
        recommended_bet = min(count_bet, kelly_bet)
        
        # Ensure bet doesn't exceed bankroll
        recommended_bet = min(recommended_bet, self.current_bankroll)
        
        # Calculate risk metrics
        risk_of_ruin = self.calculate_risk_of_ruin(recommended_bet)
        
        return {
            'recommended_bet': recommended_bet,
            'count_based_bet': count_bet,
            'kelly_bet': kelly_bet,
            'base_bet': base_bet,
            'true_count': true_count,
            'advantage': advantage * 100,  # As percentage
            'risk_of_ruin': risk_of_ruin,
            'bet_as_percent_of_bankroll': (recommended_bet / self.current_bankroll) * 100
        }

