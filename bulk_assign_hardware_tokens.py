# This script can be used to bulk assign tokens to users based on the data contained within a .CSV file. Both the tokens and users need to be already in Duo.

import duo_client
from datetime import datetime
import csv
from my_duo_keys import DUO_IKEY, DUO_SKEY, DUO_APIHOSTNAME

# Initialize Duo Admin API
admin_api = duo_client.Admin(
    ikey=DUO_IKEY,
    skey=DUO_SKEY,
    host=DUO_APIHOSTNAME
)

def get_current_time():
    now = datetime.now()
    return now.strftime('%d-%m-%Y %H:%M:%S')

def assign_tokens(csv_filename):
    print("\n-------------------------------------------------------------------")
    print("************ ASSIGNING HARDWARE TOKENS ************")
    print(f"Time Started: {get_current_time()}")
    print("-------------------------------------------------------------------")

    success = 0
    failed = 0

    with open(csv_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        for count, row in enumerate(reader, start=1):
            tokenserial, username, tokentype = row[:3]

            try:

                user_id = admin_api.get_users_by_name(username=username)[0]['user_id']
                token_id = admin_api.get_tokens_by_serial(type=tokentype, serial=tokenserial)[0]['token_id']
                admin_api.add_user_token(user_id=user_id, token_id=token_id)

                print(f"({count}) SN: {tokenserial} | User: {username} ...SUCCESS!")
                success += 1
            except Exception as e:
                print(f"({count}) SN: {tokenserial} | User: {username} ...FAILED!")
                failed += 1

    print("\n-------------------------------------------------------------------")
    print(f"Tokens Successfully Assigned: {success}")
    if failed > 0:
        print(f"Tokens Failed to be Assigned: {failed}")
        print("** Please check username or SN for errors.")
    print(f"Time Finished: {get_current_time()}")
    print("-------------------------------------------------------------------")

if __name__ == "__main__":
    csv_filename = 'token_assign.csv'
    assign_tokens(csv_filename)
