import sys
import os.path
from src.Sudoku import Sudoku
from src.SudokuScrambler import SudokuScrambler
from src.SudokuAnalyzer import SudokuAnalyzer
from src.SudokuSolver import SudokuSolver
import concurrent.futures
import time


SEED = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]

def run_experiment(batch_size, batch_number, number_of_initial_values):
    results = []
    debug_file = f"logs/batch_{batch_number}.txt"
    with open(debug_file, "a") as f:
        f.write("")
        
    for _ in range(batch_size):
        sudoku = Sudoku(SEED)
        scrambler = SudokuScrambler(sudoku, number_of_initial_values)
        scrambler.scramble()
        analyzer = SudokuAnalyzer(sudoku)
        sudoku_properties = analyzer.get_sudoku_description()

        number_of_steps = -1
        solver = SudokuSolver(sudoku, debug_file)
        solved_sudoku = solver.solve()
        if solved_sudoku is not None:
            number_of_steps = solver.number_of_steps

        
        
        with open(debug_file, "a") as f:
            f.write(f"{sudoku_properties[0]};{sudoku_properties[1]};{sudoku_properties[2]};{number_of_steps}\n\n\n")

        results.append(f"{sudoku.get_hash()};{sudoku_properties[0]};{sudoku_properties[1]};{sudoku_properties[2]};{number_of_steps}\n")
    
    print(f"Batch {batch_number} finished.")
    return results

def write_output(results, output_path):
    if not os.path.isfile(output_path):
        results = ["sudoku;sum_of_candidates;number_of_initial_values;initial_numbers_entropy;numbers_of_steps_to_solve\n"] + results
        
    with open(output_path, 'a') as f:
        for r in results:
            if r:
                f.write(r)

def check_arguments(args):
    if len(args) != 3 and len(args) != 4:
        print(f"Invalid number of arguments! {args[0]} takes 2 or 3 arguments.")
        exit(-1)

    if not args[1].isnumeric():
        print(f"{args[1]} is invalid. 1 argument must be int")
        exit(-1)
    
    if not isinstance(args[2], str):
        print(f"{args[2]} is invalid. 2 argument must be str")
        exit(-1)


def print_time(time_in, message=""):
    local_time = time.localtime(time_in)
    print(f"{message}{local_time.tm_hour:02}:{local_time.tm_min:02}:{local_time.tm_sec:02}")

def print_duration(time_in_seconds, message=""):
    hours: int = time_in_seconds // 3600
    time_in_seconds = time_in_seconds % 3600
    minutes = time_in_seconds // 60
    seconds = time_in_seconds % 60
   
    print(f"{message}{hours:0.0f}hr {minutes:0.0f}min {seconds:.2f}s")

def save_logs(n, t):
    with open("logs.txt", "a") as f:
        f.write(f"{n};{t}\n")

def random_mode(args):
    number_of_experiments = int(args[2])
    output_path = args[3]
    number_of_initial_values = 0

    if len(args) == 5:
        number_of_initial_values = int(args[4])

    num_of_workers = 32
    timeout = number_of_experiments
    timeout = timeout * 0.05 if len(args) == 5 else timeout * 0.025
    batch_size = number_of_experiments // num_of_workers
    start_time = time.time()
    print_time(start_time, "Started: ")

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_of_workers) as executor:
        futures = [executor.submit(run_experiment, batch_size, n, number_of_initial_values) for n in range(num_of_workers)]
        timeouts = {}
        results = []
        try:
            for future in concurrent.futures.as_completed(futures, timeout=timeout):
                try:
                    results.extend(future.result())
                except TimeoutError:
                    print_duration(timeout, "Timeout has been exceeded ")
                    timeouts[future] = True
        except TimeoutError:
            print("Overall timeout has been exceeded")

        for future in timeouts:
            future.cancel()

    end_time = time.time()
    print_duration(end_time - start_time, "Execution time: ")

    save_logs(number_of_experiments, end_time - start_time)

    start_time = time.time()
    write_output(results, output_path)
    end_time = time.time()
    print_duration(end_time - start_time, "Writing time: ")
    print_time(end_time, "Finished: ")


def solve_from_file(grids, batch_number):
    results = []
    debug_file = f"logs/batch_{batch_number}.txt"
    with open(debug_file, "a") as f:
        f.write("")
        
    for g in grids:
        sudoku = Sudoku(g)
        analyzer = SudokuAnalyzer(sudoku)
        sudoku_properties = analyzer.get_sudoku_description()

        number_of_steps = -1
        solver = SudokuSolver(sudoku, debug_file)
        solved_sudoku = solver.solve()
        if solved_sudoku is not None:
            number_of_steps = solver.number_of_steps
        
        with open(debug_file, "a") as f:
            f.write(f"{sudoku_properties[0]};{sudoku_properties[1]};{sudoku_properties[2]};{number_of_steps}\n\n\n")

        results.append(f"{sudoku.get_hash()};{sudoku_properties[0]};{sudoku_properties[1]};{sudoku_properties[2]};{number_of_steps}\n")
    
    print(f"Batch {batch_number} finished.")
    return results
    pass

def hash_to_grid(hash: str):
    grid = ""
    for i in range(0, 81, 9):
        grid += hash[i : i + 9] + "\n"

    return grid

def split_list_into_n_chunks(lst, n):
    chunk_size, remainder = divmod(len(lst), n)
    start = 0
    chunks = []
    for i in range(n):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunks.append(lst[start:end])
        start = end
    return chunks

def from_file_mode():
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    num_of_workers = 32


    with open(input_file) as f:
        hashes = [line.strip() for line in f]
        grids = [hash_to_grid(h) for h in hashes]
    
    splitted_grids = split_list_into_n_chunks(grids, num_of_workers)
    no_grids = len(grids)
    timeout = no_grids * 0.03

    print(f"Number of grids to be solved {no_grids}")

    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_of_workers) as executor:
        futures = [executor.submit(solve_from_file, splitted_grids[n], n) for n in range(num_of_workers)]
        timeouts = {}
        results = []
        try:
            for future in concurrent.futures.as_completed(futures):
                try:
                    results.extend(future.result())
                except TimeoutError:
                    print_duration(timeout, "Timeout has been exceeded ")
                    timeouts[future] = True
        except TimeoutError:
            print("Overall timeout has been exceeded")

        for future in timeouts:
            future.cancel()
        
    end_time = time.time()
    print_duration(end_time - start_time, "Execution time: ")

    write_output(results, output_file)
    print_time(end_time, "Finished: ")


def main():
    if sys.argv[1] == "-r":
        random_mode(sys.argv)

    elif sys.argv[1] == "-f":
        from_file_mode()

    

if __name__ == "__main__":
    main()