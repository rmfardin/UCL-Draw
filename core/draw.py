import pandas as pd
import random

teams_df = pd.read_csv('data/teams.csv')  # load base team info
pot_to_teams = teams_df.groupby('Pot')['Team'].apply(list).to_dict()  # pot → teams list
team_info = teams_df.set_index('Team').to_dict(orient='index')  # team → {country, pot}
country_to_teams = teams_df.groupby('Country')['Team'].apply(list).to_dict()  # country → teams list
constrained_countries = {k for k, v in country_to_teams.items() if len(v) > 2}  # only countries with ≥3 teams


def initialize_draw_state(team_info, constrained_countries):
   
    matchups = {}           # team → set of opponent names
    pot_counts = {}         # team → {pot_num: count}
    country_counts = {}     # team → {country_name: count} (only for constrained countries)
    slots_remaining = {}    # team → number of matches left (starts at 8)
    drawn_teams = set()     # teams fully drawn (optional use)

    for team, info in team_info.items():
        matchups[team] = set()                                # no opponents yet
        pot_counts[team] = {1: 0, 2: 0, 3: 0, 4: 0}           # 0 from all pots
        slots_remaining[team] = 8                             # 8 matches to fill

        if info['Country'] in constrained_countries:
            country_counts[team] = {}                         # only if needed

    return matchups, pot_counts, country_counts, slots_remaining, drawn_teams



# Candidate Filtering Function

def get_valid_candidates(
    team: str,
    pot: int,
    team_info: dict,
    matchups: dict,
    pot_counts: dict,
    country_counts: dict,
    slots_remaining: dict,
    constrained_countries: set,
    pot_to_teams: dict
) -> list[tuple[str, int]]:
    """
    Return valid opponents from pot for team, with weight 0 (deadlock risk) or 1 (safe).
    """
    candidates = []
    team_country = team_info[team]['Country']
    team_pot = team_info[team]['Pot']
    
    # Helper: basic immediate constraints
    def basic_ok(t, opp, opp_pot):
        # no self-match or duplicate
        if opp == t or opp in matchups[t]:
            return False
        # both teams need open slots
        if slots_remaining.get(opp, 0) < 1 or slots_remaining.get(t, 0) < 1:
            return False
        # pot quotas: max 2 per pot
        if pot_counts[t].get(opp_pot, 0) >= 2 or pot_counts[opp].get(team_pot, 0) >= 2:
            return False
        # no same-country
        opp_country = team_info[opp]['Country']
        if opp_country == team_country:
            return False
        # max 2 opponents per constrained country
        if (opp_country in constrained_countries 
            and country_counts[t].get(opp_country, 0) >= 2):
            return False
        if (team_country in constrained_countries 
            and country_counts.get(opp, {}).get(team_country, 0) >= 2):
            return False
        return True

    # Forward-check to avoid deadlocks
    def forward_check():
        for t in team_info:
            need = slots_remaining.get(t, 0)
            if need < 1:
                continue
            total_avail = 0
            for p2, teams in pot_to_teams.items():
                for cand in teams:
                    # basic immediate checks for t -> cand
                    if not basic_ok(t, cand, team_info[cand]['Pot']):
                        continue
                    total_avail += 1
            if total_avail < need:
                return False
        return True

    # Evaluate each potential opponent
    for opp in pot_to_teams.get(pot, []):
        opp_pot = team_info[opp]['Pot']
        if not basic_ok(team, opp, opp_pot):
            continue

        # simulate assignment
        matchups[team].add(opp)
        matchups[opp].add(team)
        slots_remaining[team] -= 1
        slots_remaining[opp] -= 1
        pot_counts[team][opp_pot] += 1
        pot_counts[opp][team_pot] += 1
        # update country counts if needed
        opp_country = team_info[opp]['Country']
        if opp_country in constrained_countries:
            country_counts[team][opp_country] = country_counts[team].get(opp_country, 0) + 1
        if team_country in constrained_countries:
            country_counts.setdefault(opp, {})
            country_counts[opp][team_country] = country_counts[opp].get(team_country, 0) + 1

        # check for deadlock
        safe = forward_check()

        # rollback simulation
        matchups[team].remove(opp)
        matchups[opp].remove(team)
        slots_remaining[team] += 1
        slots_remaining[opp] += 1
        pot_counts[team][opp_pot] -= 1
        pot_counts[opp][team_pot] -= 1
        if opp_country in constrained_countries:
            country_counts[team][opp_country] -= 1
        if team_country in constrained_countries:
            country_counts[opp][team_country] -= 1

        # assign weight
        weight = 1 if safe else 0
        candidates.append((opp, weight))

    return candidates

def draw_from_pot(
    team: str,
    pot: int,
    team_info: dict,
    matchups: dict,
    pot_counts: dict,
    country_counts: dict,
    slots_remaining: dict,
    constrained_countries: set,
    pot_to_teams: dict,
    get_valid_candidates_func
) -> list[str] or bool:
    """
    Draw exactly two opponents for team from pot.
    Returns list of chosen opponents if successful, else False.
    """
    # 1. Fetch candidates with weights
    candidates = get_valid_candidates_func(
        team, pot, team_info, matchups,
        pot_counts, country_counts, slots_remaining,
        constrained_countries, pot_to_teams
    )
    # 2. Filter out deadlock-risk candidates (weight=0)
    safe = [opp for opp, w in candidates if w == 1]
    # fail-fast if not enough safe candidates
    if len(safe) < 2:
        return False

    # 3. Randomly pick 2 opponents
    chosen = random.sample(safe, 2)

    # 4. Commit each draw bidirectionally
    team_country = team_info[team]['Country']
    team_pot = team_info[team]['Pot']
    for opp in chosen:
        opp_pot = team_info[opp]['Pot']
        # register match
        matchups[team].add(opp)                # add opp to team's set
        matchups[opp].add(team)                # reciprocate
        # update slots
        slots_remaining[team] -= 1
        slots_remaining[opp] -= 1
        # update pot counts
        pot_counts[team][opp_pot] += 1
        pot_counts[opp][team_pot] += 1
        # update country counts if constrained
        opp_country = team_info[opp]['Country']
        if opp_country in constrained_countries:
            country_counts[team][opp_country] = country_counts[team].get(opp_country, 0) + 1
        if team_country in constrained_countries:
            country_counts.setdefault(opp, {})
            country_counts[opp][team_country] = country_counts[opp].get(team_country, 0) + 1

    # 5. Return chosen opponents
    return chosen

def assign_opponents(
    team: str,
    team_info: dict,
    matchups: dict,
    pot_counts: dict,
    country_counts: dict,
    slots_remaining: dict,
    constrained_countries: set,
    pot_to_teams: dict,
    get_valid_candidates_func
) -> list[str] or bool:
    """
    Assign 8 opponents to `team`: 2 from each pot (1-4). Rolls back on failure.
    Returns list of opponents if successful, else False.
    """
    deltas = []      # actions to undo on failure
    opponents = []   # list of assigned opponents
    team_country = team_info[team]['Country']
    team_pot = team_info[team]['Pot']
    
    # Helper to record and perform a state change with rollback info
    def record(action, undo):
        deltas.append(undo)
        action()
    
    try:
        # Loop pots 1 through 4
        for pot in [1, 2, 3, 4]:
            # Determine how many needed from this pot
            needed = 2 - pot_counts[team][pot]
            for _ in range(needed):
                # Get safe candidates
                candidates = get_valid_candidates_func(
                    team, pot, team_info, matchups,
                    pot_counts, country_counts, slots_remaining,
                    constrained_countries, pot_to_teams
                )
                safe = [opp for opp, w in candidates if w == 1]
                if not safe:
                    raise ValueError("No safe candidates")
                
                # Choose one opponent
                opp = random.choice(safe)
                opp_pot = team_info[opp]['Pot']
                opp_country = team_info[opp]['Country']
                
                # Commit bidirectional matchup
                record(lambda: matchups[team].add(opp),
                       lambda: matchups[team].remove(opp))
                record(lambda: matchups[opp].add(team),
                       lambda: matchups[opp].remove(team))
                
                # Commit slots_remaining updates
                old_t = slots_remaining[team]
                old_o = slots_remaining[opp]
                record(lambda: slots_remaining.__setitem__(team, old_t - 1),
                       lambda: slots_remaining.__setitem__(team, old_t))
                record(lambda: slots_remaining.__setitem__(opp, old_o - 1),
                       lambda: slots_remaining.__setitem__(opp, old_o))
                
                # Commit pot_counts updates
                old_tc = pot_counts[team][opp_pot]
                old_oc = pot_counts[opp][team_pot]
                record(lambda: pot_counts[team].__setitem__(opp_pot, old_tc + 1),
                       lambda: pot_counts[team].__setitem__(opp_pot, old_tc))
                record(lambda: pot_counts[opp].__setitem__(team_pot, old_oc + 1),
                       lambda: pot_counts[opp].__setitem__(team_pot, old_oc))
                
                # Commit country_counts if constrained
                if opp_country in constrained_countries:
                    old_cc = country_counts[team].get(opp_country, 0)
                    record(lambda: country_counts[team].__setitem__(opp_country, old_cc + 1),
                           lambda: country_counts[team].__setitem__(opp_country, old_cc))
                if team_country in constrained_countries:
                    old_ocn = country_counts.get(opp, {}).get(team_country, 0)
                    if opp not in country_counts:
                        record(lambda: country_counts.__setitem__(opp, {team_country: 1}),
                               lambda: country_counts.pop(opp, None))
                    else:
                        record(lambda: country_counts[opp].__setitem__(team_country, old_ocn + 1),
                               lambda: country_counts[opp].__setitem__(team_country, old_ocn))
                
                opponents.append(opp)
        
        # Final forward-check: ensure no remaining deadlocks
        for t in team_info:
            need = slots_remaining.get(t, 0)
            if need < 1:
                continue
            # count valid options quickly
            total = sum(1 for pot in [1,2,3,4]
                        for opp in pot_to_teams[pot]
                        if (opp not in matchups[t]
                            and slots_remaining.get(opp, 0) > 0
                            and team_info[opp]['Country'] != team_info[t]['Country']))
            if total < need:
                raise ValueError("Deadlock detected after full draw")

        return opponents

    except Exception:
        # rollback on any failure
        for undo in reversed(deltas):
            undo()
        return False