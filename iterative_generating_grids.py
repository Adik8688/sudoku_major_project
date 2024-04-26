from itertools import combinations
from random import sample
import pandas as pd
import sys



def generate_subsets(grid, n, limit):
    non_zeros = [i for i, char in enumerate(grid) if char != '0']
    
    indices_to_remove_combinations = list(combinations(non_zeros, n))
    if len(indices_to_remove_combinations) > limit:
        indices_to_remove_combinations = sample(indices_to_remove_combinations, limit)
    
    subsets = []
    for indices in indices_to_remove_combinations:
        subset_list = list(grid)
        for index in indices:
            subset_list[index] = '0'
        subsets.append("".join(subset_list))
    
    return subsets

def generate_subgrids(grids, outfile, deepness, no_subgrids):
    with open(outfile, 'a') as f:
        for g in grids:
            subsets = generate_subsets(g, deepness, no_subgrids)
            for s in subsets:
                f.write(f"{s}\n")

def main():
    filepath = "csvs/analysis_random_v3.csv"
    df = pd.read_csv(filepath, sep=";")
    df['is_valid'] = df['number_of_steps_to_solve'] != -1
    grids = df[df["is_valid"]].sort_values('number_of_initial_values')[:10]['sudoku']
    generate_subgrids(grids, sys.argv[1], 5, 50000)


if __name__ == "__main__":
    main()