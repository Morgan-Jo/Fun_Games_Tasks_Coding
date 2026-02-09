import numpy as np
import json
from src.game_logic import Mansion, Ghost
from src.model import MarkovPredictor
from src.solver import DetectiveSolver
from db.seed_data import create_seed_data
import os

def generate_historical_data(mansion, ghost, n_entries=5000):
    """
    Simulates the ghost moving through the mansion for a long period
    to generate training data for our Markov model.
    """
    print(f"📡 Generating {n_entries} historical movement logs...")
    history = []
    for _ in range(n_entries):
        room = ghost.move()
        history.append(mansion.room_to_idx[room])
    return history

def main():
    # 1. Initialization
    mansion = Mansion()
    training_ghost = Ghost(mansion)
    model = MarkovPredictor(mansion.rooms)
    
    # 2. Training Phase (Data Collection)
    history = generate_historical_data(mansion, training_ghost)
    model.train(history)
    print("✅ Model trained. Transition Matrix stabilized.")

    # 3. Game Phase (Live Tracking)
    live_ghost = Ghost(mansion, start_room="Foyer")
    solver = DetectiveSolver(mansion, model)
    
    print("\n" + "="*50)
    print("🕵️‍♂️ WELCOME TO MARKOV'S MANSION: THE LIVE HUNT")
    print("="*50)

    # Simulate 5 rounds of the game
    for turn in range(1, 6):
        current_loc = live_ghost.current_room
        print(f"\n[Turn {turn}] Ghost last spotted in: **{current_loc}**")
        
        # Predict 2 steps ahead
        k = 2
        recommendations, entropy = solver.recommend_traps(current_loc, k_steps=k)
        
        print(f"📊 Analysis: Entropy (Uncertainty) = {entropy:.2f}")
        print(f"🔮 Prediction for {k} steps ahead:")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec['room']}: {rec['probability']}%")
        
        # Move the ghost for the next turn
        live_ghost.move()

    print("\n" + "="*50)
    print("Hunt complete. Check the logs for model drift analysis.")

    if not os.path.exists('data/historical_movements.json'):
        create_seed_data() # Generate if missing
    
    with open('data/historical_movements.json', 'r') as f:
        history = json.load(f)['movements']
        model.train(history)

if __name__ == "__main__":
    main()