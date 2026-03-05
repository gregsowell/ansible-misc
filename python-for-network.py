#!/usr/bin/env python3

import json
import argparse
import paramiko


def run_command(host, username, password, command):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        hostname=host,
        username=username,
        password=password,
        look_for_keys=False,
        allow_agent=False
    )

    stdin, stdout, stderr = client.exec_command(command)

    output = stdout.read().decode()
    client.close()

    return output


def get_interfaces(host, username, password):

    command = "show interface description | json"
    output = run_command(host, username, password, command)

    data = json.loads(output)

    rows = data["TABLE_interface"]["ROW_interface"]

    if isinstance(rows, dict):
        rows = [rows]

    interfaces = []

    for i in rows:
        interfaces.append({
            "interface": i.get("interface"),
            "description": i.get("desc")
        })

    return interfaces


def main():

    parser = argparse.ArgumentParser(
        description="Return Nexus interface descriptions as JSON"
    )

    parser.add_argument("--host", required=True, help="Switch hostname or IP")
    parser.add_argument("--username", required=True, help="Username")
    parser.add_argument("--password", required=True, help="Password")

    args = parser.parse_args()

    interfaces = get_interfaces(
        args.host,
        args.username,
        args.password
    )

    print(json.dumps(interfaces, indent=2))


if __name__ == "__main__":
    main()