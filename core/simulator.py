import pandas as pd
import random
from core.draw import (
    initialize_draw_state,
    assign_opponents,
    get_valid_candidates
)

def run_full_draw(
    teams_csv_path: str,
    max_retries: int = 10
) -> dict[str, set[str]]:
    """
    Conduct the full UEFA Swiss draw for all 36 teams, pot-by-pot.
    Retries up to `max_retries` times on failure before raising.

    Returns:
        matchups: dict mapping team_name -> set of 8 opponent names.
    """
    # load team data
    teams_df = pd.read_csv(teams_csv_path)
    # pot → [teams]
    pot_to_teams = teams_df.groupby('Pot')['Team'].apply(list).to_dict()
    # team → { 'Country': str, 'Pot': int }
    team_info = teams_df.set_index('Team').to_dict(orient='index')
    # country → [teams]
    country_to_teams = teams_df.groupby('Country')['Team'].apply(list).to_dict()
    # only countries with ≥3 teams need counting
    constrained_countries = {c for c, t in country_to_teams.items() if len(t) > 2}

    for attempt in range(1, max_retries + 1):
        # init all per-team state
        matchups, pot_counts, country_counts, slots_remaining, drawn_teams = \
            initialize_draw_state(team_info, constrained_countries)
        success = True

        # draw stage: pot 1 → pot 4
        for pot in [1, 2, 3, 4]:
            for team in pot_to_teams.get(pot, []):
                # skip if already full
                if slots_remaining[team] > 0:
                    result = assign_opponents(
                        team,
                        team_info,
                        matchups,
                        pot_counts,
                        country_counts,
                        slots_remaining,
                        constrained_countries,
                        pot_to_teams,
                        get_valid_candidates
                    )
                    if not result:
                        success = False
                        break
            if not success:
                break

        if success:
            return matchups  # done!

    # if we exhaust retries
    raise RuntimeError(f"Could not complete draw in {max_retries} attempts")

def build_draw_matrix(
    matchups: dict[str, set[str]],
    team_order: list[str] = None
) -> pd.DataFrame:
    """
    Build a 36×36 adjacency matrix DataFrame:
    - matrix.loc[team_i, team_j] == 1 if they play each other, else 0

    Args:
        matchups: dict mapping team -> set of opponents
        team_order: optional list to fix row/column order (default = sorted keys)

    Returns:
        Pandas DataFrame with int entries (0/1)
    """
    teams = team_order or sorted(matchups.keys())
    # initialize all zeros
    matrix = pd.DataFrame(0, index=teams, columns=teams, dtype=int)
    # fill in 1s
    for team, opponents in matchups.items():
        for opp in opponents:
            matrix.at[team, opp] = 1
    return matrix