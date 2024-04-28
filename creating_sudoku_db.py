import pandas as pd
from joblib import load

model = load('sudoku_model.joblib')
def predict_difficulty(predictors):
    """
    Predicts the difficulty level of a Sudoku puzzle using a pre-trained machine learning model.

    Parameters
    ----------
    predictors : list
        A list containing the predictors needed by the model, typically including metrics like
        the sum of candidates, the number of initial values, and the initial numbers' entropy.

    Returns
    -------
    float
        The predicted difficulty level of the Sudoku puzzle.
    """
    return model.predict([predictors])[0]

def main():
    """
    Main function to process and analyze Sudoku puzzles, assign difficulty levels, and save the results to a CSV file.
    """
     
    # merge csvs into one df
    files = ['analysis_random_v3.csv', 'recursively_generated_grids_1.csv']
    df_list = []

    for filename in files:
        df = pd.read_csv('csvs/' + filename, index_col=None, header=0, sep=";")
        df_list.append(df)

    df = pd.concat(df_list, axis=0, ignore_index=True)
    
    # filter out invalid puzzles
    df['is_valid'] = df['number_of_steps_to_solve'] != -1
    df_valid = df[df['is_valid']]

    # remove outliers
    df_valid = df_valid.sort_values('number_of_steps_to_solve').iloc[10 : -10]
    df_valid = df_valid[df_valid['number_of_initial_values'] < 71]

    # assign difficulty level
    df_valid["difficulty_level"] =  df_valid.apply(lambda x: predict_difficulty([x['sum_of_candidates'], x['number_of_initial_values'], x['initial_numbers_entropy']]), axis=1)
    
    max_value = df_valid["difficulty_level"].max()
    min_value = df_valid["difficulty_level"].min()

    # normalize to scale 1-10
    df_valid["difficulty_level"] = 1 + ((df_valid["difficulty_level"] - min_value) * 9 / (max_value - min_value))

    # save to the file
    df_valid = df_valid.sort_values('difficulty_level')
    df_valid["difficulty_level"] = df_valid["difficulty_level"].apply(
        lambda x: f"{x:.3f}" if x >= 10 else f"{x:.4f}"
    )

    df_valid[['sudoku', 'difficulty_level']].to_csv("sudoku_db.csv", sep=';', index=False, header=False)

if __name__ == "__main__":
    main()