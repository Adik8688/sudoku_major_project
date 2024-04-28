# Instalation

1. Create virtual env
python -m venv venv
venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

# Usage

python .\main_GUI.py 
Runs GUI and provide interactive application.

python .\main.py -r <number of experiments> <output path> <desired number of clues (optional)>
Randomly generates the specified number of Sudoku grids, then save them to the output path, along with its properties and the number of steps the solver needed to solve it. It is possible to set fixed number of clues.

python .\main.py -f <input file> <output file>
Same as -r, but takes grids from the file rather than generate them.

python .\recursive_removal.py <number of grids to generate> <initial number of clues> <desired number of clues>
Generates up to specified number of subgrids with desired number of clues. A file with corresponding number of initial clues must exist in the grid\ directory.