import json
from pathlib import Path


def prepare_json_credentials(name):
    with open(f"keys/raw/{name}.sh") as reader:
        lines = reader.readlines()

    headers = {}
    cookies = {}
    for line in lines:
        if not line.strip().startswith("-H"):
            continue
        key, value = line.strip()[4:-3].split(": ")
        if key.lower() == "cookie":
            for cookie in value.split("; "):
                key, value = cookie.split("=", 1)
                cookies[key] = value
        else:
            headers[key] = value

    location = "keys/credentials"
    Path(location).mkdir(parents=True, exist_ok=True)

    secrets = {"headers": headers, "cookies": cookies}
    with open(f"{location}/{name}.json", "w") as writer:
        writer.write(json.dumps(secrets, indent=4))


def read_json_credentials(name):
    with open(f"keys/credentials/{name}.json") as reader:
        credentials = json.loads(reader.read())
    return credentials
