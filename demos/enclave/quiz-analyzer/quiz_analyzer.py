import os
import pandas as pd
from pathlib import Path

DATA_ENCLAVE_ASSESSMENTS = "assessments.csv"
DATA_ENCLAVE_GRADES = "grades.csv"


data_input_path = Path(os.getenv('DATA_INPUT_DIR'))
result_output_path = Path(os.getenv('RESULT_OUTPUT_DIR'))

grades = pd.read_csv(data_input_path / DATA_ENCLAVE_GRADES)
assessments = pd.read_csv(data_input_path / DATA_ENCLAVE_ASSESSMENTS)

data = pd.merge(grades, assessments, left_on='assessment_id', right_on='id')
course_summary = data.groupby(['course_id', 'name']).size().reset_index()
course_summary.rename(columns={0: "count"}, inplace=True)

quiz_summary = data.groupby(['name']).size().reset_index()
quiz_summary.rename(columns={0: "count"}, inplace=True)

with open(result_output_path / "course_quiz_summary.csv", "w") as f:
    course_summary.to_csv(f, index=False)

with open(result_output_path / "quiz_summary.csv", "w") as f:
    quiz_summary.to_csv(f, index=False)
