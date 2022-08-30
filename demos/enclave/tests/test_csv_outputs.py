import boto3
from botocore.stub import Stubber
from compile_models import main

DEFAULT_SECTION = {"id": "DEFAULT", "title": "Default Section"}


def test_student_columns(mocker, tmp_path, two_person_raw_data):

    zip_bucket_name="sample_bucket"
    zipfile_name = "oneroster.zip"
    zip_key = zip_bucket_name + "/" + zipfile_name
    
    zip_data = two_person_raw_data(tmp_path)

    moodle_bucket_name = "sample_bucket"
    moodle_key = "moodle_files"

    s3_client = boto3.client('s3')
    stubber = Stubber(s3_client)
    stubber.add_response('get_object', zip_data,
                         expected_params={
                            'Bucket': zip_bucket_name,
                            'Key': zip_key
                          }
                         )
    stubber.add_response('get_object', {},
                         expected_params={
                            'Bucket': moodle_bucket_name,
                            'Key': moodle_key
                          }
                         )
    stubber.activate()
    mocker.patch('boto3.client', lambda service: s3_client)

    # A bunch of stuff is done to stub the Boto and Kafka calls

    csv_file_students = "studentData.csv"
    csv_file_assessments = "assessmentData.csv"

    

    mocker.patch(
        "sys.argv",
        ["", moodle_bucket_name, moodle_key, zip_bucket_name, zip_key]
    )
    main()
