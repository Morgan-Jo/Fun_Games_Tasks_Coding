import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict

class AnalyticsVisualizer:
    """
    Translates simulation logs into statistical visualizations.
    Focuses on 'Wealth Trajectory' and 'Risk of Ruin'.
    """

    def __init__(self, style: str = "whitegrid"):
        sns.set_theme(style=style)
        self.palette = "viridis"

    def plot_wealth_trajectories(self, all_runs: List[List[Dict]], strategy_name: str):
        """
        Plots multiple simulation paths to show the variance of a strategy.
        
        Args:
            all_runs: A list of 'history' lists from the engine.
            strategy_name: The label for the plot title.
        """
        plt.figure(figsize=(12, 6))
        
        for i, run in enumerate(all_runs):
            df = pd.DataFrame(run)
            # We use alpha=0.3 to show density where paths overlap
            plt.plot(df.index, df['balance'], alpha=0.3, color='royalblue', linewidth=1)

        plt.axhline(y=all_runs[0][0]['balance'], color='red', linestyle='--', label='Starting Capital')
        plt.title(f"Monte Carlo Simulation: {strategy_name} Wealth Trajectory", fontsize=15)
        plt.xlabel("Number of Spins")
        plt.ylabel("Bankroll ($)")
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_final_distribution(self, final_balances: List[float]):
        """
        Creates a histogram/KDE of the final outcomes to show probability distribution.
        """
        plt.figure(figsize=(10, 5))
        sns.histplot(final_balances, kde=True, color="seagreen", bins=30)
        
        # Calculate Expected Value E[X]
        ev = sum(final_balances) / len(final_balances)
        plt.axvline(ev, color='orange', linestyle='-', label=f'Expected Value: ${ev:.2f}')
        
        plt.title("Distribution of Final Bankrolls", fontsize=14)
        plt.xlabel("Ending Balance ($)")
        plt.ylabel("Frequency")
        plt.legend()
        plt.show()