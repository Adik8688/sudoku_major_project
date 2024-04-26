import os

class SudokuDB:
    def __init__(self) -> None:
        self.filepath = 'sudoku_db.csv'

    
    def get_sudoku_by_diff(self, desired_difficulty):
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
    
    def get_sudoku_by_diff_2(self, desired_difficulty):
        if not (1 <= desired_difficulty <= 10):
            raise ValueError("Target value must be between 1 and 10")

        with open(self.filepath, 'r') as file:
            # Determine the actual line length including newline
            first_line = file.readline()
            line_length = len(first_line) + 1  # Ensure this is correct

            # Reset file pointer to beginning after getting the line length
            file.seek(0)
            file_size = os.path.getsize(self.filepath)
            number_of_lines = file_size // line_length

            low, high = 0, number_of_lines - 1
            closest_line = None
            smallest_diff = float('inf')

            while low <= high:
                mid = (low + high) // 2
                file.seek(mid * line_length)

                # Read the current line to align the pointer
                current_line = file.readline().strip()
                if not current_line:
                    break  # In case we reach EOF

                # Parse the last attribute as float
                last_value = float(current_line.split(';')[-1])

                # Track the closest line
                diff = abs(last_value - desired_difficulty)
                if diff < smallest_diff:
                    smallest_diff = diff
                    closest_line = current_line

                # Adjust the search range based on the mid value comparison
                if last_value < desired_difficulty:
                    low = mid + 1
                else:
                    high = mid - 1

        return closest_line