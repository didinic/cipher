from collections import Counter
from typing import Optional

def encode_caesar(plaintext: str, shift: int) -> str:
    result = []
    for char in plaintext:
        if char.isalpha():
            o = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - o + shift) % 26 + o))
        else:
            result.append(char)
    return ''.join(result)

def decode_caesar(ciphertext: str, shift: int) -> str:
    return encode_caesar(ciphertext, -shift % 26)

ENGLISH_FREQ_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

def score_text(text: str) -> int:
    letters = [c.upper() for c in text if c.isalpha()]
    if not letters:
        return 0
    count = Counter(letters)
    freq_order = ''.join([c for c, _ in count.most_common()])
    return sum(l in ENGLISH_FREQ_ORDER[:6] for l in freq_order[:6])

def auto_decode_caesar(ciphertext: str) -> (str, int): # type: ignore
    best_score = -1
    best_plain = ciphertext
    best_shift = 0
    for shift in range(26):
        candidate = decode_caesar(ciphertext, shift)
        s = score_text(candidate)
        if s > best_score:
            best_score = s
            best_plain = candidate
            best_shift = shift
    return best_plain, best_shift