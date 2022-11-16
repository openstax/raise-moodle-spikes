from datetime import datetime
import json
from typing import Literal
from uuid import UUID, uuid4
from math import isnan
import os
import boto3
import argparse
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from pydantic import BaseModel, Extra, validator

MODEL_FILE_USERS = "users.csv"
MODEL_FILE_COURSES = "courses.csv"
MODEL_FILE_ONEROSTER_DEMOGRAPHICS = "oneroster_demographics.csv"
MODEL_FILE_ENROLLMENTS = "enrollments.csv"
MODEL_FILE_ASSESSMENTS = "assessments.csv"
MODEL_FILE_GRADES = "grades.csv"


class Demographic(BaseModel):
    user_uuid: UUID
    birth_date: str
    sex: Literal['male', 'female']
    american_indian_or_alaska_native: Literal['true', 'false']
    asian: Literal['true', 'false']
    black_or_african_american: Literal['true', 'false']
    native_hawaiian_or_other_pacific_islander: Literal['true', 'false']
    white: Literal['true', 'false']
    demographic_race_two_or_more_races: Literal['true', 'false']
    hispanic_or_latino_ethnicity: Literal['true', 'false']

    class Config:
        extra = Extra.forbid

    @validator('birth_date')
    def birthdate_format(cls, v):
        datetime.strptime(v, "%Y-%m-%d")
        return v


class Assessment(BaseModel):
    id: int
    name: str

    class Config:
        extra = Extra.forbid


class Course(BaseModel):
    id: int
    name: str

    class Config:
        extra = Extra.forbid


class Enrollment(BaseModel):
    user_uuid: UUID
    course_id: int
    role: Literal['student', 'teacher']

    class Config:
        extra = Extra.forbid


class Grade(BaseModel):
    assessment_id: int
    user_uuid: UUID
    course_id: int
    grade_percentage: float
    time_submitted: int

    class Config:
        extra = Extra.forbid

    @validator('grade_percentage')
    def grade_value(cls, v):
        if isnan(v):
            raise ValueError('Grade value is nan')
        if v < 0.0 or v > 100.0:
            raise ValueError(f'Grade value {v} is out of expected range')
        return v


class User(BaseModel):
    uuid: UUID
    first_name: str
    last_name: str
    email: str

    class Config:
        extra = Extra.forbid


def courses_model(clean_raw_df):
    courses_df = clean_raw_df['courses']

    for item in courses_df.to_dict(orient='records'):
        Course.parse_obj(item)

    return courses_df


def enrollments_model(clean_raw_df):
    enrollments_df = clean_raw_df['enrollments']
    users_df = clean_raw_df['cli_users'][['user_id', 'uuid']]
    enrollments_df = pd.merge(enrollments_df, users_df, on='user_id')
    enrollments_df.rename(columns={'uuid': 'user_uuid'}, inplace=True)
    enrollments_df = enrollments_df[['user_uuid', 'course_id', 'role']]

    for item in enrollments_df.to_dict(orient='records'):
        Enrollment.parse_obj(item)

    return enrollments_df


def users_model(clean_raw_df):
    users_df = clean_raw_df['cli_users']
    users_df = users_df[['uuid', 'first_name', 'last_name', 'email']]

    for item in users_df.to_dict(orient='records'):
        User.parse_obj(item)

    return users_df


def assessments_and_grades_model(clean_raw_df):
    grades_df = clean_raw_df['grades']
    assessments_df = pd.DataFrame(
        grades_df['assessment_name'].unique(), columns=['name']
    )
    assessments_df['id'] = assessments_df.index
    grades_df = pd.merge(
        grades_df, assessments_df, left_on='assessment_name', right_on='name'
    )
    grades_df.rename(columns={'id': 'assessment_id'}, inplace=True)
    cli_users = clean_raw_df['cli_users'][['user_id', 'uuid']]
    grades_df = pd.merge(grades_df, cli_users, on='user_id')
    grades_df.rename(columns={'uuid': 'user_uuid'}, inplace=True)
    grades_df = grades_df[
        ['assessment_id',
         'user_uuid',
         'course_id',
         'grade_percentage',
         'time_submitted'
         ]
    ]

    def convert_percentage(x):
        if x == '-':
            return None
        return float(x.strip("%"))

    grades_df['grade_percentage'] = grades_df['grade_percentage'].map(
        convert_percentage
    )
    grades_df = grades_df[grades_df['grade_percentage'].notnull()]
    grades_df['time_submitted'] = grades_df['time_submitted'].astype(int)

    for item in assessments_df.to_dict(orient='records'):
        Assessment.parse_obj(item)
    for item in grades_df.to_dict(orient='records'):
        Grade.parse_obj(item)

    return assessments_df, grades_df


def demographics_model(all_raw_dfs):

    demographic_df = all_raw_dfs['demographics']

    demographic_df.rename(
        columns={
            'birthDate':
            'birth_date',
            'americanIndianOrAlaskaNative':
            'american_indian_or_alaska_native',
            'blackOrAfricanAmerican':
            'black_or_african_american',
            'nativeHawaiianOrOtherPacificIslander':
            'native_hawaiian_or_other_pacific_islander',
            'demographicRaceTwoOrMoreRaces':
            'demographic_race_two_or_more_races',
            'hispanicOrLatinoEthnicity':
            'hispanic_or_latino_ethnicity'
        }, inplace=True)

    id_2_email = all_raw_dfs['or_users'][['email', 'sourcedId']]
    demographic_df = pd.merge(id_2_email, demographic_df, on='sourcedId')
    email_2_uuid = all_raw_dfs['cli_users'][['email', 'uuid']]
    demographic_df = pd.merge(email_2_uuid, demographic_df, on='email')

    demographic_df.rename(columns={'uuid': 'user_uuid'}, inplace=True)

    demographic_df = demographic_df[
        ['user_uuid', 'birth_date', 'sex',
         'american_indian_or_alaska_native', 'asian',
         'black_or_african_american',
         'native_hawaiian_or_other_pacific_islander', 'white',
         'demographic_race_two_or_more_races', 'hispanic_or_latino_ethnicity']]

    for item in demographic_df.to_dict(orient='records'):
        Demographic.parse_obj(item)

    return demographic_df


def scrub_raw_dfs(all_raw_dfs):
    or_users_df = all_raw_dfs['or_users']
    cli_users_df = all_raw_dfs['cli_users']

    or_users_df['email'] = or_users_df['email'].apply(
        lambda col: col.lower())
    cli_users_df['email'] = cli_users_df['email'].apply(
        lambda col: col.lower())

    grade_df = all_raw_dfs['grades']
    grade_df = grade_df[grade_df['assessment_name'].notnull()]

    all_raw_dfs['or_users'] = or_users_df
    all_raw_dfs['cli_users'] = cli_users_df
    all_raw_dfs['grades'] = grade_df

    return all_raw_dfs


def create_models(output_path, all_raw_dfs):

    clean_raw_df = scrub_raw_dfs(all_raw_dfs)

    demographics_df = demographics_model(clean_raw_df)
    assessments_df, grades_df = assessments_and_grades_model(clean_raw_df)
    users_df = users_model(clean_raw_df)
    enrollments_df = enrollments_model(clean_raw_df)
    courses_df = courses_model(clean_raw_df)

    with open(f"{output_path}/{MODEL_FILE_ONEROSTER_DEMOGRAPHICS}", "w") as f:
        demographics_df.to_csv(f, index=False)
    with open(f"{output_path}/{MODEL_FILE_USERS}", "w") as f:
        users_df.to_csv(f, index=False)
    with open(f"{output_path}/{MODEL_FILE_GRADES}", "w") as f:
        grades_df.to_csv(f, index=False)
    with open(f"{output_path}/{MODEL_FILE_ENROLLMENTS}", "w") as f:
        enrollments_df.to_csv(f, index=False)
    with open(f"{output_path}/{MODEL_FILE_COURSES}", "w") as f:
        courses_df.to_csv(f, index=False)
    with open(f"{output_path}/{MODEL_FILE_ASSESSMENTS}", "w") as f:
        assessments_df.to_csv(f, index=False)


def generate_grade_df(grade_dict):
    grade_data = []
    for course_id in grade_dict.keys():
        for user in grade_dict[course_id]['usergrades']:
            for grade in user['gradeitems']:
                grade_data.append({
                    'user_id': user['userid'],
                    'grade_percentage': grade['percentageformatted'],
                    'assessment_name': grade['itemname'],
                    'course_id': course_id,
                    'time_submitted': grade['gradedatesubmitted']
                })
    return pd.DataFrame(grade_data)


def generate_enrollment_df(users_dict):
    enrollment_data = []
    for course_id in users_dict.keys():
        for user in users_dict[course_id]:
            enrollment_data.append({
                'user_id': user['id'],
                'course_id': course_id,
                'role': user['roles'][0]['shortname']
            })
    return pd.DataFrame(enrollment_data)


def generate_courses_df(users_dict):
    course_data = []
    for course_id in users_dict.keys():
        enrolled = users_dict[course_id][0]['enrolledcourses']
        for course in enrolled:
            if course['id'] == course_id:
                course_data.append({
                    'id': course['id'],
                    'name': course['fullname']
                    })
    return pd.DataFrame(course_data)


def generate_users_df(users_dict):
    user_data = []
    # Use email addresses to de-duplicate users
    seen_users = set()

    for course_id in users_dict.keys():
        for user in users_dict[course_id]:
            user_email = user['email']
            if user_email not in seen_users:
                seen_users.add(user_email)
                user_data.append({
                    "first_name": user['firstname'],
                    "last_name": user['lastname'],
                    "email": user_email,
                    "user_id": user['id'],
                    "uuid": uuid4()
                })
    return pd.DataFrame(user_data)


def collect_cli_dfs(bucket, prefix):
    grades_dict, users_dict = {}, {}
    s3_client = boto3.client("s3")
    # Note that these will only get 1000 classes at a time
    grade_data_objects = s3_client.list_objects(
        Bucket=bucket,
        Prefix=f"{prefix}/grades"
    )
    users_data_objects = s3_client.list_objects(
        Bucket=bucket,
        Prefix=f"{prefix}/users"
    )
    for data_object in grade_data_objects.get("Contents"):
        object_key = data_object.get("Key")
        course_id = object_key.split("/")[-1].split(".json")[0]
        data = s3_client.get_object(
            Bucket=bucket,
            Key=object_key
        )
        contents = data["Body"].read()
        grades_dict[int(course_id)] = json.loads(contents)

    for data_object in users_data_objects.get("Contents"):
        object_key = data_object.get("Key")
        course_id = object_key.split("/")[-1].split(".json")[0]
        data = s3_client.get_object(
            Bucket=bucket,
            Key=object_key
        )
        contents = data["Body"].read()
        users_dict[int(course_id)] = json.loads(contents)

    return {
        'cli_users': generate_users_df(users_dict),
        'courses': generate_courses_df(users_dict),
        'enrollments': generate_enrollment_df(users_dict),
        'grades': generate_grade_df(grades_dict)
    }


def collect_oneroster_dfs(bucket, key):
    s3_client = boto3.client("s3")
    data = s3_client.get_object(
        Bucket=bucket,
        Key=key)

    dfs = {}
    zipfile_data = data["Body"].read()
    zf = ZipFile(BytesIO(zipfile_data))
    for name in zf.namelist():
        common_types = {
            'sourcedId': str
        }
        if name == 'demographics.csv':
            types = common_types | {
                'americanIndianOrAlaskaNative': str,
                'asian': str,
                'blackOrAfricanAmerican': str,
                'nativeHawaiianOrOtherPacificIslander': str,
                'white': str,
                'demographicRaceTwoOrMoreRaces': str,
                'hispanicOrLatinoEthnicity': str
                }
            dfs[name] = pd.read_csv(BytesIO(zf.read(name)), dtype=types)
        else:
            dfs[name] = pd.read_csv(BytesIO(zf.read(name)), dtype=common_types)

    return {
        'demographics': dfs['demographics.csv'],
        'or_users': dfs['users.csv']
    }


def compile_models(cli_bucket, cli_key, oneroster_bucket, oneroster_key):
    oneroster_dfs = collect_oneroster_dfs(oneroster_bucket, oneroster_key)
    cli_dfs = collect_cli_dfs(cli_bucket, cli_key)
    all_raw_dfs = oneroster_dfs | cli_dfs
    return all_raw_dfs


def main():
    parser = argparse.ArgumentParser(description='Upload Resources to S3')
    parser.add_argument('cli_data_bucket', type=str,
                        help='bucket for the moodle grade and user data dirs')
    parser.add_argument('cli_data_prefix', type=str,
                        help='prefix for the moodle grade and user data dirs')
    parser.add_argument('oneroster_bucket', type=str,
                        help='bucket for oneroster data')
    parser.add_argument('oneroster_key', type=str,
                        help='key + filename for one roster data')
    args = parser.parse_args()

    output_path = os.environ["CSV_OUTPUT_DIR"]

    all_raw_dfs = compile_models(
        args.cli_data_bucket,
        args.cli_data_prefix,
        args.oneroster_bucket,
        args.oneroster_key)

    create_models(output_path, all_raw_dfs)


if __name__ == "__main__":  # pragma: no cover
    main()
