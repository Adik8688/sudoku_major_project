from src.Sudoku import Sudoku
from src.SudokuSolver import SudokuSolver
from src.SudokuAnalyzer import SudokuAnalyzer
from copy import deepcopy
import sys
import concurrent.futures
import glob
import os
import time


def remove_digits(grids: list, desired_deepnees: int, limit, outfile, existing_subgrids):
    results = []
    found_grids = 0
    valid_grids = set()

    with open(existing_subgrids, 'r') as f:
        valid_grids = set([line.strip() for line in f])

    if os.path.exists(outfile):
        with open(outfile, 'r') as f:
            valid_grids.update([line.strip() for line in f])
    

    def recursive_removal(sudoku: Sudoku, first_solution: Sudoku, list_of_non_zeros: list, n: int = 0):
        nonlocal limit
        nonlocal results
        nonlocal found_grids
        
        if found_grids >= limit:
            return None

        if sudoku.get_hash() in valid_grids:
            return None
        
        solver = SudokuSolver(sudoku)
        if solver.solve_recursive(ignore_solution=first_solution) is not None:
            sudoku.reset_sudoku()
            return None

        valid_grids.add(sudoku.get_hash())

        if n == desired_deepnees:
            found_grids += 1
            with open(outfile, 'a') as f:
                f.write(f"{sudoku.get_hash()}\n")
            results.append(deepcopy(sudoku.grid))
            return None

        for i, coords in enumerate(list_of_non_zeros):
            tmp = sudoku.get_cell(coords[0], coords[1])
            sudoku.initial_grid[coords[1], coords[0]] = 0
            sudoku.set_cell(coords[0], coords[1], 0)

            recursive_removal(
                sudoku, first_solution, list_of_non_zeros[:i] + list_of_non_zeros[i + 1 :], n + 1
            )
                        
            sudoku.set_cell(coords[0], coords[1], tmp)
            sudoku.initial_grid[coords[1], coords[0]] = tmp
            if found_grids >= limit:
                return None
        
        return None
    

    for g in grids:
        sudoku = Sudoku(g)
     
        non_zeros = []
        for y in range(9):
            for x in range(9):
                if sudoku.grid[y][x]:
                    non_zeros.append((x, y))

        solver = SudokuSolver(sudoku)
        solution = deepcopy(solver.solve_recursive())
        sudoku.reset_sudoku()

        recursive_removal(sudoku, solution, non_zeros)

        if found_grids >= limit:
            break

    return results

def hash_to_grid(hash: str):
    grid = ""
    for i in range(0, 81, 9):
        grid += hash[i : i + 9] + "\n"

    return grid

def remove_duplicated_lines_from_file(filename):
    with open(filename, "r+") as f:
        hashes = [line.strip() for line in f]
        hashes = set(hashes)
        f.seek(0)
        for h in hashes:
            f.write(f"{h}\n")
        f.truncate()

def process_grid_part(grids, n, sub_grids_limit, part_number):
    remove_digits(grids, 1, sub_grids_limit, f"grids/subgrids/grids_{n}_{part_number}.txt", f"grids/grids_{n}.txt")
    remove_duplicated_lines_from_file(f"grids/subgrids/grids_{n}_{part_number}.txt")


def append_and_delete_subgrids(file_path):
    file_path = os.path.abspath(file_path)
    
    file_dir = os.path.dirname(file_path)
    subgrids_dir = os.path.join(file_dir, 'subgrids')
    
    if not os.path.exists(subgrids_dir) or not os.path.isdir(subgrids_dir):
        print(f"The directory '{subgrids_dir}' does not exist.")
        return

    with open(file_path, 'r') as main_file:
        existing_grids = main_file.readlines()


    with open(file_path, 'w') as main_file:
        for filename in os.listdir(subgrids_dir):
            subgrid_path = os.path.join(subgrids_dir, filename)
            if os.path.isfile(subgrid_path):
                with open(subgrid_path, 'r') as subgrid_file:
                    main_file.write(subgrid_file.read())
        main_file.writelines(existing_grids)
    
    for filename in os.listdir(subgrids_dir):
        os.remove(os.path.join(subgrids_dir, filename))
    print(f"All files in '{subgrids_dir}' have been appended to '{file_path}' and removed.")

    remove_duplicated_lines_from_file(file_path)


def main(sub_grids_limit, start_n, end_n):
    num_of_workers = 32
  
    for i in range(start_n, end_n, -1):
        with open(f"grids/grids_{i}.txt") as f:
            hashes = [line.strip() for line in f]


        grids = [hash_to_grid(h) for h in hashes]
        length = len(grids)

        print(f"{length} grids loaded from the file")

        part_size = length // num_of_workers
        sub_grids_limit /= num_of_workers

        start_time = time.time()
        futures = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_of_workers) as executor:
            for part_number in range(32):
                start_index = part_size * part_number
                end_index = start_index + part_size if part_number < 31 else length
                futures.append(executor.submit(process_grid_part, grids[start_index:end_index], i - 1, sub_grids_limit, part_number))

            completed_futures = 0
            for future in concurrent.futures.as_completed(futures):
                completed_futures += 1
                remaining_futures = len(futures) - completed_futures
                print(f"{remaining_futures} tasks remaining")

        end_time = time.time()
        print(f"Execution time: {round(end_time - start_time, 2)}")

        append_and_delete_subgrids(f"grids/grids_{i - 1}.txt")
        


if __name__ == "__main__":
    if len(sys.argv) > 2:
        sub_grids_limit = int(sys.argv[1])
        start_n = int(sys.argv[2])
        if len(sys.argv) > 3:
            end_n = int(sys.argv[3])
        else:
            end_n = start_n - 1

        main(sub_grids_limit, start_n, end_n)
    
    elif sys.argv[1] == 'help':
        print("Usage: ")
        print(f"{sys.argv[0]} <sub_grids_limit> <start_n> <end_n>")
        print(f"{sys.argv[0]} <name_of_file_with_grids>")

    else:
        append_and_delete_subgrids(sys.argv[1])

        