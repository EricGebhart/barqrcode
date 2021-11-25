# barqrcode


## Needs Dialog installed to work.

Here is the install for Arch Linux
and Apple.
    
    sudo pacman -S dialog
    
    brew install dialog
    
    
## Setting commands
At the top of core.py there are variables
for the print command and the window titles.

The Title is what will be displayed at the top of the dialogs.


``` python
# print_command = 'echo "I would like to print this file %s"'
print_command = "brother_ql -m QL-700 -p usb://04f9:2042 print -l 29 %s"

Title = "Print Bar or Qr codes."
```


## Installing.

After the code has been modified appropriately the install can be done with;

```python setup.py install```

The program can then be run with;

```barqrcode```

or 

```python -m barqrcode```


## The Process
When run, this program uses python dialogs to; 

  * ask for a serial number,
  * ask for a count to print,
  * Ask Bar or QR code.
  * Give a y/n confirmation dialog.
  * Loop over a shell command to print the code file
  * Remove the code file when done.



