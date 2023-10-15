# Python and Cloudflare

## DNS record updating
In an attempt to create or update a DNS record, I created a python script to help with this.

There are some requirements.

There needs to be a `cf-info.json` file with the following details in it:
```json
{
    "api_token": "",
    "zone_id": "",
    "domain_name": ""
}
```
* `api_token` is the Cloudflare Token used to update.
* `zone_id` is the zone id for the zone that will be updated.
* `domain_name` is the name of the domain name.

Usage:
```bash
$ python3 cf-dns-record.py -h
usage: cf-dns-record.py [-h] [--hostname HOSTNAME] [--value VALUE]

Update Cloudflare DNS Record

optional arguments:
  -h, --help           show this help message and exit
  --hostname HOSTNAME  Type of DNS record to be created/updated.
  --value VALUE        Value of Record
``` 

It's important to note that the hostname does not include the actual `domain_name` field from the json file.

Here's an example:
To create the entry `another_host.example.com` to point to `1.1.1.1`.
```bash
$ python3 cf-dns-record.py --hostname another_host --value 1.1.1.1
DNS record for 'another_host.example.com' created with IP address 1.1.1.1.
```

To update an existing entry `another_host.example.com` to point to 1.1.1.2.
```bash
$ python3 cf-dns-record.py --hostname another_host --value 1.1.1.2
DNS record for 'another_host.rockingtheplanet.com' updated.
```
