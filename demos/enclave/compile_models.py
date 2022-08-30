from enum import unique
import json
from uuid import UUID
import uuid
import os
import boto3
import argparse
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from pydantic import BaseModel

MODEL_FILE_USERS = "users.csv"
MODEL_FILE_COURSES = "courses.csv"
MODEL_FILE_ONEROSTER_DEMOGRAPHICS = "oneroster_demographics.csv"
MODEL_FILE_ENROLLMENTS = "enrolments.csv"
MODEL_FILE_ASSESSMENTS = "assessments.csv"
MODEL_FILE_GRADES = "grades.csv"


class Demographic(BaseModel):
    user_uuid: UUID
    birth_date: str
    sex: str
    american_indian_or_alaska_native: str
    asian: str
    black_or_african_american: str
    native_hawaiian_or_other_pacific_islander: str
    white: str
    demographic_race_two_or_more_races: str
    hispanic_or_latino_ethnicity: str


class Assessment(BaseModel):
    id: int
    name: str


class Course(BaseModel):
    id: int
    name: str


class Enrollment(BaseModel):
    user_uuid: UUID
    course_id: int
    role: str


class Grades(BaseModel):
    assessment_id: int
    user_uuid: UUID
    course_id: int
    grade_percentage: float


class User(BaseModel):
    user_uuid: UUID
    first_name: str
    last_name: str
    email: str


def assessment_model(cli_grades):
    unique_courses = []
    assessments = []
    for user_item in cli_grades["usergrades"]:
        course_id = user_item["courseid"]
        if course_id not in unique_courses:
            unique_courses.append(course_id)
            for grade_item in user_item["gradeitems"]:
                print(grade_item)
                if grade_item["itemname"] is not None:
                    data = {
                        "id": grade_item["id"],
                        "name": grade_item["itemname"]
                    }
                    assessments.append(Assessment.parse_obj(data))
    return pd.DataFrame([s.__dict__ for s in assessments])


def courses_model(cli_users):
    unique_ids = []
    courses = []
    for user in cli_users:
        course_id = user["enrolledcourses"][0]["id"]
        if course_id not in unique_ids:
            unique_ids.append(course_id)
            data = {
                "id": course_id,
                "name": user["enrolledcourses"][0]["fullname"]
            }
            courses.append(Course.parse_obj(data))
    return pd.DataFrame([s.__dict__ for s in courses])


def enrollments_model(cli_users, email_2_uuid):
    enrolments = []
    for user_item in cli_users:
        uuid = email_2_uuid[user_item["email"]]
        data = {
            "user_uuid": uuid,
            "course_id": user_item["enrolledcourses"][0]["id"],
            "role": user_item["roles"][0]["shortname"]
        }
        enrolments.append(Enrollment.parse_obj(data))
    return pd.DataFrame([s.__dict__ for s in enrolments])


def grades_model(cli_grades, userid_2_email, email_2_uuid):
    grades = []
    for user_item in cli_grades["usergrades"]:
        course_id = user_item["courseid"]
        uuid = email_2_uuid[userid_2_email[user_item["userid"]]]
        for assn in user_item["gradeitems"]:
            grade = assn["percentageformatted"].strip('%')
            if grade == "-":
                continue
            else: 
                grade = float(grade)
            data = {
                "assessment_id": assn["id"],
                "user_uuid": uuid,
                "course_id": course_id,
                "grade_percentage": float(assn["percentageformatted"].strip('%'))
            }
            grades.append(Grades.parse_obj(data))
    return pd.DataFrame([s.__dict__ for s in grades])
            

def users_model(oneroster_users, sourceid_2_email, email_2_uuid):
    users = []
    for i in range (len(oneroster_users["sourceId"])):
        uuid = email_2_uuid[sourceid_2_email[oneroster_users["sourceId"][i]]]
        data = {
            "user_uuid":
                uuid,
            "first_name":
                oneroster_users["givenName"][i],
            "last_name":
                oneroster_users["familyName"][i],
            "email":
                oneroster_users["email"][i].lower()
        }
        users.append(User.parse_obj(data))
    return pd.DataFrame([s.__dict__ for s in users])


def demographics_model(oneroster_demographics, sourceid_2_email, email_2_uuid, ):
    demographics = []
    for i in range(len(oneroster_demographics["sourceId"])):
        uuid = email_2_uuid[sourceid_2_email[oneroster_demographics["sourceId"][i]]]
        data = {
            "user_uuid":
                uuid,
            "birth_date":
                oneroster_demographics["birthDate"][i],
            "sex":
                oneroster_demographics["sex"][i],
            "american_indian_or_alaska_native":
                str(oneroster_demographics["americanIndianOrAlaskaNative"][i]).lower(),
            "asian":
                str(oneroster_demographics["asian"][i]).lower(),
            "black_or_african_american":
                str(oneroster_demographics["blackOrAfricanAmerican"][i]).lower(),
            "native_hawaiian_or_other_pacific_islander":
                str(oneroster_demographics["naitiveHawaiianOrPacificIslander"][i]).lower(),
            "white":
                str(oneroster_demographics["white"][i]).lower(),
            "demographic_race_two_or_more_races":
                str(oneroster_demographics["demographicRaceTwoOrMoreRaces"][i]).lower(),
            "hispanic_or_latino_ethnicity":
                str(oneroster_demographics["hispanicOrLatinoEthnicity"][i]).lower()
        }
        demographics.append(Demographic.parse_obj(data))
    return pd.DataFrame([s.__dict__ for s in demographics])



def make_email2uuid(cli_users):
    mapping = {}
    for user in cli_users:
        mapping[user["email"]] = uuid.uuid4()
    return mapping 


def make_userid2email(cli_users):
    mapping = {}
    for user in cli_users:
        mapping[user["id"]] = user["email"]
    return mapping

def make_sourceid2email(oneroster_users):
    mapping = {}
    for i in range(0, len(oneroster_users['sourceId'])):
        if oneroster_users["sourceId"][i] != "nan":            
            mapping[oneroster_users["sourceId"][i]] = oneroster_users["email"][i]
    return mapping


def create_models(
    output_path, cli_grades, cli_users, oneroster_demographics, oneroster_users, 
):
    sourceid_2_email = make_sourceid2email(oneroster_users)
    userid_2_email = make_userid2email(cli_users)
    email_2_uuid = make_email2uuid(cli_users)

    demographics_df = demographics_model(oneroster_demographics,sourceid_2_email, email_2_uuid)
    users_df = users_model(oneroster_users, sourceid_2_email, email_2_uuid)
    grades_df = grades_model(cli_grades, userid_2_email, email_2_uuid)
    enrollments_df = enrollments_model(cli_users, email_2_uuid)
    courses_df = courses_model(cli_users)
    assessments_df = assessment_model(cli_grades)

    with open(f"{output_path}/demographics.csv", "w") as f:
        demographics_df.to_csv(f, index=False, header=True)
    with open(f"{output_path}/users.csv", "w") as f:
        users_df.to_csv(f, index=False, header=True)
    with open(f"{output_path}/grades.csv", "w") as f:
        grades_df.to_csv(f, index=False, header=True)
    with open(f"{output_path}/enrollments.csv", "w") as f:
        enrollments_df.to_csv(f, index=False, header=True)
    with open(f"{output_path}/courses.csv", "w") as f:
        courses_df.to_csv(f, index=False, header=True)
    with open(f"{output_path}/assessments.csv", "w") as f:
        assessments_df.to_csv(f, index=False, header=True)
    exit()


def collect_HISD_oneroster_data(bucket, key):
    s3_client = boto3.client("s3")
    data = s3_client.get_object(
        Bucket=bucket,
        Key=key
    )
    dfs = {}
    zipfile_data = data["Body"].read()
    zf = ZipFile(BytesIO(zipfile_data))
    for name in zf.namelist():
        if "__MACOSX/" in name:
            continue
        dfs[name] = pd.read_csv(BytesIO(zf.read(name)))

    demographics = dfs["demographics.csv"].to_dict('list')
    users = dfs["users.csv"].to_dict('list')
    return demographics, users


def collect_cli_data(bucket, prefix):
    s3_resource = boto3.resource("s3")
    s3_bucket = s3_resource.Bucket(bucket)
    users, grades = {}, {}
    for object in s3_bucket.objects.filter(Prefix=f"{prefix}/users"):
        users = json.loads(object.get()["Body"].read())
    for object in s3_bucket.objects.filter(Prefix=f"{prefix}/grades"):
        grades = json.loads(object.get()["Body"].read())
    return grades, users


def compile_models(cli_bucket, cli_key, oneroster_bucket, oneroster_key):
    oneroster_demographics, oneroster_users = \
        collect_HISD_oneroster_data(
            oneroster_bucket,
            oneroster_key
            )
    cli_grades, cli_users = collect_cli_data(cli_bucket, cli_key)
    output_path = os.environ["OUTPUT_DIR"]

    create_models(
        output_path,
        cli_grades,
        cli_users,
        oneroster_demographics,
        oneroster_users,
        )


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

    compile_models(
        args.cli_data_bucket,
        args.cli_data_prefix,
        args.oneroster_bucket,
        args.oneroster_key)


if __name__ == "__main__":  # pragma: no cover
    main()
