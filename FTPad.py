# Importing modules
import time
import os
import sys
import paramiko
import json
import platform
import shlex
import struct
from scp import SCPClient
from pathlib import Path

# Declaring global values
global filelist
global host
global port
global username
global password
global fpath
global sys_color

global config_path
config_path = 'C:\\Windows\\System32' #This is the path to your config file
global config_name
config_name = 'FTPad_config' #This is the name of your config file
is_compiled = True
if is_compiled == True:
    config_path = os.getcwd()
    config_name = sys.argv[0].split('.')[0] + "_config"

# Checks if colorama module is avaliable, sets up sys_color to enable or disable colored output
try:
    from colorama import init
    init()
    from colorama import Fore, Back, Style
    sys_color = True
except:
	sys_color = False

# Prints text letter by letter with a given time interval (coeff)
def print_slow(text, coeff = 0.025):
    [(sys.stdout.write(letter), sys.stdout.flush(), time.sleep(coeff)) for letter in text] #requires: import time, sys

# Used to print text with a given color, format & speed in format: state('the text itself', 'color', '\n in the end of the line', 'letter by letter or all together')
def state(text, color = 'w', enter = 'n', mode = 's'):

    # If colorama is not installed, any parameter given to color would be changed to w (white)
    if sys_color == False:
        color = 'w'

    # Disables letter by letter printing
    if sys_print_slow == False:
        mode = 'n'

    if color == 'r':
        print(Fore.RED, end = '')
        print(Style.BRIGHT, end = '')
        if mode == 's':
            print_slow(text)
            if enter == 'y':
                print('\n')
            else:
                print('')
        elif mode == 'n':
            print(text)
            if enter == 'y':
                print('')
        else:
            None
        print(Style.RESET_ALL, end = '')
        
    if color == 'g':
        print(Fore.GREEN, end = '')
        print(Style.BRIGHT, end = '')
        if mode == 's':
            print_slow(text)
            if enter == 'y':
                print('\n')
            else:
                print('')
        elif mode == 'n':
            print(text)
            if enter == 'y':
                print('')
        else:
            None
        print(Style.RESET_ALL, end = '')
    
    if color == 'b':
        print(Fore.BLUE, end = '')
        print(Style.BRIGHT, end = '')
        if mode == 's':
            print_slow(text)
            if enter == 'y':
                print('\n')
            else:
                print('')
        elif mode == 'n':
            print(text)
            if enter == 'y':
                print('')
        else:
            None
        print(Style.RESET_ALL, end = '')
        
    if color == 'm':
        print(Fore.MAGENTA, end = '')
        print(Style.BRIGHT, end = '')
        if mode == 's':
            print_slow(text)
            if enter == 'y':
                print('\n')
            else:
                print('')
        elif mode == 'n':
            print(text)
            if enter == 'y':
                print('')
        else:
            None
        print(Style.RESET_ALL, end = '')
        
    if color == 'c':
        print(Fore.CYAN, end = '')
        print(Style.BRIGHT, end = '')
        if mode == 's':
            print_slow(text)
            if enter == 'y':
                print('\n')
            else:
                print('')
        elif mode == 'n':
            print(text)
            if enter == 'y':
                print('')
        else:
            None
        print(Style.RESET_ALL, end = '')
        
    if color == 'y':
        print(Fore.YELLOW, end = '')
        print(Style.BRIGHT, end = '')
        if mode == 's':
            print_slow(text)
            if enter == 'y':
                print('\n')
            else:
                print('')
        elif mode == 'n':
            print(text)
            if enter == 'y':
                print('')
        else:
            None
        print(Style.RESET_ALL, end = '')

    if color == 'w':
        if sys_color == True:
            print(Style.RESET_ALL, end = '')
        if mode == 's':
            print_slow(text)
            if enter == 'y':
                print('\n')
            else:
                print('')
        elif mode == 'n':
            print(text)
            if enter == 'y':
                print('')
        else:
            None

# Gets the terminal size (required only for logo)
def size():
    def get_terminal_size():
        current_os = platform.system()
        tuple_xy = None

        if current_os == 'Windows':
            tuple_xy = _get_terminal_size_windows()

            if tuple_xy is None:
                tuple_xy = _get_terminal_size_tput()

        if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
            tuple_xy = _get_terminal_size_linux()

        if tuple_xy is None:
            tuple_xy = (80, 25)
        return tuple_xy


    def _get_terminal_size_windows():

        try:
            from ctypes import windll, create_string_buffer
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
            if res:
                (bufx, bufy, curx, cury, wattr,
                 left, top, right, bottom,
                 maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
                sizex = right - left + 1
                sizey = bottom - top + 1
                return sizex, sizey
        except:
            pass


    def _get_terminal_size_tput():

        try:
            cols = int(subprocess.check_call(shlex.split('tput cols')))
            rows = int(subprocess.check_call(shlex.split('tput lines')))
            return (cols, rows)
        except:
            pass


    def _get_terminal_size_linux():

        def ioctl_GWINSZ(fd):
            try:
                import fcntl
                import termios
                cr = struct.unpack('hh',
                                   fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
                return cr

            except:
                pass

        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)

            except:
                pass

        if not cr:
            try:
                cr = (os.environ['LINES'], os.environ['COLUMNS'])

            except:
                return None

        return int(cr[1]), int(cr[0])

    def det_size():
        if __name__ == "__main__":
            sizex, sizey = get_terminal_size()

            return [sizex, sizey]
    return det_size()

# Load or create config file
def config(mode = 'base'):
    global host
    global port
    global username
    global password
    global fpath
    global sys_logo
    global sys_print_slow

    os.chdir(config_path)

    try:
        if mode == 'setup':
            a = b
        file = open(config_name, 'r')
        data = json.load(file)
        file.close()
        host = data[0]
        port = data[1]
        username = data[2]
        password = data[3]
        fpath = data[4]
        sys_logo = data[5]
        sys_print_slow = data[6]

    except:
        if mode == 'base':
            print('No configuration file has been found!')
            print('Enter address of the remote host: ')
        if mode == 'setup':
            print('Enter new configuration data: ')
        host = input('Enter a host name (or ip): ')
        def prt():
            port = input('Enter a port number (eg. 22): ')
            try:
                port = int(port)
                return port
            except:
                print('Warning! Incorrect port number!')
                return False
        port = prt()
        while port == False:
            port  = prt()
        username = input('Enter a username: ')
        password = input('Enter password: ')
        fpath = input('Enter path (leave empty, then default path (/var/root/) will be used): ')
        if fpath == '':
            fpath = " /var/root/"
        else:
            fpath = '" ' + fpath + '"'
        sys_mod = 0
        if input('Do you want to modify system config? (y/n): ') == 'y':
            sys_mod = 1
            sys_logo = input('Enter sys_logo value (1/0): ')
            exit_101 = 0
            while exit_101 != 1:
                try:
                    sys_logo = bool(int(sys_logo))
                    exit_101 = 1
                except:
                    print('Failed to convert to bool!')
                    sys_logo = input('Enter sys_logo value (1/0): ')
            sys_print_slow = input('Enter sys_print_slow value (1/0): ')
            exit_101 = 0
            while exit_101 != 1:
                try:
                    sys_print_slow = bool(int(sys_print_slow))
                    exit_101 = 1
                except:
                    print('Failed to convert to bool!')
                    sys_print_slow = input('Enter sys_logo value (1/0): ')

        if sys_mod == 0:
            lst = [host, port, username, password, fpath, True, True]
        else:
            lst = [host, port, username, password, fpath, sys_logo, sys_print_slow]
        file = open(config_name, 'w')
        file.write(json.dumps(lst))
        file.close()
        print('Configurations has been saved!')
        if len(sys.argv) < 2:
            input('Enter to exit: ')
            return 0
        if mode == 'setup':
            input('Enter to exit: ')
            return 0
        config()

# Check if any parameters were given to program
def check():
    if len(sys.argv) >= 2:
        return 'Drag'
    else:
        return 'Norm'

# Prints logo
def logo(mode = 'std'):

    author_logo = ' |\\___/|                                                    \n )     (           _=,_                                     \n=\\     /=       o_/6 /#\\                                    \n  )===(         \\__ |##/                                    \n /     \\         =\'|--\\                                     \n |     |           /   #\'-.                                 \n/       \\          \\#|_   _\'-. /                            \n\\       /           |/ \\_( # |"                             \n \\__  _/           C/ ,--___/                               \n   ( (                                                      \n    ) )                     Developed by:                   \n    (_(                           Duke Murmur & Count Furfur'
    
    pattern = ['|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|',
               '|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|\\/|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|/\\|']
    
    program_logo = ['                                                                                            dddddddd\n',
                    'FFFFFFFFFFFFFFFFFFFFFFTTTTTTTTTTTTTTTTTTTTTTTPPPPPPPPPPPPPPPPP                              d::::::d\n',
                    'F::::::::::::::::::::FT:::::::::::::::::::::TP::::::::::::::::P                             d::::::d\n',
                    'F::::::::::::::::::::FT:::::::::::::::::::::TP::::::PPPPPP:::::P                            d::::::d\n',
                    'FF::::::FFFFFFFFF::::FT:::::TT:::::::TT:::::TPP:::::P     P:::::P                           d:::::d \n',
                    '  F:::::F       FFFFFFTTTTTT  T:::::T  TTTTTT  P::::P     P:::::Paaaaaaaaaaaaa      ddddddddd:::::d \n',
                    '  F:::::F                     T:::::T          P::::P     P:::::Pa::::::::::::a   dd::::::::::::::d \n',
                    '  F::::::FFFFFFFFFF           T:::::T          P::::PPPPPP:::::P aaaaaaaaa:::::a d::::::::::::::::d \n',
                    '  F:::::::::::::::F           T:::::T          P:::::::::::::PP           a::::ad:::::::ddddd:::::d \n',
                    '  F:::::::::::::::F           T:::::T          P::::PPPPPPPPP      aaaaaaa:::::ad::::::d    d:::::d \n',
                    '  F::::::FFFFFFFFFF           T:::::T          P::::P            aa::::::::::::ad:::::d     d:::::d \n',
                    '  F:::::F                     T:::::T          P::::P           a::::aaaa::::::ad:::::d     d:::::d \n',
                    '  F:::::F                     T:::::T          P::::P          a::::a    a:::::ad:::::d     d:::::d \n',
                    'FF:::::::FF                 TT:::::::TT      PP::::::PP        a::::a    a:::::ad::::::ddddd::::::dd\n',
                    'F::::::::FF                 T:::::::::T      P::::::::P        a:::::aaaa::::::a d:::::::::::::::::d\n',
                    'F::::::::FF                 T:::::::::T      P::::::::P         a::::::::::aa:::a d:::::::::ddd::::d\n',
                    'FFFFFFFFFFF                 TTTTTTTTTTT      PPPPPPPPPP          aaaaaaaaaa  aaaa  ddddddddd   ddddd']

    console_logo = "   ___                  _     \n  / __|___ _ _  ___ ___| |___ \n | (__/ _ \\ ' \\(_-</ _ \\ / -_)\n  \\___\\___/_||_/__/\\___/_\\___|"
    computer_logo = '                  .----.\n      .---------. | == |\n      |.-"""""-.| |----|\n      ||       || | == |\n      ||       || |----|\n      |\'-.....-\'| |::::|\n      `"")---(""` |___.|\n     /:::::::::::\\" _  "\n    /:::=======:::\\`\\`\\ \n    `"""""""""""""`  \'-\''
    
    if mode == 'std':
  
        lenght = size()[0]

        state(pattern[0][0 : lenght - 1], 'm', 'n', 'n')
        state(pattern[1][0 : lenght - 1], 'm', 'n', 'n')
        print('\n')

        if sys_color == True:
            print(Fore.YELLOW, end = '')
            print(Style.BRIGHT, end = '')

        print(author_logo[0 : len(author_logo) - 93], end = '')

        if sys_color == True:
            print(Fore.CYAN, end = '')

        print(author_logo[len(author_logo) - 93 : len(author_logo) - 75], end = '')

        if sys_color == True:
            print(Fore.YELLOW, end = '')

        print(author_logo[len(author_logo) - 75 : len(author_logo) - 45], end = '')

        if sys_color == True:
            print(Fore.CYAN, end = '')

        print(author_logo[len(author_logo) - 45 : len(author_logo)], end = '')
        print('\n')

        state(pattern[0][0 : lenght - 1], 'm', 'n', 'n')
        state(pattern[1][0 : lenght - 1], 'm', 'n', 'n')

        output = '© All rights reserved, 2020'
        spaces = ' ' * (lenght - len(output))
        output = spaces + output
        state('\n\n' + output, 'r', 'n', 'n')

        time.sleep(3)
        os.system('CLS')


        for item in program_logo:

            if sys_color == True:
                print(Fore.YELLOW, end = '')
                print(Style.BRIGHT, end = '')

            print(item[0 : 45], end = '')

            if sys_color == True:
                print(Fore.CYAN, end = '')
                print(Style.BRIGHT, end = '')

            print(item[45 : len(item) - 1])

            if sys_color == True:
                print(Style.RESET_ALL, end = '')

        print('')
        state('FTPad, version 4.2.9 on python 3.8.2', 'm', 'y')
        state('File transfer for iPad (or other unix based systems)', 'b', 'y')
        state('*** Transfer files from windows to linux only, path indication is not required! ***', 'r')
        state('*** The default destination folder would be a folder of ssh user ***', 'r')
        state('*** If you want to use default folder of user, leave path field empty on configuration setup ***', 'y')
        state('*** You can also indicate /var/root/ (same as empty) to prevent program from copying you files anywhere ***\n', 'y')
        state('*** Drag & Drop files on python script, or use full paths as a parameters if executed from terminal! ***', 'r', 'y')
        state('*** Filenames or filepaths that contain non english letters will probably return an error while copying! ***', 'r')
        state('*** Make sure you have all names and paths in english or create a temporary directory with english filenames ***\n', 'r')
        state('*** Printing logo or speed of text printing can be adjusted in config file, 1 - enabled, 0 - disabled ***', 'y')
        state('*** You can also change them by using flags, use --help to get more info ***\n', 'y')
        state('*** Launching a program without parameters will enter configuration mode, where server info can be edited ***', 'g')
        state('*** By default the configuration file will be stored in C://Windows//System32, path can be changed in line 23 ***', 'g')
        state('*** By default the configuration file named FTPad_config name can be changed in line 25 ***\n', 'g')
        state('*** If the program is compiled into .exe the default path would be the same path as where the program is stored ***', 'r')
        state('*** It can not be changed anyhow except recompiling it with the new path ***', 'r')

        time.sleep(3)

        os.system('CLS')

    computer_logo = computer_logo.split('\n')
    console_logo = console_logo.split('\n')

    for i in range(6):
        state(computer_logo[i], 'c', 'n', 'n')

    for j in range(4):

        if sys_color == True:
            print(Fore.CYAN, end = '')
            print(Style.BRIGHT, end = '')

        print(computer_logo[j + 5] + '      ', end = '')

        if sys_color == True:
            print(Fore.YELLOW, end = '')
        
        print(console_logo[j])

    print('\n')

# Old module, not used here any more
def module_import():
    None

# Connecting to the remote host
def connecting():
    global filelist

    def createSSHClient(server, port, user, password):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port, user, password)
        return client

    def progress(filename, size, sent):
        filename = filename.decode()
        sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )


    string = 'Establishing connection to ' + host + ', port ' + str(port) + ', username: ' + username + '...'

    state(string, 'c')

    ssh = createSSHClient(host, port, username, password)
    scp = SCPClient(ssh.get_transport(), progress = progress)

    state('Done', 'g')


    state('\nCopying files...', 'c')

    filelist = sys.argv[1 : len(sys.argv)]

    count = 1
    for item in filelist:

        try:

            if sys_color == True:
                print(Fore.YELLOW, end = '')
                print(Style.BRIGHT, end = '')
            scp.put(item)
            print('  (Total progress: ' + str(count) + '/' + str(len(filelist)) + ' or ' + str(round((count / len(filelist) * 100), 2)) + '%)                                   ')
            count += 1

        except:

            string = 'Error while copying file: ' + item
            state(string, 'r', 'n', 'n')

    if sys_color == True:
        print(Style.RESET_ALL, end = '')

    state('Done', 'g')

# Moving to given path
def moving(mode = 'n'):
    if mode == 'n':
        state('\nConnecting to the remote host through ssh...', 'c')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    if mode == 'n':
        state('Done', 'g')

    if mode == 'n':
        state('\nCopying files to the given directory...', 'c')

    for item in filelist:

        command = 'cp ./"' + Path(item).name + fpath + Path(item).name + '"'
        stdin, stdout, stderr = ssh.exec_command(command)

        if fpath != " /var/root/":
            command = 'rm ./"' + Path(item).name + '"'
            stdin, stdout, stderr = ssh.exec_command(command)

    state('Done', 'g')

# Prints enter to exit
def end():
    state('\n\nFile transfer has been completed successfully!', 'g')
    input('\nPress enter to exit: ')

# Combines connecting & moving
def drag():
    try:
        connecting()

    except:
        state('An error occured while transfering data!', 'r')
        state('Check the filenames and filepaths!', 'r')
        input('Enter to exit: ')
        sys.exit()

    if fpath != " /var/root/":
        try:
            count = 0
            try:
                moving()
            except:
                state('*** This error is not fatal, it can occur when transfering large number of files! ***', 'y', 'n', 'n')
                state('*** It can appear a much more times, program is still copying files! ***', 'y', 'n', 'n')
                time.sleep(2)
                while count < 1000:
                    try:
                        count += 1
                        moving('s')
                        break
                    except:
                        state('*** This error is not fatal, it can occur when transfering large number of files! ***', 'y', 'n', 'n')
                        state('*** It can appear a much more times, program is still copying files! ***', 'y', 'n', 'n')
                        time.sleep(2)

        except:
            state('An error occured while changing the filepaths on recieveing device!', 'r')
            state('Check, if the path indicated is correct', 'r')
            input('Enter to exit: ')
            sys.exit()

# Checks if any flags were given to program
def arguments_check():

    try:
        if config() == 0:
            return 0
    except:
        print('An error occured while checking the configuration file!')
        print('Make sure the path is indicated correctly!')
        input('Enter to exit: ')
        return 0

    file = open(config_name, 'r')
    data = json.load(file)
    file.close()
    host = data[0]
    port = data[1]
    username = data[2]
    password = data[3]
    fpath = data[4]
    sys_logo = data[5]
    sys_print_slow = data[6]

    if sys.argv[1] == '--help':
        print('\nList of flags:\n1. -host or -h to modify host name only\n2. -port or -p to modify port only\n3. -username or -u to modify username only\n4. -password or -s to modify password only\n5. -path or -r to modify path only\n6. -mod_logo or -m to modify logo\n7. -print_config or -c to get config data\nFor params 1-5 you can also use -h new_host_name\nFor param 6 you can also use -m 1 0')
        return 0

    if sys.argv[1] == '-host' or sys.argv[1] == '-h':
        try:
            host = sys.argv[2]
        except:
            host = input('Enter new host name: ')
        lst = [host, port, username, password, fpath, sys_logo, sys_print_slow]
        file = open(config_name, 'w')
        file.write(json.dumps(lst))
        file.close()
        return 0

    if sys.argv[1] == '-port' or sys.argv[1] == '-p':
        src = 0
        try:
            port = sys.argv[2]
            src = 1
        except:
            port = input('Enter a new port number: ')
        def prt():
            port = input('Enter a new port number (eg. 22): ')
            try:
                port = int(port)
                return port
            except:
                print('Warning! Incorrect port number!')
                return False
        try:
            port = int(port)
        except:
            if src == 1:
                print('Warning! Incorrect port number! Indicate a new one')
            else:
                print('Warning! Incorrect port number!')
            port = prt()
            while port == False:
                port  = prt()
        lst = [host, port, username, password, fpath, sys_logo, sys_print_slow]
        file = open(config_name, 'w')
        file.write(json.dumps(lst))
        file.close()
        return 0

    if sys.argv[1] == '-username' or sys.argv[1] == '-u':
        try:
            username = sys.argv[2]
        except:
            username = input('Enter new username: ')
        lst = [host, port, username, password, fpath, sys_logo, sys_print_slow]
        file = open(config_name, 'w')
        file.write(json.dumps(lst))
        file.close()
        return 0

    if sys.argv[1] == '-password' or sys.argv[1] == '-s':
        try:
            password = sys.argv[2]
        except:
            password = input('Enter new password: ')
        lst = [host, port, username, password, fpath, sys_logo, sys_print_slow]
        file = open(config_name, 'w')
        file.write(json.dumps(lst))
        file.close()
        return 0

    if sys.argv[1] == '-path' or sys.argv[1] == '-r':
        try:
            fpath = sys.argv[2]
            fpath = '" ' + fpath + '"'
        except:
            fpath = input('Enter new path: ')
            fpath = '" ' + fpath + '"'
        lst = [host, port, username, password, fpath, sys_logo, sys_print_slow]
        file = open(config_name, 'w')
        file.write(json.dumps(lst))
        file.close()
        return 0

    if sys.argv[1] == '-mod_logo' or sys.argv[1] == '-m':

        try:
            p1 = sys.argv[2]
            p2 = sys.argv[3]
            sys_logo = bool(int(p1))
            sys_print_slow = bool(int(p2))
            lst = [host, port, username, password, fpath, sys_logo, sys_print_slow]
            file = open(config_name, 'w')
            file.write(json.dumps(lst))
            file.close()
            return 0
        except:
            print('')
            sys_logo = input('Enter sys_logo value (1/0): ')
            exit_101 = 0
            while exit_101 != 1:
                try:
                    sys_logo = bool(int(sys_logo))
                    exit_101 = 1
                except:
                    print('Failed to convert to bool!')
                    sys_logo = input('Enter sys_logo value (1/0): ')
            sys_print_slow = input('Enter sys_print_slow value (1/0): ')
            exit_101 = 0
            while exit_101 != 1:
                try:
                    sys_print_slow = bool(int(sys_print_slow))
                    exit_101 = 1
                except:
                    print('Failed to convert to bool!')
                    sys_print_slow = input('Enter sys_logo value (1/0): ')

            lst = [host, port, username, password, fpath, sys_logo, sys_print_slow]
            file = open(config_name, 'w')
            file.write(json.dumps(lst))
            file.close()
            print('Configurations has been saved!')
            return 0

    elif sys.argv[1] == '-print_config' or sys.argv[1] == '-c':
        
        print('\nHost ip: ' + host)
        print('Port: ' + str(port))
        print('Username: ' + username)
        print('Password: ' + password)
        print('Path: ' + fpath)
        print('Show logo: ' + str(sys_logo))
        print('Typewriter: ' + str(sys_print_slow))
        print('Config path: ' + config_path)
        print('Config name: ' + config_name)
        print('is_compiled: ' + str(is_compiled))
        return 0

    else:
        return None

# Used to manage other modules
def start():

    gb_exit = 0
    try:
        if arguments_check() == 0:
            gb_exit = 1
    except:
        None

    if gb_exit == 1:
        sys.exit()

    sys_end = 1

    if check() == 'Drag':

        if sys_logo == True:
            logo()
        else:
            logo('false')

        drag()

    else:
        try:
            print('Edit configuration data mode')
            config('setup')
            sys_end = 0
        except:
            print('An error occured while checking the configuration file!')
            print('Make sure the path is indicated correctly!')
            input('Enter to exit: ')
            sys.exit()

    if sys_end == 1:
        end()

# Initiates the whole program
start()
