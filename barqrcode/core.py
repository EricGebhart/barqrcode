import os

import barcode
from barcode.writer import ImageWriter
import qrcode

# import regex as re
import re

# from qrcode.image.pure import PymagingImage
from PIL import Image, ImageDraw, ImageFont, ImageOps
from tkinter import (
    Tk,
    Label,
    Entry,
    Button,
    Radiobutton,
    messagebox,
    IntVar,
    Spinbox,
)

"""
Create the barcode stickers and QR code stickers
"""

# print_command = 'echo "I would like to print this file %s"'
print_command = "brother_ql -m QL-700 -p usb://04f9:2042 print -l 29 %s"

Title = "Print Bar or Qr codes."

wfont = ("Arial Bold", 24)


def msgbox(msg):
    "Display a simple message box, enter to continue."
    messagebox.showinfo(Title, msg)


# res = messagebox.askquestion("Message title", "Message content")
# res = messagebox.askyesno("Message title", "Message content")
# res = messagebox.askyesnocancel("Message title", "Message content")
# res = messagebox.askokcancel("Message title", "Message content")
# res = messagebox.askretrycancel("Message title", "Message content")


def ynbox(msg):
    "Display a yesno dialog, return True or False."
    return messagebox.askyesno(Title, msg)


def ck_input_regex(txt, regex="^[0-9]{6}$"):
    """check a entry input that matches the regex"""
    if re.findall(regex, txt):
        return True
    else:
        msgbox("Input must match pattern: %s" % regex)
        return False


def pad_serial_num(sn):
    """make the serial number is the minimum length, pad from left with 0s."""
    return "%.6d" % int(sn)


def serial_num_2_barcode(sn):
    return pad_serial_num(sn)


def serial_num_2_qrcode(sn):
    prefix = "K1"
    suffix = "A"
    return str(prefix + pad_serial_num(sn) + suffix)


def get_bc_filename(sn):
    """generate a name for a barcode file"""
    suffix = "BC"
    return sn + suffix  # extension of png is automatic.


def get_qr_filename(sn):
    """generate a name for a QR code file"""
    suffix = "QR"
    return sn + suffix + ".png"


def create_bar_code(sn):
    """Create a barcode from a number"""
    return barcode.get("code128", serial_num_2_barcode(sn), writer=ImageWriter())


def create_qr_code(sn):
    """Create a QR code from a number"""
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=0,
    )

    qr.add_data(sn)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    backColor = "rgb(255, 255, 255)"
    # Left Top Right Bottom
    bimg = ImageOps.expand(img, border=(30, 0, 30, 40), fill=backColor)

    draw = ImageDraw.Draw(bimg)
    font = ImageFont.truetype("DejaVuSans.ttf", size=18)
    (x, y) = (34, 116)
    color = "rgb(0, 0, 0)"
    draw.text((x, y), sn, fill=color, font=font)

    return bimg


def makeFailSticker(reason, code):
    img = Image.new("L", (200, 100), 255)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("DejaVuSans.ttf", size=24)
    (x, y) = (1, 8)
    color = "rgb(0, 0, 0)"
    draw.text((x, y), "TEST FAIL", fill=color, font=font)
    font = ImageFont.truetype("DejaVuSans.ttf", size=14)
    (x, y) = (1, 33)
    case = reason + ": " + str(code)
    draw.text((x, y), case, fill=color, font=font)
    return img
    # img.save(filesystem.get_reports_path() + '/fail/' + 'fail' + '.png')


def print_it(serial, count, label_type):
    """
    A serial number,
    how many to print
    and QR or Bar code.
    Then loop through an os.system call to print.
    """

    print(serial, count, label_type)

    fn = None

    if label_type == "Bar Code":
        code = create_bar_code(serial_num_2_barcode(serial))
        fn = get_bc_filename(serial)
        options = {"module_height": 8, "text_distance": 2}
        code.save(fn, options)
        fn = fn + ".png"  # so everyone else knows it's extension.

    elif label_type == "QR Code":
        code = create_qr_code(serial_num_2_qrcode(serial))
        fn = get_qr_filename(serial)
        code.save(fn)

    command = print_command % fn
    if ynbox(
        "You are ready to print %d %s label(s) of %s?\n Using this command: %s"
        % (count, label_type, serial, command)
    ):
        for i in range(0, count):
            os.system(command)

    os.remove(fn)


def dialog_window():
    window = Tk()
    window.option_add("*font", "Helvetica 24")
    # window.option_add("*Dialog.msg.font", "Helvetica 24")
    # window.option_add("*Dialog.button.font", "Helvetica 24")
    window.title("Print Bar or QR codes")

    window.geometry("850x500")  # doesn't seem to make a difference yet.

    # input string to get serial number.
    sometitle = Label(window, text="Print Bar or QR Codes", font=wfont)
    sometitle.grid(column=0, row=0)
    snlbl = Label(window, text="Enter a Serial Number", font=wfont)
    sn = Entry(window, width=10, font=wfont)
    snlbl.grid(column=0, row=1)
    sn.grid(column=1, row=1)

    # Radio button to find out which to print.
    bc_or_qr = IntVar()
    bc_or_qr.set(0)

    rad1 = Radiobutton(window, text="Bar Code", value=0, variable=bc_or_qr, font=wfont)
    rad2 = Radiobutton(window, text="QR Code", value=1, variable=bc_or_qr, font=wfont)

    rad1.grid(column=0, row=2)
    rad2.grid(column=0, row=3)

    # Spinbox to get a count.
    spinlbl = Label(window, text="How many to print ?", font=wfont)
    # # create a default value.
    count = IntVar()
    count.set(1)
    spin = Spinbox(window, from_=0, to=100, width=5, textvariable=count, font=wfont)

    spinlbl.grid(column=0, row=4)
    spin.grid(column=1, row=4)

    Codes = ["Bar Code", "QR Code"]

    def clicked_print():
        """This is what we do when they click print."""
        txt = sn.get()
        bc = Codes[bc_or_qr.get()]
        c = count.get()
        if ck_input_regex(txt):
            print_it(txt, c, bc)
        sn.focus()

    print_btn = Button(window, text="Print", command=clicked_print, font=wfont)
    print_btn.grid(column=0, row=5)
    cancel_btn = Button(window, text="Exit", command=window.destroy, font=wfont)
    cancel_btn.grid(column=1, row=5)

    sn.focus()

    return window


def init():
    "get a dialog window and run it."
    dialog_window().mainloop()
