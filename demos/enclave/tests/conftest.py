import csv
from io import BytesIO
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

        dem_path = str(tmp_path) + "/demographics.csv"
        usr_path = str(tmp_path) + "/users.csv"

        with open(dem_path, "w") as f:
            writer = csv.writer(f)
            key_list = mock_oneroster_demographic_data.keys()
            writer.writerow(key_list)
            limit = len(mock_oneroster_demographic_data['sourceId'])
            for i in range(limit):
                writer.writerow([mock_oneroster_demographic_data[x][i] for x in key_list])
        with open(usr_path, "w") as f:
            writer = csv.writer(f)
            key_list = mock_oneroster_user_data.keys()
            writer.writerow(key_list)
            limit = len(mock_oneroster_user_data['sourceId'])
            for i in range(limit):
                writer.writerow([mock_oneroster_user_data[x][i] for x in key_list])
        
        mem_zip = BytesIO()
        with ZipFile(mem_zip, 'w', compression=ZIP_DEFLATED) as zipF:
            zipF.write(usr_path)
            zipF.write(dem_path)
        
        os.remove(usr_path)
        os.remove(dem_path)
        size = mem_zip.getbuffer().nbytes
        mem_zip.seek(0)
        data = {"Body": StreamingBody(mem_zip, size)}
        return data

    return _builder
