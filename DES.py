# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from operation import IpPermutation, InverseIpPermutation, ExtendPermutation, \
                      CreateSubKeys, SBoxPermutation, PBoxPermutation, \
                      string2bin, bin2string, xor


def cipher(message, key, mode='encrypt'):
    message = string2bin(message)
    key = string2bin(key)

    subkeys = CreateSubKeys(key) if mode == 'encrypt' else CreateSubKeys(key)[::-1]
    text = IpPermutation(message)

    for i in range(16):
        l, r = text[:32], text[32:]
        r_extend = ExtendPermutation(r)
        xor1 = xor(r_extend, subkeys[i])
        s_box_result = SBoxPermutation(xor1)
        p_box_result = PBoxPermutation(s_box_result)
        xor2 = xor(l, p_box_result)
        text = r + xor2

    text = text[32:] + text[:32]
    return bin2string(InverseIpPermutation(text))


def fill(string):
    mod = len(string) % 8
    space = 8 - mod
    return string + bytes([0 for _ in range(space)]).decode('utf-8')


class DES:
    def __init__(self, message, key):
        self.message = message
        self.key = key

    @property
    def ciphertext(self):
        return self.__encrypt()
    
    @property
    def plaintext(self):
        return self.__decrypt()

    def __encrypt(self):
        output = []
        length = len(self.message)
        times, mod = length // 8, length % 8

        if mod:
            self.message = fill(self.message)
            times += 1

        for i in range(times):
            result = cipher(self.message[i * 8:i * 8 + 8], self.key, 'encrypt')
            output.append(result)
        
        return ''.join(output)

    def __decrypt(self):
        output = []
        length = len(self.message)
        times, mod = length // 8, length % 8

        if not times:
            return None
        
        if mod:
            self.message = fill(self.message)
            length += 1
        
        for i in range(times):
            result = cipher(self.message[i * 8:i * 8 + 8], self.key, 'decrypt')
            output.append(result)

        return ''.join(output).rstrip(b'\x00'.decode('utf-8'))


if __name__ == '__main__':
    print(cipher('I LOVE Y', 'ABCDEFGH'))
    print(cipher(['¯', 'Ý', '\x0f', '\x90', '*', 'd', 'Ú', 'É'], 'ABCDEFGH', mode='decrypt'))

    cipher1 = DES('Sliver Love Ariel.', 'ABCDEFGH')
    print(cipher1.ciphertext)
    cipher2 = DES(cipher1.ciphertext, 'ABCDEFGH')
    print(cipher2.plaintext)