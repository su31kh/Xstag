global path_image
from base64 import b64encode
# from PIL.Image import Resampling

from PIL import Image, ImageTk
import PIL.Image
from tkinter import PhotoImage, filedialog
import cv2
import numpy as np
import math
import tkinter as tk
from tkinter import filedialog, Tk, Button, Label,Text,WORD


#global path_image
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode
from Crypto.Cipher import AES

data = '0'
image_display_size = 350, 200


def on_clickl():
    global path_image
    path_image = filedialog.askopenfilename()
    load_image = Image.open(path_image)
    load_image.thumbnail(image_display_size, Image.ANTIALIAS)
    np_load_image = np.asarray(load_image)
    np_load_image = Image.fromarray(np.uint8(np_load_image))
    render = ImageTk.PhotoImage(np_load_image)
    img = Label(root, image=render)
    img.image = render
    img.grid(column=0,row=1)


def encrypt_data_into_image():
    # Step 2
    #global path_image
    meta_data = txt.get(1.0, "end-1c")
    # print(meta_data)

    with open('text.txt', 'r+') as entry:
        entry.truncate(0)
        entry.write(meta_data)

    key = pas.get(1.0, "end-1c")
    key = key.encode("UTF-8")
    key = pad(key, AES.block_size)

    def encrypt(file_name, key):
        with open(file_name, 'rb') as entry:
            data = entry.read()
            cipher = AES.new(key, AES.MODE_CFB)
            ciphertext = cipher.encrypt(pad(data, AES.block_size))
            iv = b64encode(cipher.iv).decode('UTF-8')
            ciphertext = b64encode(ciphertext).decode('UTF-8')
            to_write = iv + ciphertext
        entry.close()
        with open(file_name + '.enc', 'w') as data:
            data.truncate(0)
            data.write(to_write)
        data.close()

    encrypt('text.txt', key)

    with open('text.txt.enc', 'r') as entry:
        data = entry.read()

    img = cv2.imread(path_image)
    data = [format(ord(i), '08b') for i in data]
    _, width, _ = img.shape
    PixReq = len(data) * 3
    RowReq = PixReq / width
    RowReq = math.ceil(RowReq)
    count = 0
    charCount = 0
    for i in range(RowReq + 1):
        while (count < width and charCount < len(data)):
            char = data[charCount]
            charCount += 1
            for index_k, k in enumerate(char):
                if (k == '1' and img[i][count][index_k % 3] % 2 == 0) or (
                        k == '0' and img[i][count][index_k % 3] % 2 == 1):
                    img[i][count][index_k % 3] -= 1
                if (index_k % 3 == 2):
                    count += 1
                if (index_k == 7):
                    if (charCount * 3 < PixReq and img[i][count][2] % 2 == 1):
                        img[i][count][2] -= 1
                    if (charCount * 3 >= PixReq and img[i][count][2] % 2 == 0):
                        img[i][count][2] -= 1
                    count += 1
        count = 0

    cv2.imwrite("encrypted_image.png", img)
    success_label = Label(root, text="Encryption Successful!",
                          bg='lavender', font=("Times New Roman", 20))
    success_label.place(x=160, y=300)


def on_clickr():
    # Step 1.5
    global path_image2
    path_image2 = filedialog.askopenfilename()
    load_image2 = Image.open(path_image2)
    load_image2.thumbnail(image_display_size, Image.ANTIALIAS)
    np_load_image2 = np.asarray(load_image2)
    np_load_image2 = Image.fromarray(np.uint8(np_load_image2))
    render = ImageTk.PhotoImage(np_load_image2)
    img2 = Label(root, image=render)
    img2.image = render
    img2.grid(column=2,row=1)


def decrypt():
    load = PIL.Image.open(path_image2)
    load.thumbnail(image_display_size)
    load = np.asarray(load)
    load = Image.fromarray(np.uint8(load))
    render = ImageTk.PhotoImage(load)
    img = Label(root, image=render)
    img.image = render
    img = cv2.imread(path_image2)
    data = []
    stop = False
    for index_i, i in enumerate(img):
        i.tolist()
        for index_j, j in enumerate(i):
            if ((index_j) % 3 == 2):
                data.append(bin(j[0])[-1])
                data.append(bin(j[1])[-1])
                if (bin(j[2])[-1] == '1'):
                    stop = True
                    break
            else:
                data.append(bin(j[0])[-1])
                data.append(bin(j[1])[-1])
                data.append(bin(j[2])[-1])
        if (stop):
            break

    message = []

    for i in range(int((len(data) + 1) / 8)):
        message.append(data[i * 8:(i * 8 + 8)])
    message = [chr(int(''.join(i), 2)) for i in message]
    message = ''.join(message)
    # print(message)
    metta = message
    with open('secret.txt.enc', 'w') as data:
        data.truncate(0)
        data.write(message)

    key = passt.get(1.0, "end-1c")
    key = key.encode('UTF-8')
    key = pad(key, AES.block_size)

    with open('secret.txt.enc', 'r') as entry:
        try:
            data = entry.read()
            length = len(data)
            iv = data[:24]
            iv = b64decode(iv)
            ciphertext = data[24:length]
            ciphertext = b64decode(ciphertext)
            cipher = AES.new(key, AES.MODE_CFB, iv)
            decrypted = cipher.decrypt(ciphertext)
            decrypted = unpad(decrypted, AES.block_size)
            message = decrypted
        except(ValueError, KeyError):
            # print('wrong password')
            message = 'wrong password'
    message_label = Label(root, text=message, font=("Times New Roman", 10))
    message_label.grid(column=2,row=3)


# gui 

root= tk.Tk()
root.title("Xstag")

ico= PhotoImage(file="logox.png")
root.iconphoto(False, ico)

canvas= tk.Canvas(root, width=1200, height= 600,background="#86D1D0")
canvas.grid(columnspan=4,rowspan=8)

instructions= tk.Label(root, text="Encrypt your image")
instructions.grid(columnspan=1, column=0, row=0)

instructions2= tk.Label(root, text="Decrypt your image")
instructions2.grid(columnspan=1, column=2, row=0)

browse_img= tk.StringVar()
browse_bt= tk.Button(root, textvariable= browse_img, command= on_clickl)
browse_img.set("Browse")
browse_bt.grid(column=1,row=1)

browse_img2= tk.StringVar()
browse_bt2= tk.Button(root, textvariable= browse_img2, command= on_clickr)
browse_img2.set("Browse")
browse_bt2.grid(column=3,row=1)

msg_lable= Label(root,text="Enter the message")
msg_lable.grid(columnspan=1,column=0,row=3)

txt = Text(root, wrap=WORD, width=30,height=3)
txt.grid(columnspan=1,column=0,row=4)

passw= Label(root, text="Set a password")
passw.grid(columnspan=1,column=1,row=3)

pas = Text(root,wrap=WORD, width=30,height=1)
pas.grid(columnspan=1,column=1,row=4)

encrypt_bt= tk.Button(root,command=encrypt_data_into_image,text="Encrypt")
encrypt_bt.grid(columnspan=1,column=0,row=5)

passd=Label(root,text="Enter the password")
passd.grid(columnspan=1,column=3,row=3)

passt=Text(root,wrap=WORD,width=30, height=1)
passt.grid(columnspan=1,column=3,row=4)

dencrypt_bt= tk.Button(root,command=decrypt,text="Decrypt")
dencrypt_bt.grid(columnspan=1,column=3,row=5)

root.mainloop()
