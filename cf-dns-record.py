# Author:                    TheScriptGuy
# Version:                   0.01
# Description:               A python script to create/update a cloudflare DNS record.

import requests
import argparse
import os
import sys
import json

class CloudflareInfo:
    """Manage Cloudflare information and authentication headers."""

    def __init__(self, file_path=None):
        self.api_token = ""
        self.api_base_url = "https://api.cloudflare.com/client/v4"
        self.zone_id = ""
        self.domain_name = ""
        self.api_auth_headers = {
            "Authorization": "",
            "Content-Type": "application/json"
        }

        if file_path:
            self.load_from_file(file_path)

    def load_from_file(self, file_path: str) -> None:
        """Load Cloudflare information from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Raises:
            FileNotFoundError: If the specified file is not found.
            json.JSONDecodeError: If the file does not contain valid JSON.
        """
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {file_path}") from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError("Invalid JSON format.", e.doc, e.pos) from e
        
        self.api_token = data.get('api_token', "")
        self.zone_id = data.get('zone_id', "")
        self.domain_name = data.get('domain_name', "")
        self._update_auth_header()

    def _update_auth_header(self):
        """Update the Authorization field in the API authentication headers."""
        self.api_auth_headers["Authorization"] = f"Bearer {self.api_token}"


def parseArguments():
    """
    Create argument options and parse through them to determine what to do with script.
    """

    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Update Cloudflare DNS Record')

    # Optional arguments
    parser.add_argument('--hostname', default='',
                        help='Type of DNS record to be created/updated.')


    parser.add_argument('--value', default='',
                        help='Value of Record')

    global args
    args = parser.parse_args()


def updateCloudflareDNS(__hostname: str, __ipAddress: str) -> None:
    """Update Cloudflare DNS zone rockingtheplanet.com with the IP address that was created from the container."""
    # Define a cloudflare_info instance
    cf_info = CloudflareInfo('cf-info.json')

    # Set your Cloudflare API token, zone ID, domain name, and public IP addresses
    domain_name = f'{__hostname}.{cf_info.domain_name}'

    # Get the DNS records for the domain
    response = requests.get(f"{cf_info.api_base_url}/zones/{cf_info.zone_id}/dns_records", headers=cf_info.api_auth_headers)
    dns_records = response.json()["result"]

    # Find the existing DNS record, if any
    existing_record = None
    for record in dns_records:
        if record["name"] == domain_name:
            existing_record = record
            break

    # Update or create the DNS record with the public IP addresses
    if existing_record:
        # Update the existing DNS record
        record_id = existing_record["id"]
        response = requests.put(
            f"{cf_info.api_base_url}/zones/{cf_info.zone_id}/dns_records/{record_id}",
            headers=cf_info.api_auth_headers,
            json={
                "type": "A",
                "name": domain_name,
                "content": __ipAddress,
                "proxied": False
            }
        )
        print(f"DNS record for '{domain_name}' updated.")
    else:
        # Create a new DNS record
        response = requests.post(
            f"{cf_info.api_base_url}/zones/{cf_info.zone_id}/dns_records",
            headers=cf_info.api_auth_headers,
            json={
                "type": "A",
                "name": domain_name,
                "content": __ipAddress,
                "proxied": False
            }
        )
        print(f"DNS record for '{domain_name}' created with IP address {__ipAddress}.")


def main():
    """Main definition."""
    parseArguments()
    if (args.hostname != '') and (args.value != ''):
        updateCloudflareDNS(args.hostname, args.value)
    else:
        print('Invalid arguments provided.')
        sys.exit(1)


if __name__ == '__main__':
    try:
        
        main()

    except KeyboardInterrupt:
        print('Interrupted')
        print
        try:
            sys.exit(0)
        except SystemExit:
            os.exit(0)
