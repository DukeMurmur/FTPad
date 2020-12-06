# FTPad
Python script to transfer files from windows to linux over SCP

# Works only on windows!
A script.reg file will edit the windows registry value to enable drag & drop over python scripts<br />
It can also be launched with parameters from console e.g. python FTPad.py C://Path to file, C://Path to file ... etc<br />
# Default path
By default, the path where the files will be copied is the home folder of the ssh user<br />
For mobile, home folder will be /var/mobile/<br />
For root, home folder will be /var/root/<br />
For the program, the default path is /var/root/. If this path is indicated, it won't attempt to move copied files anywhere.
You can indicate this path manually at the configuration stage, or leave path parameter blank (this will automatically set path to /var/root/)
<br /><br />/var/root/ doesn't mean that the files will be copied there!<br />It literally means do nothing with copied files<br /><br />
However, indicating other locations will make program to move copied files there
# Filenames & paths to those files
All filenames and paths should be in english letters only, otherwise this will lead to program crash
# Configuration file
By default, the configuration file is created at C://Windows//System32, called FTPad_config<br />Program enters configuration mode if it is unable to find
FTPad_config file in the indicated directory.<br />The format of FTPad_config is a python list, where<br /><br />[hostname (string value), port (int value), username  (string value), password  (string value), path  (string value), show_logo (bool), typewriter(bool)]<br /><br />This file will be created at the first launch, after that it can be edited manually or by the program.<br />To enter the configuration mode with FTPad_config existing, run FTPad without any parameters (python FTPad.py).
# Setting up
The path to config file can be changed in line 23<br />
The name of the config file can be changed in line 25
# Flags
Flags is used to print the config file data or to change its parameters separately<br />
Usage: FTPad.py -F new_value for:<br />
-h or -host to change server address<br />
-p or -port to change port number<br />
-u or -username to change username<br />
-s or -password to change password<br />
-r or -path to change path, where files would be saved<br />
-c or -print_config to print the config file data<br />
(Second parameter after flag is not required, it can be entered in input field afterwards)<br />
Usage: FTpad.py -F new_value new_value for:<br />
-m or -mod_logo first parameter to disable or enable logo, second to enable or disable printing letter by letter<br />
1 - enabled<br />
0 - disabled
# .exe
There is a compiled version of the program, however it is unable to change the config file directory<br />
The path used is the current path where the program is stored<br />
It cannot be modified anyhow except recompiling the program
# Requirements.txt
There is a colorama module in requirements, however it is not compulsory
scp & paramiko are mandatory to make program work

