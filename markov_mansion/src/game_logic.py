import random
import networkx as nx
from typing import List, Tuple

class Mansion:
    def __init__(self):
        # Define the rooms and their physical connections
        self.adj_list = {
            'Foyer': ['Hallway', 'Library'],
            'Library': ['Foyer', 'Study', 'Conservatory'],
            'Study': ['Library', 'Secret Room'],
            'Secret Room': ['Study', 'Cellar'],
            'Cellar': ['Secret Room', 'Kitchen'],
            'Kitchen': ['Cellar', 'Dining Room'],
            'Dining Room': ['Kitchen', 'Hallway'],
            'Hallway': ['Dining Room', 'Foyer', 'Conservatory'],
            'Conservatory': ['Hallway', 'Library']
        }
        self.rooms = list(self.adj_list.keys())
        self.room_to_idx = {room: i for i, room in enumerate(self.rooms)}
        self.idx_to_room = {i: room for i, room in enumerate(self.rooms)}

    def get_neighbors(self, room: str) -> List[str]:
        return self.adj_list.get(room, [])

class Ghost:
    def __init__(self, mansion: Mansion, start_room: str = "Foyer"):
        self.mansion = mansion
        self.current_room = start_room

    def move(self):
        """
        Moves the ghost to a random adjacent room.
        In a real Markov scenario, these probabilities wouldn't be uniform.
        """
        neighbors = self.mansion.get_neighbors(self.current_room)
        self.current_room = random.choice(neighbors)
        return self.current_room