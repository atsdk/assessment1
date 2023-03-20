import argparse
import os
import requests
import time


parser = argparse.ArgumentParser(description="Get patient data files folder")
parser.add_argument(
    "--folder",
    type=str,
    help="Folder where FHIR json files for test are stored",
    default="test_data",
)

url = "http://127.0.0.1:8000/api/v1/patient-data"
token = "bearer test-token"


def test_all_files_upload(folder):
    # iteratate over all files in the ./test_data directory
    for filename in os.listdir(f"{folder}"):
        file = {"file": open(f"{folder}/{filename}", "rb")}
        resp = requests.post(
            url=url, files=file, headers={"Authorization": token}
        )
        print(f"Response: {resp.status_code} {resp.json()}\n")


if __name__ == "__main__":
    args = parser.parse_args()
    start = time.time()
    test_all_files_upload(args.folder)
    end = time.time()
    print(f"Total time: {end - start}")
