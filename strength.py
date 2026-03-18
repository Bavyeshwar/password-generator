import math
import string
import hashlib
import requests

def strength(password):
    size = 0
    hash = hash_string(password)

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    punctuation = string.punctuation
    digits = string.digits
    if any(char in lower for char in password): size += len(lower)
    if any(char in upper for char in password): size += len(upper)
    if any(char in digits for char in password): size += len(digits)
    if any(char in punctuation for char in password): size += len(punctuation)

    strength = (math.log2(size ** len(password)))
    if pawned(hash): strength = strength - 50.0

    R = 94
    L = 20
    BENCHMARK = (math.log2(R ** L))

    percentage = int((strength / BENCHMARK) * 100)


    return min(100, max(0, percentage))

def hash_string(s):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(s.encode('utf-8'))
    return sha1_hash.hexdigest()

def pawned(hash):
    url = f"https://api.pwnedpasswords.com/range/{hash[:5]}"
    params = {
        'Add-Padding': True,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.text.splitlines()
        suffix = hash[5:].upper()

        for line in data:
            api_suffix = line.split(':')[0]

            if api_suffix == suffix:
                return True
        return False
    except requests.exceptions.RequestException as e:
        print("error")
        return e


def main():
    print(f"{strength("j[d(#1-]*)$=")}%")


main()
