#!/usr/bin/env python3

import json
import argparse
from netmiko import ConnectHandler


def get_interfaces(host, username, password):

    device = {
        "device_type": "cisco_nxos",
        "host": host,
        "username": username,
        "password": password,
    }

    conn = ConnectHandler(**device)

    output = conn.send_command("show interface description | json")

    data = json.loads(output)

    interfaces = []

    rows = data["TABLE_interface"]["ROW_interface"]

    # Handle case where only one interface is returned
    if isinstance(rows, dict):
        rows = [rows]

    for intf in rows:
        interfaces.append({
            "interface": intf.get("interface"),
            "description": intf.get("desc")
        })

    conn.disconnect()

    return interfaces


def main():

    parser = argparse.ArgumentParser(
        description="Return Nexus interface descriptions as JSON"
    )

    parser.add_argument("--host", required=True, help="Switch hostname or IP")
    parser.add_argument("--username", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")

    args = parser.parse_args()

    interfaces = get_interfaces(args.host, args.username, args.password)

    print(json.dumps(interfaces, indent=2))


if __name__ == "__main__":
    main()