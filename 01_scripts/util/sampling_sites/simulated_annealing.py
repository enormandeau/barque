#!/usr/bin/env python3
"""In species table from Barque, identify best n sites to maximize diversity

This script is used to assist in finding better sampling plans in lakes.

WARNING! Treat species table to keep only species of interest:
    - Remove non-fish species if you are interested only in fish
    - Resolve multiple hits (merge with existing species if needed)
    - Filter to remove potential false positives

NOTE: Need to find a good way to assess diversity
    - RECOMMENDED: Presence/absence (with possible filters, eg: min reads, min samples)
    - Shannon index? (May maximize shannon while loosing more species) (may create biases)
    - Presence but favor species with more reads (sqrt(reads)) (may create biases)

Usage:
    <program> input_table num_sites
"""
# Modules
from collections import Counter
from random import random, sample
from math import sqrt, exp
import sys

# Functions
def compute_score_num_species(solution, min_reads=10):
    """Return number of counted species from SA solution

    Recommended score function.
    """
    species = [list(x)[:] for x in list(zip(*solution))][1: ]
    score = 0.0
    for s in species:
        score += 1 if len([x for x in s if x >= min_reads]) else 0

    return score

def compute_score_weighted(solution):
    """Return sqrt number of reads per site per species

    WARNING: Not recommended. Maximizing this score is detrimental to rare
    species (less reads or present in fewer samples).
    """
    species = [list(x)[:] for x in list(zip(*solution))][1: ]

    score = 0.0
    for s in species:
        score += sum([sqrt(x) for x in s])

    return score

# Parse user input
try:
    input_table = sys.argv[1]
    num_sites = int(sys.argv[2])
except:
    print(__doc__)
    sys.exit(1)

# Read table count
with open(input_table) as infile:
    lines = [line.strip().split(",") for line in infile]

    if not lines[0][3] == "Total":
        print("Wrong format. The 4 first columns should be named:")
        print("'Group', 'Genus', 'Species', 'Total'")
        sys.exit(1)

    transposed = list(zip(*lines))

    header = transposed[:6]
    data = [list(x) for x in transposed[6: ]]

    for d in data:
        d[1: ] = [int(x) for x in d[1: ]]

# Intitialize Simulated Annealing

# Create initial solution
shuffled = sample(data, len(data))#num_sites)
solution = shuffled[: num_sites]
excluded = shuffled[num_sites: ]
#print("\n".join([x[0] for x in solution]))
best_solution = solution
absolute_best_solution = solution

# Score function to use
compute_score = compute_score_num_species

score = sqrt(compute_score(solution)) / 2
best_score = score
#print(compute_score(solution))

temp = score

max_iter = 100000
max_iter_without_improvement = 100000
temp_gradient = 0.999

iter_num = 1
iter_without_improvement = 0
new_samples = 1

# Run Simulated Annealing
while True:
    #if not iter_num % 1000:
    #    print(iter_num, best_score)

    # - Switch an included sample with an excluded sample
    # Shuffle both solution and excluded and pick the first `new_samples`
    # elements from each to switch between the two
    solution = sample(solution, len(solution))
    excluded = sample(excluded, len(excluded))

    from_solution = solution[: new_samples]
    from_excluded = excluded[: new_samples]

    solution = from_excluded + solution[new_samples: ]
    excluded = from_solution + excluded[new_samples: ]

    score = compute_score(solution)

    if score >= best_score:
        #print("Round:", iter_num, "temp:", round(temp, 2), "best score:", round(best_score, 2), "score:", round(score, 2), "improvement:", round(score - best_score, 2), "without improvement:", iter_without_improvement)
        best_solution = solution
        absolute_best_solution = solution
        best_score = score
        iter_without_improvement = 0

    else:
        # Use probability of accepting lower quality solution
        delta = best_score - score
        rand = random()
        if rand < exp(-delta / temp):
            #print(iter_num, round(temp, 2), round(score, 2), round(-delta, 2), round(exp(-delta / temp), 4))
            best_solution = solution

        iter_without_improvement += 1

    if iter_without_improvement > max_iter_without_improvement:
        #print("Stopping Annealing: max_iter_without_improvement")
        break

    temp *= temp_gradient

    iter_num += 1

    if iter_num > max_iter:
        #print("Stopping Annealing: maximum number of iterations reached")
        break

    #print(iter_num, temp)

print("\t".join([str(x) for x in [num_sites, round(best_score, 4)]]))
#print("\n".join(sorted([" ".join([str(i) for i in x]) for x in absolute_best_solution])))
#print(" ".join(sorted([x[0] for x in absolute_best_solution])))
