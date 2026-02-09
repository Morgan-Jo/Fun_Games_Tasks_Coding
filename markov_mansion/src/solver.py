import numpy as np
from src.model import MarkovPredictor
from src.game_logic import Mansion

class DetectiveSolver:
    def __init__(self, mansion: Mansion, model: MarkovPredictor):
        self.mansion = mansion
        self.model = model

    def calculate_entropy(self, probabilities: np.ndarray) -> float:
        """
        Calculates Shannon Entropy to measure prediction uncertainty.
        H(x) = -sum(p * log2(p))
        """
        # Filter out zero probabilities to avoid log(0)
        p = probabilities[probabilities > 0]
        return -np.sum(p * np.log2(p))

    def recommend_traps(self, current_room: str, k_steps: int, top_n: int = 3):
        """
        Predicts where the ghost will be in k steps and returns top candidates.
        """
        start_idx = self.mansion.room_to_idx[current_room]
        
        # Calculate the probability vector for k steps ahead
        probs = self.model.predict_k_steps(start_idx, k_steps)
        entropy = self.calculate_entropy(probs)
        
        # Sort rooms by probability
        ranked_indices = np.argsort(probs)[::-1]
        
        recommendations = []
        for i in range(top_n):
            idx = ranked_indices[i]
            recommendations.append({
                "room": self.mansion.idx_to_room[idx],
                "probability": round(probs[idx] * 100, 2)
            })
            
        return recommendations, entropy