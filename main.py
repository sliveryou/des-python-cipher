# -*- coding: UTF-8 -*-
__author__ = 'Sliver'

from tkinter import *
import tkinter.messagebox as mbox
from DES import DES


class Cipher(Frame):
    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.var1 = Variable()
        self.var2 = Variable()
        self.var3 = Variable()
        self.var4 = Variable()

        self.lab1 = Label(frame, text="明文：")
        self.lab1.grid(row=0, column=0, sticky=W)

        self.ent1 = Entry(frame)
        self.ent1.grid(row=0, column=1, sticky=W)

        self.lab2 = Label(frame, text="密钥：")
        self.lab2.grid(row=1, column=0, sticky=W)

        self.ent2 = Entry(frame)
        self.ent2.grid(row=1, column=1, sticky=W)

        self.lab3 = Label(frame, text="结果：")
        self.lab3.grid(row=2, column=0, sticky=W)

        self.ent3 = Entry(frame, textvariable=self.var1)
        self.ent3.grid(row=2, column=1, sticky=W)

        self.button1 = Button(frame, text="加密", command=self.encrypt, fg='orange')
        self.button1.grid(row=3, column=1)

        self.lab4 = Label(frame, text="密文：")
        self.lab4.grid(row=4, column=0, sticky=W)

        self.ent4 = Entry(frame, textvariable=self.var3)
        self.ent4.grid(row=4, column=1, sticky=W)

        self.lab5 = Label(frame, text="密钥：")
        self.lab5.grid(row=5, column=0, sticky=W)

        self.ent5 = Entry(frame, textvariable=self.var4)
        self.ent5.grid(row=5, column=1, sticky=W)

        self.lab6 = Label(frame, text="结果：")
        self.lab6.grid(row=6, column=0, sticky=W)

        self.ent6 = Entry(frame, textvariable=self.var2)
        self.ent6.grid(row=6, column=1, sticky=W)

        self.button2 = Button(frame, text="解密", command=self.decrypt, fg='orange')
        self.button2.grid(row=7, column=1)

    def encrypt(self):
        message = self.ent1.get()
        key = self.ent2.get()
        if len(key) != 8:
            mbox.showwarning('错误','密钥须为8字节字符！')
            return
        result = DES(message, key)
        self.var1.set(result.ciphertext)

        self.var3.set(result.ciphertext)
        self.var4.set(key)

    def decrypt(self):
        message = self.ent4.get()
        key = self.ent5.get()
        if len(key) != 8:
            mbox.showwarning('错误','密钥须为8字节字符！')
            return
        result = DES(message, key)
        if result.plaintext:
            self.var2.set(result.plaintext)
        else:
            mbox.showwarning('错误', '密文缺失信息，无法解密！')


root = Tk()
root.title('DES')
root.geometry('400x250')
app = Cipher(root)
root.mainloop()