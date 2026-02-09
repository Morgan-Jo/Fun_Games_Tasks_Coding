# 🎰 Monte Carlo Casino: A Study in Risk & Ruin

## 📌 Project Overview
This project is a high-fidelity **Monte Carlo Simulation framework** designed to test various gambling strategies against the mathematical reality of a casino.
Rather than a simple "game," this tool serves as a backtesting suite for probability theory. It allows users to simulate thousands of iterations of Roulette to visualize the **Law of Large Numbers, Expected Value** ($E[X]$), and **the Probability of Ruin**.

**Why this exists?**

To prove a fundamental statistical truth: The House always wins. This project demonstrates how even "winning" strategies like the Martingale fail when confronted with capital constraints and negative expectancy.

## 📊 The Mathematics of Ruin
In a European Roulette wheel, there are 37 pockets (1-36 and a single 0). For a "Red" bet, the probability of winning is $P(win) = \frac{18}{37}$.

The Expected Value ($E$) for a $1 bet on Red is calculated as:$$E[X] = \left( \frac{18}{37} \times 1 \right) + \left( \frac{19}{37} \times -1 \right) \approx -0.027$$This result (-2.7%) represents the "House Edge." No matter the betting sequence, the long-term trajectory of a player's bankroll will converge toward this negative expectancy.

## 🛠 Project Structure
```txt
monte_carlo_casino/
├── src/
│   ├── engine.py       # Core Roulette mechanics (Object-Oriented)
│   ├── strategies.py   # Strategy patterns (Martingale, Fibonacci, etc.)
│   └── visualizer.py   # Seaborn-based wealth trajectory plotting
├── data/               # (Generated) Simulation logs
├── main.py             # Experiment entry point
├── requirements.txt    # Pinned dependencies
└── README.md
```

## 🚀 Getting Started
1. Clone & Setup
```bash
git clone https://github.com/Morgan-Jo/Fun_Games_Tasks_Coding.git
cd monte-carlo-casino
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
2. Run the Experiment
```bash
python main.py
```

## 📈 Key Features
- Modular Strategy Engine: Built using Abstract Base Classes (ABC), allowing you to easily plug in new betting algorithms.

- Monte Carlo Simulations: Run 100+ concurrent "lives" to see the distribution of outcomes rather than a single anecdotal run.

- Visual Analytics: * Wealth Trajectories: Visualizes bankroll variance over time using alpha-blended line charts.

- KDE Distributions: Shows the density of final outcomes to highlight the skewness of aggressive strategies.

- Risk Metrics: Tracks Maximum Drawdown (MDD) and Ruination Rate.

## ✍️ Author
Morgan J. Tonner 

## ⚠️ Disclaimer
⚠️ Educational Purposes Only
This project is a mathematical simulation intended for educational and analytical purposes.

- **Not Financial Advice**: The strategies simulated here (e.g., Martingale, Fibonacci) are statistically proven to fail in long-term real-world scenarios due to house edges and table limits. This code is not an endorsement of gambling.
- **Risk Warning**: Gambling involves significant financial risk. The author is not responsible for any financial losses incurred by individuals applying these theoretical models to real-world scenarios.
- **No Real-Money Integration**: This software does not connect to any actual gambling platforms or financial institutions.

