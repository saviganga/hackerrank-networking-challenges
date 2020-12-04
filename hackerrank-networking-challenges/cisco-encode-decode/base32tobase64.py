'''
QUESTION
To ship data across a network various encoding formats are used; one such router in Cisco gets data in Base32 encoded format. The router has to then transfer the data, converting it to Base64.

Your task is to write a code that converts Base32 encoded strings to Base64.

Note Encoding has to be manually written, and use of such an external library will lead to disqualification.
''' 



#base32 charset
base32_charset = {'a': 0, 'b': 1, 'c': 2, 'd':3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25, '2': 26, '3': 27, '4': 28, '5': 29, '6': 30, '7': 31,}

#base64 charset
base64_charset = {'A': 0, 'B': 1, 'C': 2, 'D':3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25, 'a': 26, 'b': 27, 'c': 28, 'd': 29, 'e': 30, 'f': 31, 'g': 32, 'h': 33, 'i': 34, 'j': 35, 'k': 36, 'l': 37, 'm': 38, 'n': 39, 'o': 40, 'p': 41, 'q': 42, 'r': 43, 's': 44, 't': 45, 'u': 46, 'v': 47, 'w': 48, 'x': 49, 'y': 50, 'z': 51, '0': 52, '1': 53, '2': 54, '3': 55, '4': 56, '5': 57, '6': 58, '7': 59, '8': 60, '9': 61, '+': 62, '/': 63, '=': '$'}

#splits a list into chunks
def splitList(List, chunk_size):
    return [List[a:a+chunk_size] for a in range(0, len(List), chunk_size)]

#splits a string into chunks
def splitstring(String, size):
    return [[String[a:a+size]] for a in range(0, len(String), size)]


#decodes base 32 strings to english
def decode_base32(base32_string):

    base32string = base32_string.lower()

    #map to base32_charset
    base32_alphabet = [base32_charset[i] for i in base32string if i in base32_charset]

    #convert the values to binary 
    for i in range(len(base32_alphabet)):
        base32_alphabet[i] = bin(base32_alphabet[i]).replace('0b', '')

    #with 5 bits
        if len(base32_alphabet[i])<5:
            y = 5 - len(base32_alphabet[i])
            base32_alphabet[i] = '0'*y + base32_alphabet[i]
        elif len(base32_alphabet[i])>5:
            y = len(base32_alphabet[i]) - 5
            base32_alphabet[i] = base32_alphabet[i].lstrip('0'*y)
        else:
            base32_alphabet[i] = base32_alphabet[i]

    #group into 8 'five bit' blocks
    fivebitblocks = splitList(base32_alphabet, 8)
    eightbitblocks_build = [[''.join(a)] for a in fivebitblocks]
    eightbitblocks = [ splitstring(b[0], 8) for b in eightbitblocks_build ]

    #convert the 8 bit binary to decimal
    decoded_string_list = []
    for c in eightbitblocks:
        for d in c:
            d[0] = int(d[0], 2)

    #map decimal to ascii characters
            decoded_string_list.append(chr(d[0]))

    #return result
    decoded_string = ''.join(decoded_string_list)
    return decoded_string



#encodes an english string to base 64
def encode_base64(human_string):

    #break the string into groups of 3
    grouped_string = splitstring(human_string, 3)

    #get 8 bit binary equivalent of each group (using ascii values)
    grouped_string_ascii = []
    for r in grouped_string:
        grouped_string_ascii_rows = []
        for c in r:
            for letter in c:
                grouped_string_ascii_rows.append(bin(ord(letter)).replace('0b', '0'))
        grouped_string_ascii.append(grouped_string_ascii_rows)

    #get 24 bit binary of each group
    twentyfourbitblock = [[''.join(group)] for group in grouped_string_ascii]

    #break down 24 bits into six bit chunks
    sixbitchunks = [splitstring(bits, 6) for blk in twentyfourbitblock for bits in blk]

    #complete the incomplete chunks (make them 6)
    for chunk in sixbitchunks:
        for ch in chunk:
            if len(ch[0]) < 6:
                rem = 6 - len(ch[0])
                ch[0] = ch[0] + '0'*rem

    #convert the bits to decimal
    for chh in sixbitchunks:
        for chhh in chh:
            chhh[0] = int(chhh[0], 2)

    #complete the incomplete blocks (make them 4)
        if len(chh) < 4:
            rems = 4 - len(chh)
            chh.extend([['=']]*rems)

    #map the decimal value to the base64 charset dictionary
        for rr in chh:
            for key, val in base64_charset.items():
                if rr[0] == val:
                    rr[0] = key

    #return the result
    base64_str_list = [zzz for z in sixbitchunks for zz in z for zzz in zz]
    base64_str = ''.join(base64_str_list)
    return base64_str



if __name__ == "__main__":
    base32_str = input('\nEnter base 32 string: ')
    dec = decode_base32(base32_str)
    print(f'decoded base 32 string: {dec}')
    enc = encode_base64(dec)
    print(f'encoded base 64 string: {enc}')