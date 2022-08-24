import json
import boto3
import argparse
import pandas as pd
from io import BytesIO
from zipfile import ZipFile

MODEL_FILE_USERS = "users.csv"
MODEL_FILE_COURSES = "courses.csv"
MODEL_FILE_ONEROSTER_DEMOGRAPHICS = "oneroster_demographics.csv"
MODEL_FILE_ENROLLMENTS = "enrolments.csv"
MODEL_FILE_ASSESSMENTS = "assessments.csv"
MODEL_FILE_GRADES = "grades.csv"


RAW_CLI_DATA_GRADES = 'grades/'
RAW_CLI_DATA_USERS = 'users/'


def create_student_model():
    pass


def create_grade_item_model():
    pass


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

    demographics = dfs["demographics.csv"]
    users = dfs["users.csv"]
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
    one_rosterdemographics, oneroster_users = \
        collect_HISD_oneroster_data(
            oneroster_bucket,
            oneroster_key
            )
    grades, users = collect_cli_data(cli_bucket, cli_key)


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
