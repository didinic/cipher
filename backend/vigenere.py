def vigenere_encode(plaintext: str, key: str) -> str:
    """Encode plaintext using the Vigenere cipher."""
    key = key.upper()
    result = []
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            encoded_char = chr((ord(char) - base + shift) % 26 + base)
            result.append(encoded_char)
            key_index += 1
        else:
            result.append(char)  # Non-alpha characters pass through unchanged

    return ''.join(result)


def vigenere_decode(ciphertext: str, key: str) -> str:
    """Decode ciphertext using the Vigenere cipher."""
    key = key.upper()
    result = []
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            decoded_char = chr((ord(char) - base - shift) % 26 + base)
            result.append(decoded_char)
            key_index += 1
        else:
            result.append(char)

    return ''.join(result)