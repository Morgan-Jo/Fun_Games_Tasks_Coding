from abc import ABC, abstractmethod
from typing import Dict, Optional

class BettingStrategy(ABC):
    """Abstract base class for all betting strategies."""
    
    def __init__(self, initial_bet: float):
        self.initial_bet = initial_bet
        self.current_bet = initial_bet

    @abstractmethod
    def update(self, last_result: Dict) -> float:
        """
        Updates the internal state based on the last spin 
        and returns the next bet amount.
        """
        pass

class ConstantBet(BettingStrategy):
    """The 'Control Group' strategy: Always bet the same amount."""
    
    def update(self, last_result: Dict) -> float:
        return self.initial_bet

class Martingale(BettingStrategy):
    """
    The 'Double or Nothing' strategy. 
    Doubles the bet after every loss to recoup all previous losses.
    """
    
    def update(self, last_result: Dict) -> float:
        if last_result['result'] == 'win':
            self.current_bet = self.initial_bet
        else:
            self.current_bet *= 2
        return self.current_bet

class Fibonacci(BettingStrategy):
    """
    A more conservative progression using the Fibonacci sequence.
    Increases bet by moving up the sequence on loss, moves down on win.
    """
    
    def __init__(self, initial_bet: float):
        super().__init__(initial_bet)
        self.sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        self.ptr = 0

    def update(self, last_result: Dict) -> float:
        if last_result['result'] == 'win':
            self.ptr = max(0, self.ptr - 2)
        else:
            self.ptr = min(len(self.sequence) - 1, self.ptr + 1)
        
        self.current_bet = self.initial_bet * self.sequence[self.ptr]
        return self.current_bet