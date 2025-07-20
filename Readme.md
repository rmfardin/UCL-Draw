# UEFA Champions League Draw Simulator (2025/26 – Swiss Format)

## Project Overview

This project simulates the official UEFA Champions League draw for the 2025/26 season, reflecting the new Swiss league format that replaces the traditional group stage. Built using Python and Streamlit, the simulator executes a realistic draw procedure according to UEFA’s updated tournament rules.

As a football enthusiast with a background in Computer Science, this project brings together a passion for sport and programming — offering an interactive tool to understand, visualize, and experiment with the new draw structure.

## Background: Format Change Explained

### Old Format (pre–2024/25)

- 32 teams
- Divided into 8 groups of 4
- Round-robin matches (home and away) within each group
- Top 2 teams from each group advanced to the Round of 16

### New Format (from 2024/25 onwards)

- 36 teams in a single league table
- Each team plays 8 unique matches against 8 different opponents:
  - 4 home matches
  - 4 away matches
- Draw opponents come from different seeding pots
- No rematches, and no teams from the same country face each other in the league phase

This Swiss-style format is inspired by systems used in chess and esports tournaments to create a more balanced and competitive progression into the knockout stages.

## Draw Rules Modeled in This Simulator

This simulator implements the draw logic with the following UEFA constraints:

- 36 qualified teams are seeded into 4 pots of 9 teams each, based on UEFA club coefficients
- Each team is drawn to play:
  - 2 teams from each of the 3 other pots
  - A total of 8 unique opponents
- Teams cannot play another team from the same pot
- Teams cannot play clubs from their own country
- Home/Away balance: Each team has 4 home and 4 away matches

## Project Structure


## How to Run the Simulator Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ucl-draw-simulator.git
   cd ucl-draw-simulator
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
3. Run the Streamlit app:
    ```bash
    streamlit run app.py
4. Interact with the simulator:  
    a. Press the "Simulate Draw" button.  
    b. View draw results: Each team’s 8 opponents will be displayed.  
    c. Optionally export the results as CSV or JSON.


## Features Implemented
1. Randomized draw simulation adhering to UEFA rules.
2. Dynamic team matching across pots.
3. Nationality and duplication conflict checks.
4. Visual interface to view results instantly.
5. Clean layout with optional enhancements (color-coding, filters).