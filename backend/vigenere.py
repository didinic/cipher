def vigenere_encode(plaintext, key, encode):
    key = key.upper()
    result = []
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            if encode:
                result_char = chr((ord(char) - base + shift) % 26 + base)
            else:
                result_char = chr((ord(char) - base - shift) % 26 + base)
            result.append(result_char)
            key_index += 1
        else:
            result.append(char)

    return ''.join(result)
