# The following Python script can be used to bulk import Yubikeys from a .csv file to Duo.

import duo_client
import csv
import json
from my_duo_keys import DUO_IKEY, DUO_SKEY, DUO_APIHOSTNAME

# Initialize Duo Admin API
admin_api = duo_client.Admin(
    ikey=DUO_IKEY,
    skey=DUO_SKEY,
    host=DUO_APIHOSTNAME
)

def add_yubikey_token(serial, private_id, aes_key):
    try:
        # Add a single YubiKey token
        response = admin_api.add_yubikey_token(
            serial=serial,
            private_id=private_id,
            aes_key=aes_key
        )

        # Print the JSON response for inspection
        print("JSON Response:")
        print(json.dumps(response, indent=4))  # Pretty-print the JSON response

        token_id = response.get("token_id")
        if token_id:
            print(f"Added YubiKey Token with Serial: {serial} successfully. Token ID: {token_id}")
        else:
            print(f"Failed to add YubiKey Token with Serial: {serial}")
            if "message" in response:
                print(f"Error Message: {response['message']}")

    except Exception as e:
        print(f"An error occurred while adding a YubiKey token: {str(e)}")

def bulk_add_yubikey_tokens(csv_filename):
    try:
        # Read the CSV file and add YubiKey tokens one by one
        with open(csv_filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                tokenserial = row["token_serial"]
                private_id = row["private_id"]
                aes_key = row["aes_key"]

                add_yubikey_token(tokenserial, private_id, aes_key)

    except Exception as e:
        print(f"An error occurred while adding YubiKey tokens: {str(e)}")

if __name__ == "__main__":
    csv_filename = 'csv_tokenfile.csv'
    bulk_add_yubikey_tokens(csv_filename)
