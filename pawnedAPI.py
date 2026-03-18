import requests
import hashlib

def pawned(hash):
    url = f"https://api.pwnedpasswords.com/range/{hash[:5]}"
    params = {
        'Add-Padding': True,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.text.splitlines()

        for line in data:
            suffix = hash[5:]
            api_suffix, count = line.split(':')

            if api_suffix == suffix.upper():
                return int(count)

        return 0
    except requests.exceptions.RequestException as e:
        print("error")
        return e

def hash_string(s):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(s.encode('utf-8'))
    return sha1_hash.hexdigest()

def main():
    password = "password"
    hash = hash_string(password)
    breached = pawned(hash)

    if breached != 0:
        print(f"{breached}")


main()
