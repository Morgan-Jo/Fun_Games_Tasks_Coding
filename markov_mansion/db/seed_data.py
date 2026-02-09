import json
from src.game_logic import Mansion, Ghost

def create_seed_data(filename="data/historical_movements.json"):
    mansion = Mansion()
    ghost = Ghost(mansion)
    
    # Simulate a long walk to capture the "Statistical Norm"
    walk_history = [mansion.room_to_idx[ghost.current_room]]
    for _ in range(10000):
        room = ghost.move()
        walk_history.append(mansion.room_to_idx[room])
        
    data = {
        "metadata": {"total_steps": len(walk_history)},
        "movements": walk_history
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"✅ Created {filename} with 10,000 movements.")