# pyvi
## A polymorphic virus that effects python files

A polymorphic virus is one that can morph or change itself in a way, through filename
changes or changes to compression (encryption of the virus body) using variable keys
or some other way. 

As a rough overview, my virus is divided into 2 parts:
* The decryption routine (unencrypted)
* The virus body (which contains the replication mechanism and the payload)

Virus Working 
My virus is an appending virus (It appends its body to the existing code of the file to-be-infected).

The initial virus file, virus.py, contains the virus body unencrypted.
However, as soon as it is executed and finds another uninfected .py file in the directory,
virus.py will encrypt its own body. It will append the (unencrypted) decryption routine first into the uninfected
file and after that it will append its encrypted virus body into the file. Last, it will execute its payload which in
our case is a simple: 

```
print('Hello World!')

```

Now, the newly infected file contains, in addition to its own code, the decryption routine + the **encrypted** virus body (which includes the payload and the replication logic).
When this newly infected file will be executed in a directory containing other python files, it will execute the payload and copy its body to all the other files. 
