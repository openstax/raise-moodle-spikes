import pandas as pd
import os


INPUT_PATH = os.getenv('DATA_INPUT_DIR')
RESULTS_OUTPUT_PATH = os.getenv('RESULT_OUTPUT_DIR')

grades = pd.read_csv(f'{INPUT_PATH}/grades.csv')
demographic = pd.read_csv(f'{INPUT_PATH}/oneroster_demographics.csv')


merged_data = pd.merge(grades, demographic, on='user_uuid', how='outer')


average_grade_by_sex = merged_data[["sex", "grade_percentage"]].groupby('sex').mean()


average_grade_by_sex.to_csv(f'{RESULTS_OUTPUT_PATH}/average_grades_by_sex.csv')
