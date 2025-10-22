# I vibecoded so hard guys - kyle
# OOP fears me - kyle 

import random
import itertools

def simple_matchmaker(n_tables, n_teams, existing_struct = {}, max_timeslots=1000):

    all_matches = set(itertools.combinations(range(1, n_teams + 1), 2))
    # makes unique pairs of teams.
    # needs to be a set to enable import of old game 

    struct = {i + 1: [] for i in range(max_timeslots)} 

    if existing_struct:
        for old_timeslot, matches in existing_struct.items():
            struct[old_timeslot] = matches[:]
            # Remove already played matches from the pool
            for match in matches:
                all_matches.discard(tuple(sorted(match)))

        # Continue numbering from the last filled timeslot
        timeslot = max(existing_struct.keys()) + 1
    else:
        timeslot = 1
    
    all_matches = list(all_matches)
    random.shuffle(all_matches)
    # makes all_matches into a list and shuffles it randomly 

    while len(all_matches) > 0:
        available_teams = set(range(1, n_teams + 1))
        # make a set of all teams
        matches_this_slot = []
        # make a list for matches in this slot

        for _ in range(n_tables):
            for i in all_matches:
                # order of all_matches needed to be randomized 
                # because this just relies on getting the next 
                # item from the list. Unsophisticated. 
                # Very simple though. 
                # Introducing iterations ensures use of 
                # least timeslots. 
                a, b = i
                # a and b are the teams in the match
                if a in available_teams and b in available_teams:
                    # if both teams are available
                    matches_this_slot.append(i)
                    # add match to list of matches in slot
                    available_teams.remove(a)
                    available_teams.remove(b)
                    # mark teams unavailable for timeslot
                    all_matches.remove(i)
                    # remove match from list of all matches
                    break
            else:
                # if I don't put this here, the whole thing freaks out.
                # too high to understand why, too drunk to care. 
                break

        if matches_this_slot:
            struct[timeslot] = matches_this_slot
            #if there is something to add, it adds it to the structure

        timeslot += 1
        #goes to next timeslot

    struct = {k: v for k, v in struct.items() if v}
    # removes empty slots hopefully
    return struct

def matchmaker(iterations, n_tables, n_teams, existing_struct = {}, max_timeslots=1000):
    best_struct = simple_matchmaker(n_tables, n_teams, existing_struct, max_timeslots)

    for _ in range(iterations-1):
        attempt = simple_matchmaker(n_tables, n_teams, existing_struct, max_timeslots)
        if len(attempt) < len(best_struct):
            best_struct = dict(attempt)
    return(best_struct)

# examples for your pleasure
# old_game = {1: [(7, 8), (5, 12), (1, 11), (3, 6)], 2: [(4, 12), (3, 10), (6, 9), (7, 11)], 3: [(2, 12), (3, 9), (1, 4), (6, 7)]}
# matchmaker(100, 4, 20, old_game)