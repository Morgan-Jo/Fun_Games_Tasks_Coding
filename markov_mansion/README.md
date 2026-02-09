# 🕵️‍♂️ Markov’s Mansion: Stochastic Hide & Seek

## 📌 Project Overview

**Markov's Mansion** is a predictive modeling game where you play a detective tracking an invisible "Ghost" through a 10-room mansion. You cannot see the ghost, but you have access to historical movement logs.

Your goal is to build a **Transition Matrix** from the logs and use **Matrix Exponentiation** to predict the most likely room the ghost will occupy in $k$ steps.

**The "Analyst" Challenge**

Instead of guessing, you are applying the **Markov Property**: the future state depends only on the current state and not on the sequence of events that preceded it.

## 📂 Project Structure
```txt
markov_mansion/
├── data/
│   └── historical_movements.json  # 10,000+ simulated room transitions
├── src/
│   ├── model.py                  # Matrix math & Transition logic
│   ├── mansion.py                # Mansion graph & state management
│   └── engine.py                 # Game loop & probability calculator
├── main.py                       # Entry point
├── requirements.txt
└── README.md
```

## 🧪 The Mathematics

The core of this game is the **Transition Probability Matrix** $P$. If the mansion has $N$ rooms, $P$ is an $N \times N$ matrix where each entry $P_{ij}$ represents the probability of moving from room $i$ to room $j$.

To find the probability distribution after $n$ moves, we use the initial state vector $v_0$ and the $n$-th power of the transition matrix:

$$v_n = v_0 \cdot P^n$$

In this game, you will calculate $v_n$ to place your "traps" in the rooms with the highest probability density.

## 🛠 Features

- **Automated Transition Learning**: The system parses `.json` logs to populate the matrix using Maximum Likelihood Estimation (MLE).
- **Matrix Exponentiation**: Uses `numpy.linalg.matrix_power` for efficient long-range predictions.
- **Entropy Tracking**: Measures the "uncertainty" of the ghost's location over time—as $n$ increases, the distribution typically moves toward a **Steady State**.

## 🚀 Installation & Usage

1. Clone the repository:

```bash
git clone https://github.com/Morgan-Jo/Fun_Games_Tasks_Coding.git
cd Fun_Games_Tasks_Coding/markov-mansion
```

2. Install Dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Game:

```bash
pyhton main.py
```

## ✍️ Author

Morgan Jo Tonner

## ⚖️ Disclaimer

**⚠️ For Simulation & Educational Use Only**

- **Theoretical Model**: This project uses a first-order Markov Chain. Real-world human (or ghost) movement is often non-Markovian and influenced by external variables not captured in this model.
- **No Practical Application**: This software is a game. It is not designed for real-world surveillance, security forecasting, or tracking of physical entities.
- **Predictive Limitations**: Stochastic modeling provides probabilities, not certainties. The "Ghost" may still appear in a low-probability room due to the inherent randomness ($p > 0$) of the system.