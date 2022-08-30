import csv
from io import BytesIO
import json
import pytest
import os
from zipfile import ZipFile, ZIP_DEFLATED
from botocore.response import StreamingBody


@pytest.fixture
def two_person_raw_data():
    def _builder(tmp_path):
        mock_oneroster_demographic_data = {
            "sourceId": ["u100", "u101"],
            "birthDate": ["2008-01-02", "2007-12-01"],
            "sex": ["male", "female"],
            "americanIndianOrAlaskaNative": ["false", "false"],
            "asian": ["true", "false"],
            "blackOrAfricanAmerican": ["false", "true"],
            "naitiveHawaiianOrPacificIslander": ["false", "false"],
            "white": ["false", "false"],
            "demographicRaceTwoOrMoreRaces": ["false", "false"],
            "hispanicOrLatinoEthnicity": ["false", "false"]
        }

        mock_oneroster_user_data = {
            "sourceId": ["u100", "u101"],
            "givenName": ["Craig", "Yolanda"],
            "familyName": ["Johnston", "Guitierrez"],
            "email": ["cjohnston@yahoo.com", "yolanda@gmail.com"]
        }

        mock_cli_grades_data = {
            "usergrades": [
                {
                    "courseid": 2,
                    "gradeitems": [
                        {
                            "id": 16,
                            "itemname": "Unit 1, Section A Quiz"
                        }
                    ]
                }
            ]
        }

        mock_cli_user_data = [
            {
                "email": "davidtucci13431@gmail.us",
                "enrolledcourses": [
                    {
                        "fullname": "Algebra 1 (Research Dev)",
                        "id": 2,
                        "shortname": "Alg1"
                    }
                ],
                "firstname": "David",
                "fullname": "David Tucci",
                "id": 7,
                "lastname": "Tucci",
                "roles": [
                    {
                        "roleid": 5,
                        "shortname": "student"
                    }
                ]
            }
        ]

        dem_path = str(tmp_path) + "/demographics.csv"
        with open(dem_path, "w") as f:
            writer = csv.writer(f)
            key_list = mock_oneroster_demographic_data.keys()
            writer.writerow(key_list)
            limit = len(mock_oneroster_demographic_data['sourceId'])
            for i in range(limit):
                writer.writerow([mock_oneroster_demographic_data[x][i] for x in key_list])

        usr_path = str(tmp_path) + "/users.csv"
        with open(usr_path, "w") as f:
            writer = csv.writer(f)
            key_list = mock_oneroster_user_data.keys()
            writer.writerow(key_list)
            limit = len(mock_oneroster_user_data['sourceId'])
            for i in range(limit):
                writer.writerow([mock_oneroster_user_data[x][i] for x in key_list])

        grades_path = str(tmp_path) + "/grades/2.json"
        os.mkdir(str(tmp_path) + "/grades")
        with open(grades_path, "w") as f:
            json.dump(mock_cli_grades_data, f)

        users_path = str(tmp_path) + "/users/2.json"
        os.mkdir(str(tmp_path) + "/users")
        with open(users_path, "w") as f:
            json.dump(mock_cli_user_data, f)

        mem_zip = BytesIO()
        with ZipFile(mem_zip, 'w', compression=ZIP_DEFLATED) as zipF:
            zipF.write(usr_path)
            zipF.write(dem_path)

        os.remove(usr_path)
        os.remove(dem_path)

        size = mem_zip.getbuffer().nbytes
        mem_zip.seek(0)
        zip_data = {"Body": StreamingBody(mem_zip, size)}
        
        with open(f'{str(tmp_path)}/grades/2.json', "r") as f:
            grades_data = [{"Body": StreamingBody(f.read(), size)}]

        with open(f'{str(tmp_path)}/users/2.json', "r") as f:
            users_data = [{"Body": StreamingBody(f.read(), size)}]

        return zip_data, grades_data, users_data

    return _builder
