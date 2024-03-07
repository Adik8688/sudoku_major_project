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

def run_simulation():
    sudoku = Sudoku(SEED)
    scrambler = SudokuScrambler(sudoku)
    scrambler.scramble()
    analyzer = SudokuAnalyzer(sudoku)
    sudoku_properties = analyzer.get_sudoku_description()

    solver = SudokuSolver(sudoku)
    solved_sudoku = solver.solve()
    if solved_sudoku is None:
        return ""
    
    return f"{sudoku_properties[0]};{sudoku_properties[1]};{sudoku_properties[2]};{solver.number_of_steps}\n"

def write_output(results, output_path):
    with open(output_path, 'a') as f:
        for r in results:
            if r:
                f.write(r)

def main():
    if len(sys.argv) != 3:
        print("Invalid argumets")
        exit(-1)

    n = int(sys.argv[1])
    output_path = sys.argv[2]

    start_time = time.time()

    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(run_simulation) for _ in range(n)]

        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    end_time = time.time()

    print(f"Execution time: {end_time - start_time} seconds")
    
    write_output(results, output_path)



if __name__ == "__main__":
    main()