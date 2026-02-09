from src.engine import RouletteEngine
from src.strategies import ConstantBet, Martingale, Fibonacci
from src.visualizer import AnalyticsVisualizer
import pandas as pd

def run_simulation(strategy_class, num_runs=100, spins_per_run=100):
    """
    Executes multiple simulation loops for a given strategy.
    """
    engine = RouletteEngine(type="European", initial_capital=1000)
    all_histories = []
    final_balances = []

    print(f"--- Running {num_runs} simulations for {strategy_class.__name__} ---")

    for _ in range(num_runs):
        engine.reset()
        strategy = strategy_class(initial_bet=10)
        
        # Initial spin to kick off the strategy state
        current_bet = strategy.initial_bet
        
        for _ in range(spins_per_run):
            if engine.current_balance < current_bet:
                break # Player is "Ruined"
                
            result = engine.spin(current_bet, bet_type="color", bet_value="red")
            current_bet = strategy.update(result)
            
        all_histories.append(engine.history)
        final_balances.append(engine.current_balance)

    return all_histories, final_balances

def main():
    # Setup
    viz = AnalyticsVisualizer()
    num_sims = 50
    spins = 200
    
    # 1. Test Martingale (High Volatility)
    m_history, m_finals = run_simulation(Martingale, num_sims, spins)
    viz.plot_wealth_trajectories(m_history, "Martingale")
    
    # 2. Test Constant Bet (Control Group)
    c_history, c_finals = run_simulation(ConstantBet, num_sims, spins)
    viz.plot_wealth_trajectories(c_history, "Constant Bet")

    # Summary Statistics Comparison
    stats = {
        "Strategy": ["Martingale", "Constant Bet"],
        "Avg Final Balance": [sum(m_finals)/num_sims, sum(c_finals)/num_sims],
        "Max Final": [max(m_finals), max(c_finals)],
        "Min Final": [min(m_finals), min(c_finals)]
    }
    print("\nSimulation Summary:")
    print(pd.DataFrame(stats))

if __name__ == "__main__":
    main()