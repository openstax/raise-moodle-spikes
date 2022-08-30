import boto3
from botocore.stub import Stubber
from compile_models import main


def test_student_columns(mocker, tmp_path, two_person_raw_data):

    zip_bucket_name="sample_bucket"
    zipfile_name = "oneroster.zip"
    zip_key = zip_bucket_name + "/" + zipfile_name

    zip_data, grades_data, users_data  = two_person_raw_data(tmp_path)

    moodle_bucket_name = "sample_bucket"
    moodle_key = "moodle_files"

    s3_client = boto3.client('s3')
    stubber_client = Stubber(s3_client)
    stubber_client.add_response('get_object', zip_data,
                         expected_params={
                            'Bucket': zip_bucket_name,
                            'Key': zip_key
                          }
                         )

    s3_object = boto3.object('s3')
    stubber_object = Stubber(s3_client)
    stubber_object.add_response('filter', grades_data,
                         expected_params={
                            'Prefix': f'{moodle_key}/users'
                          }
                         )

    stubber_object.add_response('filter', users_data,
                         expected_params={
                            'Prefix': f'{moodle_key}/users'
                          }
                         )
    stubber_client.activate()
    stubber_object.activate()
    mocker.patch('boto3.client', lambda service: s3_client)
    mocker.patch('boto3.object', lambda service: s3_object)

    mocker.patch(
        "sys.argv",
        ["", moodle_bucket_name, moodle_key, zip_bucket_name, zip_key]
    )
    main()
