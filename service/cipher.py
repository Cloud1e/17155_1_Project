def encrypt(inputText, D):
    N = 3
    valid_start = 34
    valid_end = 126
    reversedText = inputText[::-1]
    encryptedText = ''
    for char in reversedText:
        if char in [' ', '!']:
            encryptedText += char
        else:
            new_char = ord(char) + N * D
            if new_char > valid_end:
                new_char = valid_start + (new_char - valid_end - 1)
            elif new_char < valid_start:
                new_char = valid_end - (valid_start - new_char - 1)
            encryptedText += chr(new_char)
    return encryptedText

def decrypt(encryptedText, D):
    return encrypt(encryptedText, -D)