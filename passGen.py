import string
import secrets

EXCLUDE = ['\\', '\'', '"', ',', '.', '<', '>', '[', ']', '{', '}', '`', '~', ';', '/', ':', '|', '&']
RARE_PUNCT = ['.', '>', '<', '~', '[', ']', ':', '|', '&']

def transform(phrase):
    words = phrase.split()
    letters = []
    for word in words:
        for letter in word: letters.append(letter)
    exclude = ['"', '\'', '\\', '<', '>', '/', '?', ',', '.', '`', '~', ']', '[', '}', '{', ';']
    pool = [char for char in string.punctuation if char not in exclude]
    for char in string.digits: pool.append(char)
    subs = {
        'A': '@',
        'E': '3',
        'H': '|-|',
        'I': '!',
        'L': '|_',
        'O': '0',
        'S': '$',
        'V': '\\/'
    }

    password = []
    for i in range(secrets.randbelow(5)): password.append(secrets.choice(pool))

    for letter in letters:
        uppercase = letter.upper()
        if uppercase in subs.keys():
            password.append(subs[uppercase])
        else:
            password.append(secrets.choice([uppercase, uppercase.lower()]))

    min = 15
    while sum(1 for _ in password) < min:
        extra = secrets.choice(pool)
        if extra not in password: password.append(extra)

    return "".join(password)
def generate(punct, extra_punct, uppercase, lowercase, digits, length):
    if not isinstance(punct, bool) or not isinstance(extra_punct, bool) or not isinstance(uppercase, bool) or not isinstance(lowercase, bool) or not isinstance(digits, bool) or not isinstance(length, int): return -1

    pool = []
    if uppercase == True:
        pool.append(string.ascii_uppercase)
    if lowercase == True:
        pool.append(string.ascii_lowercase)
    if digits == True:
        pool.append(string.digits)
    if punct == True or extra_punct == True:
        pool.append(''.join([char for char in string.punctuation if char not in EXCLUDE]))
        if extra_punct == True: pool.append(''.join(RARE_PUNCT))
    return ''.join([secrets.choice(''.join(pool)) for _ in range(length)])
