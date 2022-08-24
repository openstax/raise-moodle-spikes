import csv
import boto3
import botocore.stub
import pytest
from enclave.compile_models import main

def test_student_columns(mocker, tmp_path):

    s3_client = boto3.client('s3')
    stubber = botocore.stub.Stubber(s3_client)
    stubber.add_response('put_object', {},
                         expected_params={
                            'Body': botocore.stub.ANY,
                            'Bucket': bucket_name,
                            'Key': full_key1,
                            'ContentType': 'application/json'
                          }
                         )

    # A bunch of stuff is done to stub the Boto and Kafka calls

    csv_file_students = "studentData.csv"
    csv_file_assessments = "assessmentData.csv"

    mocker.patch(
        "sys.argv",
        ["", str(input_csv_path), str(output_path), resource_url_prefix]
    )

    main()


    
