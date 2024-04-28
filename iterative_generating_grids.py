from itertools import combinations
from random import sample
import pandas as pd
import sys



def generate_subsets(grid, n, limit):
    """
    Generate subsets of a given grid by removing 'n' non-zero elements, limiting the number of generated subsets.

    Parameters
    ----------
    grid : str
        A string representation of the Sudoku grid where each character represents a cell.
    n : int
        The number of non-zero elements to remove from the grid.
    limit : int
        The maximum number of subsets to generate if the number of possible combinations is too high.

    Returns
    -------
    list
        A list of strings, each representing a new grid configuration with 'n' elements removed.
    """
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
    """
    Generate subgrids by removing a specified number of non-zero elements from each grid and write them to a file.

    Parameters
    ----------
    grids : iterable
        An iterable of Sudoku grid strings to process.
    outfile : str
        The file path where the generated subgrids will be written.
    deepness : int
        The number of non-zero elements to remove from each grid.
    no_subgrids : int
        The limit on the number of subgrids to generate per original grid.

    """
    with open(outfile, 'a') as f:
        for g in grids:
            subsets = generate_subsets(g, deepness, no_subgrids)
            for s in subsets:
                f.write(f"{s}\n")

def main():
    """
    Main function to process Sudoku grids from a CSV file, generate subgrids, and save them to a specified output file.
    """
    filepath = "csvs/analysis_random_v3.csv"
    df = pd.read_csv(filepath, sep=";")
    df['is_valid'] = df['number_of_steps_to_solve'] != -1
    grids = df[df["is_valid"]].sort_values('number_of_initial_values')[:10]['sudoku']
    generate_subgrids(grids, sys.argv[1], 5, 50000)


if __name__ == "__main__":
    main()