#!/usr/bin/python3

### bot program
# reference:
#  https://code-maven.com/interactive-shell-with-cmd-in-python
#  https://docs.python.org/3/library/cmd.html
#
# use the following for development:  
# find ./ -maxdepth 1 -name "*.py" | entr -cp python app.py


import cryptor as ct
import dbhandler as dr

import pyautogui as py
from time import sleep
from cmd import Cmd
import hashlib
from getpass import getpass
from random import choice
from string import ascii_letters, digits
from os import system
import pyperclip as pc
import configparser as cfgp

config = cfgp.ConfigParser()
config.read('config.ini')
default = config['DEFAULT']
keystroke = config['KeyStroke']



# reference: https://pynative.com/python-generate-random-string/
def randomStringDigits(stringLength=32):
    lettersAndDigits = ascii_letters + digits
    result = ''.join(choice(lettersAndDigits) for i in range(stringLength))
    return result.encode('utf-8')


def md5hash(input='YTYwMzExZTAxMmUyYTdmNzRjMGE2NGQ1'):
    return hashlib.md5(input.encode()).hexdigest()


def encrypt(password, salt, message):
    try:
        return ct.encrypt(password, salt, message)
    except Exception as e:
        return randomStringDigits()


def decrypt(password, salt, token):
    try:
        return ct.decrypt(password, salt, token)
    except Exception as e:
        return randomStringDigits()


def parse(arg):
    return tuple(map(str, arg.split()))


def insert_record(password, salt):
    new_record = dr.Record()
    new_record.account = input("enter account: ")
    new_record.notes = input("enter notes: ")
    new_record.tag = input("enter tag: ")
    new_record.url = input("enter url: ")

    new_subrecord = dr.SubRecord()
    new_subrecord.user = input("enter username: ")

    new_subrecord.password = encrypt(
                                password, salt,
                                (getpass("enter password: "))).decode()

    new_record.subrecords.append(new_subrecord)

    dr.addRecord(new_record)

    print("account %s has been created" % (new_record.account))


def is_field_updated(message, orig):
    new_value = input(f"update {message} [{orig}]: ")
    return new_value if new_value else orig


def update_record(recid):
    orig_rec = dr.getByRecordId(recid)

    new_record = dr.Record()
    new_record.account = is_field_updated("account", orig_rec.account)
    new_record.notes = is_field_updated("notes", orig_rec.notes)
    new_record.tag = is_field_updated("tag", orig_rec.tag)
    new_record.url = is_field_updated("url", orig_rec.url)

    dr.updateRecord(recid, new_record)
    #print("account %s has been created" % (new_record.account))


def display_record(record):
    print("%s:\tAccount:\t%s\n\tNotes:\t%s\n\tTag:\t%s\n\tURL:\t%s" %
            ( record.id,
              record.account,
              record.notes,
              record.tag,
              record.url
                )
            )


def all_records():
    results = dr.queryAllRecord()
    for i in results:
        #print("%s : %s " % (i.id, i.account))
        display_record(i)


def find_record(keyword):
    keyword =  f"%{keyword}%"
    results = dr.searchRecord(dr.Record.account.like(keyword))
    results += dr.searchRecord(dr.Record.notes.like(keyword))
    results += dr.searchRecord(dr.Record.tag.like(keyword))
    results = set(results)

    for i in results:
        #print("%s : %s " % (i.id, i.account))
        display_record(i)


def display_cred(password, salt, recid):
    result = dr.getRecentSubRecord(recid)

    #print(f"{result.password}")

    displayP = decrypt(password, salt, result.password).decode()
    print(f"{result.user} {displayP}")
    displayP = None
    del displayP
    sleep(5)
    system('clear')


def push_cred(password, salt, delay, recid, first, second):
    sleep(delay)
    result = dr.getRecentSubRecord(recid)

    py.write(result.user)
    py.press(first)

    displayP = decrypt(password, salt, result.password).decode()
    py.write(displayP)
    displayP = None
    del displayP
    py.press(second)

def push_pw(password, salt, delay, recid):
    sleep(delay)
    result = dr.getRecentSubRecord(recid)

    displayP = decrypt(password, salt, result.password).decode()
    py.write(displayP)
    displayP = None
    del displayP

def copy_cred(password, salt, recid):
    result = dr.getRecentSubRecord(recid)
    displayP = decrypt(password, salt, result.password).decode()
    pc.copy(displayP)
    displayP = None
    del displayP
    print("Clipboard will clear in 15 sec.")
    sleep(15)
    pc.copy("")
    system('clear')




def update_subrecord(recid, password, salt):
    new_subrecord = dr.SubRecord()
    new_subrecord.user = input("enter username: ")
    new_subrecord.password = encrypt(
                                password, salt,
                                (getpass("enter password: "))).decode()

    dr.appendSubRecord(recid, new_subrecord)



# bot class
class bot(Cmd):
    prompt =  default['Prompt'] + " "
    app_key = default['AppKey']
    pwhash = md5hash()
    delay = int(default['Delay'])
    interval = float(default['Interval'])

    ks_first = keystroke['First']
    ks_second = keystroke['Second']


    # standard commands
    def emptyline(self):
        pass

    def do_exit(self, arg):
        print("exiting")
        return True

    def do_clear(self, arg):
        system('clear')

    def do_set_app_key(self, arg):
        self.app_key = arg

    def do_set_password(self, arg):
        self.pwhash = md5hash(getpass("enter password: "))

    def do_show_app(self, arg):
        print(self.app_key)


    # encrypt/decrypt and push keystrokes
    def do_EncryptMessage(self, arg):
        print(encrypt(self.pwhash, self.app_key, arg))

    def do_DecryptMessage(self, arg):
        print(decrypt(self.pwhash, self.app_key, arg))

    def do_TypeThis(self, arg):
        sleep(self.delay)
        py.write(arg, interval=self.interval)

    def do_TypeSecret(self, arg):
        secret = getpass("enter secret: ")
        sleep(self.delay)
        py.write(secret, interval=self.interval)
        secret = None
        del secret


    # Record db interaction
    def do_Add_Record(self, arg):
        insert_record(self.pwhash, self.app_key)

    def do_All_Records(self, arg):
        all_records()

    def do_Find_Record(self, arg):
        find_record(arg)

    def do_Update_Record(self, arg):
        update_record(arg)

    def do_Show_Cred(self, arg):
        display_cred(self.pwhash, self.app_key, arg)

    def do_Push_Cred(self, arg):
        input_array = arg.split(' ')

        if len(input_array) == 3:
            recid, first, second =  input_array
        else:
            recid = arg
            first = keystroke['First']
            second = keystroke['Second']


        push_cred(self.pwhash, self.app_key, self.delay, recid, first, second)

    def do_Push_Password(self,arg):
        push_pw(self.pwhash, self.app_key, self.delay, arg)

    def do_Copy_Cred(self, arg):
        copy_cred(self.pwhash, self.app_key, arg)


    def do_Update_Cred(self, arg):
        update_subrecord(arg, self.pwhash, self.app_key)

#    def do_Func(self, arg):
#        pass



if __name__ == "__main__":
    try:
        bot().cmdloop()
    except:
        print("error")




# things to add
#  py.hotkey('ctrl', 'c')
#  pyautogui.typewrite('Hello world!\n', interval=secs_between_keys)  # useful for entering text, newline is Enter
#  pyautogui.typewrite(['a', 'b', 'c', 'left', 'backspace', 'enter', 'f1'], interval=secs_between_keys)
#  pyautogui.keyDown(key_name)
#  pyautogui.keyUp(key_name)


