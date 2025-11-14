"""Session statistics and performance tracking."""

from typing import List, Dict
from datetime import datetime
import json


class SessionStatistics:
    """Track session-wide statistics and performance."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.rounds = []
        self.players_data = []
        
    def record_round(self, round_number: int, players_data: List[Dict], total_pl: float):
        """Record a round's statistics."""
        self.rounds.append({
            'round': round_number,
            'timestamp': datetime.now().isoformat(),
            'total_pl': total_pl,
            'players': players_data
        })
    
    def get_session_summary(self) -> Dict:
        """Get overall session summary."""
        if not self.rounds:
            return {}
        
        total_rounds = len(self.rounds)
        total_pl = sum(r['total_pl'] for r in self.rounds)
        avg_pl_per_round = total_pl / total_rounds if total_rounds > 0 else 0
        
        # Calculate win/loss streaks
        wins = sum(1 for r in self.rounds if r['total_pl'] > 0)
        losses = sum(1 for r in self.rounds if r['total_pl'] < 0)
        pushes = sum(1 for r in self.rounds if r['total_pl'] == 0)
        
        return {
            'total_rounds': total_rounds,
            'total_pl': total_pl,
            'avg_pl_per_round': avg_pl_per_round,
            'wins': wins,
            'losses': losses,
            'pushes': pushes,
            'win_rate': (wins / total_rounds * 100) if total_rounds > 0 else 0,
            'session_duration': str(datetime.now() - self.start_time)
        }
    
    def export_to_json(self, filename: str = None) -> str:
        """Export session data to JSON file."""
        if filename is None:
            filename = f"blackjack_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            'session_start': self.start_time.isoformat(),
            'session_end': datetime.now().isoformat(),
            'summary': self.get_session_summary(),
            'rounds': self.rounds
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export session data to CSV file."""
        import csv
        
        if filename is None:
            filename = f"blackjack_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            # Header
            writer.writerow(['Round', 'Timestamp', 'Total P/L', 'Player', 'Balance', 'Win Rate', 'RTP', 'Strategy %'])
            
            # Data rows
            for round_data in self.rounds:
                for player_data in round_data.get('players', []):
                    writer.writerow([
                        round_data['round'],
                        round_data['timestamp'],
                        round_data['total_pl'],
                        player_data.get('player_index', ''),
                        player_data.get('balance', ''),
                        player_data.get('win_rate', ''),
                        player_data.get('rtp', ''),
                        player_data.get('strategy_adherence', '')
                    ])
        
        return filename

