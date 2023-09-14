import duo_client
from my_duo_keys import DUO_IKEY, DUO_SKEY, DUO_APIHOSTNAME  # Import your Duo API credentials

# Initialize Duo Admin API
admin_api = duo_client.Admin(
    ikey=DUO_IKEY,
    skey=DUO_SKEY,
    host=DUO_APIHOSTNAME
)
def list_integrations():
    try:
        limit = 100  # Adjust the limit as needed to retrieve integrations in batches
        offset = 0

        while True:
            integrations = admin_api.get_integrations(limit=limit, offset=offset)
            if not integrations:
                break

            print("Integration IDs and Names:")
            for integration in integrations:
                print(f"{integration['integration_key']}: {integration['name']}")

            offset += limit

    except Exception as e:
        print(f"Error listing integrations: {str(e)}")

def delete_integration(integration_key):
    try:
        admin_api.delete_integration(integration_key)
        print(f"Integration with ID {integration_key} has been deleted.")
    except Exception as e:
        print(f"Error deleting integration: {str(e)}")

def main():
    list_integrations()
    
    while True:
        integration_keys = input("Enter the integration IDs to delete (separated by spaces): ").strip()
        if not integration_keys:
            print("No integration IDs provided. Exiting.")
            return
        
        integration_keys = integration_keys.split()  # Split Integration IDs by spaces
        for integration_key in integration_keys:
            delete_integration(integration_key.strip())

        continue_deletion = input("Do you want to delete another integration? (yes/no): ").strip().lower()
        if continue_deletion != 'yes':
            break

if __name__ == "__main__":
    main()
