import os
import pandas as pd
from collections import defaultdict

INPUT_PATH = os.getenv('DATA_INPUT_DIR')
RESULTS_OUTPUT_PATH = os.getenv('RESULT_OUTPUT_DIR')

quiz_questions = pd.read_csv(
    f'{INPUT_PATH}/quiz_questions.csv'
)
quiz_question_contents = pd.read_csv(
    f'{INPUT_PATH}/quiz_question_contents.csv'
)
quiz_multichoice_answers = pd.read_csv(
    f'{INPUT_PATH}/quiz_multichoice_answers.csv'
)

merged_data = pd.merge(
    quiz_questions, quiz_question_contents,
    left_on="question_id", right_on='id'
)
merged_data.pop('id')
merged_data.rename(columns={'text': 'question_text'}, inplace=True)

answer_data = pd.merge(
    quiz_multichoice_answers, merged_data,
    on="question_id"
)
data_by_question = defaultdict(list)
for index, row in answer_data.iterrows():
    data_by_question[row['question_id']].append(row)

headers = [
    "quiz_name",
    "question_number",
    "question_id",
    "question_text",
    "answer_a_text",
    "answer_b_text",
    "answer_c_text",
    "answer_d_text",
    "answer_a_grade",
    "answer_b_grade",
    "answer_c_grade",
    "answer_d_grade",
    "answer_a_feedback",
    "answer_b_feedback",
    "answer_c_feedback",
    "answer_d_feedback"
]
questions_df = pd.DataFrame(columns=headers)
for key in data_by_question.keys():
    text = []
    grade = []
    feedback = []
    for answer in data_by_question[key]:
        text.append(answer["text"])
        grade.append(answer["grade"])
        feedback.append(answer["feedback"])
    item = data_by_question[key][0]
    new_row = pd.DataFrame({
        "quiz_name": [item["assessment_id"]],
        "question_number": [item["question_number"]],
        "question_id": [item["question_id"]],
        "question_text": [item["question_text"]],
        "answer_a_text": [text[0]],
        "answer_b_text": [text[1]],
        "answer_c_text": [text[2]],
        "answer_d_text": [text[3]],
        "answer_a_grade": [grade[0]],
        "answer_b_grade": [grade[1]],
        "answer_c_grade": [grade[2]],
        "answer_d_grade": [grade[3]],
        "answer_a_feedback": [feedback[0]],
        "answer_b_feedback": [feedback[1]],
        "answer_c_feedback": [feedback[2]],
        "answer_d_feedback": [feedback[3]]
    })
    questions_df = pd.concat([questions_df, new_row], ignore_index=True)


questions_df.to_csv(f'{RESULTS_OUTPUT_PATH}/levi_data.csv', index=False)
