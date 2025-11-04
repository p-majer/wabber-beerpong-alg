import random
import itertools
from math import comb
def simple_matchmaker(n_tables, n_teams, existing_struct=None, max_timeslots=None):
    """
    Generates a random schedule for beerpong matches.
    Each match is stored as [ (team1, team2), False ] — the bool flips to True when scored.

    n_tables: number of tables available per timeslot
    n_teams: number of teams in the tournament
    existing_struct: optional existing schedule, must follow structure described, or will crash horribly
    max_timeslots: optional upper bound for timeslots
    """
    if existing_struct is None:
        existing_struct = {}

    if max_timeslots is None:
        if existing_struct == {} or not existing_struct:
            max_timeslots = (comb(n_teams, n_tables)/4) + 100
        else:
            max_timeslots = comb(n_teams, n_tables)

    # create all unique pairs of teams
    all_matches = set(itertools.combinations(range(1, n_teams + 1), 2))
    # makes unique pairs of teams.
    # needs to be a set to enable import of old game 

    #struct = {i + 1: [] for i in range(max_timeslots)}
    struct = {}
    # if continuing an existing schedule, remove non-scored matches
    if existing_struct:
        for old_timeslot, matches in existing_struct.items():
            struct[old_timeslot] = []
            for match_entry in matches:
                if isinstance(match_entry, list) and len(match_entry) == 3:
                    match_pair, scored_flag, _ = match_entry
                    struct[old_timeslot].append(match_entry)
                    if scored_flag[0] is True:
                        all_matches.discard(tuple(sorted(match_pair)))
        timeslot = max(struct.keys()) + 1 if struct else 1 
    else:
        timeslot = 1

    all_matches = list(all_matches)
    random.shuffle(all_matches)

    while all_matches:
        available_teams = set(range(1, n_teams + 1))
        # make a set of all teams
        matches_this_slot = []
        # make a list for matches in this slot

        for _ in range(n_tables):
            for pair in list(all_matches):
                a, b = pair
                if a in available_teams and b in available_teams:
                    matches_this_slot.append([(a, b), [False], {0: 0, 1: 0}])
                    available_teams.remove(a)
                    available_teams.remove(b)
                    all_matches.remove(pair)
                    break
            else:
                break

        if matches_this_slot:
            struct[timeslot] = matches_this_slot
        timeslot += 1

    struct = {k: v for k, v in struct.items() if v}
    # remove empty timeslots
    return struct

def matchmaker(iterations, n_tables, n_teams, existing_struct=None, max_timeslots=1000):
    """Run the simple_matchmaker multiple times and pick the schedule with the fewest timeslots."""
    best_struct = simple_matchmaker(n_tables, n_teams, existing_struct, max_timeslots)

    for _ in range(iterations - 1):
        attempt = simple_matchmaker(n_tables, n_teams, existing_struct, max_timeslots)
        if len(attempt) < len(best_struct):
            best_struct = dict(attempt)
            
    return best_struct

# Example usage
if __name__ == "__main__":
    schedule = matchmaker(100, 4, 5)
    print(schedule)
