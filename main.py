import sys
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

def run_experiment(batch_size, batch_number):
    results = []
    for _ in range(batch_size):
        sudoku = Sudoku(SEED)
        scrambler = SudokuScrambler(sudoku)
        scrambler.scramble()
        analyzer = SudokuAnalyzer(sudoku)
        sudoku_properties = analyzer.get_sudoku_description()

        solver = SudokuSolver(sudoku)
        solved_sudoku = solver.solve()
        if solved_sudoku is None:
            results.append("")
            continue

        results.append(f"{sudoku_properties[0]};{sudoku_properties[1]};{sudoku_properties[2]};{solver.number_of_steps}\n")
    
    print(f"Batch {batch_number} finished.")
    return results

def write_output(results, output_path):
    with open(output_path, 'a') as f:
        for r in results:
            if r:
                f.write(r)

def check_arguments(args):
    if len(args) != 3:
        print(f"Invalid number of arguments! {args[0]} takes 2 arguments.")
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



def main():
    check_arguments(sys.argv)

    number_of_experiments = int(sys.argv[1])
    output_path = sys.argv[2]
    num_of_workers = 16
    batch_size = number_of_experiments // num_of_workers
    start_time = time.time()
    print_time(start_time, "Started: ")

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_of_workers) as executor:
        futures = [executor.submit(run_experiment, batch_size, n) for n in range(num_of_workers)]

        results = []
        for future in concurrent.futures.as_completed(futures):
            results.extend(future.result())

    end_time = time.time()
    print_duration(end_time - start_time, "Execution time: ")

    start_time = time.time()
    write_output(results, output_path)
    end_time = time.time()
    print_duration(end_time - start_time, "Writing time: ")
    print_time(end_time, "Finished: ")

if __name__ == "__main__":
    main()