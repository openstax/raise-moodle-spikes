import argparse
import boto3
import json
import csv
from pathlib import Path
from datetime import datetime, timedelta


def get_user_json_by_course(s3_bucket, user_data_prefix):
    json_data = {}

    s3_client = boto3.client("s3")
    data_objects = s3_client.list_objects(
        Bucket=s3_bucket,
        Prefix=user_data_prefix
    )
    for data_object in data_objects.get("Contents"):
        object_key = data_object.get("Key")
        course_id = object_key.split("/")[-1].split(".json")[0]

        data = s3_client.get_object(
            Bucket=s3_bucket,
            Key=object_key
        )
        contents = data["Body"].read()
        json_data[course_id] = json.loads(contents)

    return json_data


def get_course_name(course_id, users_data):
    # We should be able to find the target course in any user, so the
    # first is as good as any
    enrolled_courses = users_data[0]["enrolledcourses"]
    for course in enrolled_courses:
        if str(course["id"]) == course_id:
            return course["fullname"]

    raise Exception(
        f"Could not find course name for {course_id} in {enrolled_courses}"
    )


def get_enrolled_students(users_data):
    enrolled_students = 0
    for user in users_data:
        # Based on inspection, even if users have different roles across
        # multiple courses, since we query by course this seems to be always
        # length 1 with the course-specific role
        user_role = user["roles"][0]["shortname"]
        if user_role == "student":
            enrolled_students += 1
    return enrolled_students


def get_wau(users_data):
    wau = 0
    for user in users_data:
        # This is a unix timestamp or 0
        lastaccess = user["lastcourseaccess"]
        time_since_access = datetime.now() - datetime.fromtimestamp(lastaccess)
        if time_since_access < timedelta(days=7):
            wau += 1
    return wau


def run_analysis(s3_bucket, user_data_prefix):
    users_by_course = get_user_json_by_course(s3_bucket, user_data_prefix)
    result_data = []

    for course_id, users_data in users_by_course.items():
        course_name = get_course_name(course_id, users_data)
        enrolled_students = get_enrolled_students(users_data)
        wau = get_wau(users_data)
        result_data.append({
            "course_id": course_id,
            "course_name": course_name,
            "enrolled_students": enrolled_students,
            "weekly_active_users": wau
        })

    return result_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("s3_bucket", type=str)
    parser.add_argument("user_data_prefix", type=str)
    parser.add_argument("output_csv", type=str)

    args = parser.parse_args()

    output_csv_file = Path(args.output_csv)
    output_data = run_analysis(
        args.s3_bucket,
        args.user_data_prefix
    )

    with open(output_csv_file, "w") as output_file:
        writer = csv.DictWriter(
            output_file,
            output_data[0].keys()
        )
        writer.writeheader()
        writer.writerows(output_data)


if __name__ == "__main__":
    main()
