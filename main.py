import sys
import os.path
from src.Sudoku import Sudoku
from src.SudokuScrambler import SudokuScrambler
from src.SudokuAnalyzer import SudokuAnalyzer
from src.SudokuSolver import SudokuSolver
import concurrent.futures
import time
import glob


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
    """
    Runs a batch of Sudoku scrambling and analysis experiments.

    Parameters
    ----------
    batch_size : int
        The number of Sudoku puzzles to process in this batch.
    batch_number : int
        The identifier for the current batch.
    number_of_initial_values : int
        The number of initial values to set in the Sudoku puzzle.

    Returns
    -------
    list
        A list of results with Sudoku properties and solver metrics.
    """
    results = []
        
    for _ in range(batch_size):
        sudoku = Sudoku(SEED)
        scrambler = SudokuScrambler(sudoku, number_of_initial_values)
        scrambler.scramble()
        analyzer = SudokuAnalyzer(sudoku)
        sudoku_properties = analyzer.get_sudoku_description()

        number_of_steps = -1
        solver = SudokuSolver(sudoku)
        solved_sudoku = solver.solve()
        if solved_sudoku is not None:
            number_of_steps = solver.number_of_steps
        

        results.append(f"{sudoku.get_hash()};{sudoku_properties[0]};{sudoku_properties[1]};{sudoku_properties[2]};{number_of_steps}\n")
    
    print(f"Batch {batch_number} finished.")
    return results

def write_output(results, output_path):
    """
    Writes the results of Sudoku experiments to a file.

    Parameters
    ----------
    results : list
        The list of string results to write to the file.
    output_path : str
        The path to the output file.
    """
    if not os.path.isfile(output_path):
        results = ["sudoku;sum_of_candidates;number_of_initial_values;initial_numbers_entropy;number_of_steps_to_solve\n"] + results
        
    with open(output_path, 'a') as f:
        for r in results:
            if r:
                f.write(r)

def print_time(time_in, message=""):
    """
    Prints the current time with a custom message.

    Parameters
    ----------
    time_in : float
        The time in seconds since the epoch.
    message : str
        The message to prepend to the time printout.
    """
    local_time = time.localtime(time_in)
    print(f"{message}{local_time.tm_hour:02}:{local_time.tm_min:02}:{local_time.tm_sec:02}")

def print_duration(time_in_seconds, message=""):
    """
    Prints the duration in a formatted string.

    Parameters
    ----------
    time_in_seconds : float
        Duration in seconds.
    message : str
        A message to prepend to the duration.
    """
    hours: int = time_in_seconds // 3600
    time_in_seconds = time_in_seconds % 3600
    minutes = time_in_seconds // 60
    seconds = time_in_seconds % 60
   
    print(f"{message}{hours:0.0f}hr {minutes:0.0f}min {seconds:.2f}s")

def save_logs(n, t):
    """
    Saves log entries to a log file.

    Parameters
    ----------
    n : int
        The batch number or identifier.
    t : float
        The time-related data to log.
    """
    with open("logs.txt", "a") as f:
        f.write(f"{n};{t}\n")

def random_mode(args):
    """
    Handles the generation and analysis of random Sudoku grids based on a specified number of experiments and initial values.

    Parameters
    ----------
    args : list
        Command-line arguments provided to the script. Expected to include the number of experiments, output path, and optionally the number of initial values.

    This function manages the distribution of Sudoku generation tasks across multiple processes and collates the results.
    """
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
    """
    Solves a batch of Sudoku puzzles loaded from a file.

    Parameters
    ----------
    grids : list
        List of Sudoku grid strings.
    batch_number : int
        Identifier for the batch, used for debugging and logging purposes.

    Returns
    -------
    list
        Results of the Sudoku solving process for each grid in the batch.
    """
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

def split_list_into_n_chunks(lst, n):
    """
    Splits a list into n approximately equal parts.

    Parameters
    ----------
    lst : list
        The list to split.
    n : int
        The number of chunks to split the list into.

    Returns
    -------
    list
        A list of lists, where each sublist is one part of the original list.
    """
    chunk_size, remainder = divmod(len(lst), n)
    start = 0
    chunks = []
    for i in range(n):
        end = start + chunk_size + (1 if i < remainder else 0)
        chunks.append(lst[start:end])
        start = end
    return chunks

def from_file_mode():
    """
    Processes Sudoku grids loaded from files specified on the command line, using multiprocessing to distribute the work.

    This function reads grids from files, splits them into chunks for processing, solves them, and writes the results to an output file.
    """
    input_path = sys.argv[2]
    output_file = sys.argv[3]
    num_of_workers = 32

    file_paths = glob.glob(input_path)
    all_grids = []

    for input_file in file_paths:
        with open(input_file) as f:
            grids = [line.strip() for line in f]
            all_grids.extend(grids)
    
    
    splitted_grids = split_list_into_n_chunks(all_grids, num_of_workers)
    no_grids = len(all_grids)
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