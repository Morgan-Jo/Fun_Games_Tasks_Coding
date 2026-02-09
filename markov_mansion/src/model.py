import numpy as np

class MarkovPredictor:
    def __init__(self, states):
        self.states = states
        self.n = len(states)
        # Initialize an empty transition matrix
        self.transition_matrix = np.zeros((self.n, self.n))

    def train(self, historical_data):
        """Builds the transition matrix from move logs."""
        for i in range(len(historical_data) - 1):
            current_state = historical_data[i]
            next_state = historical_data[i+1]
            self.transition_matrix[current_state][next_state] += 1
        
        # Normalize rows to sum to 1
        row_sums = self.transition_matrix.sum(axis=1)
        self.transition_matrix = self.transition_matrix / row_sums[:, np.newaxis]

    def predict_k_steps(self, start_state, k):
        """
        Calculates the probability distribution after k steps.
        Uses the property: v_k = v_0 * P^k
        """
        initial_dist = np.zeros(self.n)
        initial_dist[start_state] = 1
        
        # Matrix exponentiation for efficiency
        pk = np.linalg.matrix_power(self.transition_matrix, k)
        return initial_dist @ pk