from pyspark.sql import SparkSession
import os
import json
import csv
import io
import boto3

SPARK_APP_NAME = "Research data analyzer"
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_DATA_PREFIX = os.environ.get("S3_DATA_PREFIX")
S3_RESULT_PREFIX = os.environ.get("S3_RESULT_PREFIX")


def graded_students(data):
    events = data[1]
    for event in events:
        if event["eventname"] == "\\core\\event\\user_graded":
            return True
    return False


def viewed_desmos(data):
    events = data[1]
    for event in events:
        if event["eventname"] == "\\mod_lesson\\event\\content_page_viewed" \
                and event["page_title"] == "Desmos activity":
            return True
    return False


def viewed_phet(data):
    events = data[1]
    for event in events:
        if event["eventname"] == "\\mod_lesson\\event\\content_page_viewed" \
                and event["page_title"] == "PHET activity":
            return True
    return False


def passed_quiz(data):
    events = data[1]
    for event in events:
        if event["eventname"] == "\\core\\event\\user_graded":
            grade = float(event["grade"])
            return grade >= 70.0
    raise Exception("No grade event for quiz!")


def main():
    # Configure SparkSession
    spark = SparkSession \
        .builder \
        .appName(SPARK_APP_NAME) \
        .getOrCreate()

    s3Rdd = spark.sparkContext.textFile(
        f"s3a://{S3_BUCKET}/{S3_DATA_PREFIX}/*"
    )

    # Get events for the lesson we care about
    events = s3Rdd.map(lambda event: json.loads(event))\
        .filter(lambda event: event["course_name"] == "RAISE Algebra 1" and
                event["lesson_name"] == "Demo lesson")
    events_by_user = events.groupBy(lambda event: event["username"])
    events_by_graded_user = events_by_user.filter(graded_students)
    users_viewed_desmos = events_by_graded_user.filter(viewed_desmos)
    users_viewed_phet = events_by_graded_user.filter(viewed_phet)
    users_desmos_passed = users_viewed_desmos.filter(passed_quiz)
    users_phet_passed = users_viewed_phet.filter(passed_quiz)
    desmos_activity_count = users_viewed_desmos.count()
    phet_activity_count = users_viewed_phet.count()
    desmos_passed_count = users_desmos_passed.count()
    phet_passed_count = users_phet_passed.count()

    output = io.StringIO()
    data = []
    data.append({
        "Page": "Desmos activity",
        "Views": desmos_activity_count,
        "Quiz passes": desmos_passed_count,
        "Pass probability": desmos_passed_count / desmos_activity_count
    })
    data.append({
        "Page": "Phet activity",
        "Views": phet_activity_count,
        "Quiz passes": phet_passed_count,
        "Pass probability": phet_passed_count / phet_activity_count
    })
    writer = csv.DictWriter(
        output,
        fieldnames=["Page", "Views", "Quiz passes", "Pass probability"]
    )
    writer.writeheader()
    writer.writerows(data)

    s3_client = boto3.client('s3')
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=f"{S3_RESULT_PREFIX}/report.csv",
        Body=output.getvalue()
    )


if __name__ == "__main__":
    main()
