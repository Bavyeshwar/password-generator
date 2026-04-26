import string
import secrets
from xkcdpass import xkcd_password as xp

MNEMONIC_PHRASES = [
   " spotted a ",
   " jumped over the ",
   " talked to a ",
   " hid behind a "
]
MNEMONIC_CONJUNCTIONS = [
   " while a ",
   " then  a ",
   " because the ",
   " and suddenly a "
]
def generate_mnemonic(length):
   connectors = ['-', '', '|', '_']
   for i in range(4):
      for j in range(1, 4):
         connectors.append(f"{connectors[i] * j}")
   connector = secrets.choice(connectors)
    
   pw = xp.generate_xkcdpassword(xp.generate_wordlist(xp.locate_wordfile(), min_length=5, max_length=8), numwords=length, delimiter=connector)

   words = [word for word in pw.split(connector)]
   mnemonic = words[0].capitalize()
   for i in range(1, len(words)):
      mnemonic += secrets.choice(MNEMONIC_CONJUNCTIONS) if i % 3 == 0 else secrets.choice(MNEMONIC_PHRASES)
      mnemonic += words[i].lower()
   return {"mnemonic": mnemonic, "pw": pw}
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
