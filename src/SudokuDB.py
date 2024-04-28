import os

class SudokuDB:
    """
    A class to interact with a database of Sudoku puzzles stored in a CSV file.
    Provides functionality to retrieve puzzles based on their difficulty.

    Attributes
    ----------
    filepath : str
        The path to the CSV file containing the Sudoku puzzles.
    """
    def __init__(self) -> None:
        """
        Initializes the SudokuDB with the path to the database file.
        """
        self.filepath = 'sudoku_db.csv'
    
    def get_sudoku_by_diff(self, desired_difficulty: float) -> str: 
        """
        Retrieves a Sudoku puzzle that closely matches a specified difficulty level.
        This function performs a linear search to find the puzzle with the smallest
        difficulty difference.

        Parameters
        ----------
        desired_difficulty : float
            The difficulty level of the Sudoku puzzle to retrieve, between 1 and 10.

        Returns
        -------
        str
            The CSV line corresponding to the Sudoku puzzle closest to the desired difficulty.
        
        Raises
        ------
        ValueError
            If the desired difficulty is not within the valid range (1 to 10).
        """
        if not (1 <= desired_difficulty <= 10):
            raise ValueError("Desired difficulty must be between 1 and 10")
        
        delta = 10
        choice = None
        with open(self.filepath) as f:
            f.readline()
            for line in f:
                diff = float(line.split(";")[-1].strip())
                if abs(diff - desired_difficulty) > delta:
                    return choice
                
                delta = abs(diff - desired_difficulty)
                choice = line
        
        return choice
    
    def get_sudoku_by_diff_2(self, desired_difficulty: float) -> str:
        """
        Retrieves a Sudoku puzzle that closely matches a specified difficulty level.
        This function performs a binary search assuming the file is sorted by difficulty.

        Parameters
        ----------
        desired_difficulty : float
            The difficulty level of the Sudoku puzzle to retrieve, between 1 and 10.

        Returns
        -------
        str
            The CSV line corresponding to the Sudoku puzzle closest to the desired difficulty.
        
        Raises
        ------
        ValueError
            If the desired difficulty is not within the valid range (1 to 10).
        """
        if not (1 <= desired_difficulty <= 10):
            raise ValueError("Desired difficulty must be between 1 and 10")

        with open(self.filepath, 'r') as file:
            first_line = file.readline()
            line_length = len(first_line) + 1

            file.seek(0)
            file_size = os.path.getsize(self.filepath)
            number_of_lines = file_size // line_length

            low, high = 0, number_of_lines - 1
            choice = None
            delta = float('inf')

            while low <= high:
                mid = (low + high) // 2
                file.seek(mid * line_length)

                current_line = file.readline().strip()
                if not current_line:
                    break 

                last_value = float(current_line.split(';')[-1])

                diff = abs(last_value - desired_difficulty)
                if diff < delta:
                    delta = diff
                    choice = current_line

                if last_value < desired_difficulty:
                    low = mid + 1
                else:
                    high = mid - 1

        return choice