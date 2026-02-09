import random
from typing import Dict, List, Union

class RouletteEngine:
    """
    A robust simulation engine for European and American Roulette.
    Designed to provide data streams for Monte Carlo analysis.
    """

    def __init__(self, type: str = "European", initial_capital: float = 1000.0):
        self.type = type
        self.initial_capital = initial_capital
        self.current_balance = initial_capital
        
        # Setup wheel mechanics
        # European: 0 (Green), 1-36 (Red/Black)
        # American: 0, 00 (Green), 1-36 (Red/Black)
        self.pockets = list(range(37))
        if type.lower() == "american":
            self.pockets.append("00")
            
        self.history: List[Dict[str, Union[int, str, float]]] = []

    def _get_color(self, pocket: Union[int, str]) -> str:
        """Determines the color of the pocket based on standard roulette layouts."""
        if pocket in [0, "00"]:
            return "green"
        
        # Standard Red/Black distribution
        red_pockets = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        return "red" if pocket in red_pockets else "black"

    def spin(self, bet_amount: float, bet_type: str, bet_value: Union[int, str]) -> Dict:
        """
        Executes a single spin and resolves the bet.
        
        Args:
            bet_amount: Capital allocated to this spin.
            bet_type: 'color' (red/black) or 'straight_up' (single number).
            bet_value: The target (e.g., 'red', 17, 'black').
        """
        if bet_amount > self.current_balance:
            return {"error": "Insufficient funds"}

        # Random pocket selection
        outcome = random.choice(self.pockets)
        outcome_color = self._get_color(outcome)
        
        win = False
        payout_ratio = 0

        # Logic for payouts
        if bet_type == "color" and bet_value == outcome_color:
            win = True
            payout_ratio = 1  # 1:1 payout
        elif bet_type == "straight_up" and bet_value == outcome:
            win = True
            payout_ratio = 35 # 35:1 payout

        # Update balance
        if win:
            reward = bet_amount * payout_ratio
            self.current_balance += reward
        else:
            self.current_balance -= bet_amount

        # Record state for the Data Analyst's future analysis
        record = {
            "pocket": outcome,
            "color": outcome_color,
            "bet_amount": bet_amount,
            "result": "win" if win else "loss",
            "balance": self.current_balance
        }
        self.history.append(record)
        return record

    def reset(self):
        """Reset the engine for a new simulation run."""
        self.current_balance = self.initial_capital
        self.history = []