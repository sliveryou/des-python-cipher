# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from operation import IpPermutation, InverseIpPermutation, ExtendPermutation, \
                      CreateSubKeys, SBoxPermutation, PBoxPermutation, \
                      string2bin, bin2string, xor, dex2bin8


def separate(lst):
    '''['11010100', '10110010', ...] -> [1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, ...]'''
    return [int(i) for i in ''.join(lst)]


def merge(lst):
    '''[1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, ...] -> ['11010100', '10110010', ...]'''
    result = []
    for i in range(8):
        temp = [str(x) for x in lst[i * 8:i * 8 + 8]]
        result.append(''.join(temp))
    return result


def cipher(message, key, mode='encrypt'):
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
    return InverseIpPermutation(text)


def fill(string):
    '''
    填充函数，若字符分组长度不为8的倍数，补全为8的整数倍。
    如：'ABCDE' -> 'ABCDEABC'
    '''
    mod = len(string) % 8
    space = 8 - mod
    return string + string[:space]


class DES:
    def __init__(self, key):
        self.key = key
        
    @staticmethod
    def __readfile(filename):
        with open(filename, 'rb') as f:
            string = f.read()
            binList = [dex2bin8(string[i]) for i in range(len(string))]
        return binList

    @staticmethod
    def __writefile(filename, encryptList, mode):
        first = {0: 'encrypt.', 1: 'decryt.'}
        last = filename.split('.')[-1]
        
        with open(first[mode] + last, 'wb') as f:
            byte = bytes(int(b, 2) for b in encryptList)
            f.write(byte)

    def encrypt(self, filename):
        output = []
        binList = self.__readfile(filename)
        length = len(binList)
        times, mod = length // 8, length % 8

        if mod:
            binList = fill(binList)
            times += 1

        for i in range(times):
            group = separate(binList[i * 8:i * 8 + 8])
            result = merge(cipher(group, self.key, 'encrypt'))
            output.extend(result)
        
        self.__writefile(filename, output, 0)

    def decrypt(self, filename):
        output = []
        binList = self.__readfile(filename)
        length = len(binList)
        times, mod = length // 8, length % 8

        if not times:
            return None
        
        if mod:
            binList = fill(binList)
            length += 1
        
        for i in range(times):
            group = separate(binList[i * 8:i * 8 + 8])
            result = merge(cipher(group, self.key, 'decrypt'))
            output.extend(result)
            
        self.__writefile(filename, output, 1)


if __name__ == '__main__':
    test1 = DES('ABCDEFGH')
    test1.encrypt('test.py')
    test1.decrypt('encrypt.py')
    test1.encrypt('test.jpeg')
    test1.decrypt('encrypt.jpeg')