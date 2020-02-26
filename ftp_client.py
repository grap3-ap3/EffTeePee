#!/usr/bin/env python3
########################################################################
#Author: Phil Grimes pgrimes 
#Python 3.7.5 (tags/v3.7.5:5c02a39a0b, Oct 15 2019, 00:11:34)
#[MSC v.1916 64 bit (AMD64)] on win32
#Description: 
##      This is a basic command line FTP client.
##      Use this program to connect to connect to, and interact with FTP servers.
##
__version__ = ('0.0.1a')
########################################################################
#######################DO NOT EDIT ABOVE THIS LINE######################

import ftplib
import sys

loggedIn = False

def getInputFromUser():
    try:
        myServer = input('Server?: ')
    except:
        print('No server defined!')
        exit()
        
    myUser = input('User? (enter for anonymous): ') or 'anonymous'
    myPass = input('Password? (enter for anonymous): ') or 'anonymous'

    myList = [myServer, myUser, myPass]
    
    return(myList)
    
def ftpLogin(server, user, password):
    ftp = ftplib.FTP(server)
    ftp.login(user, password)

    return(ftp)

def printAvailableCommands():
    print('''Command List:
            \t dir <dir> | List contents of <dir>. (Blank prints current directory)
            \t cwd <dir> | Set the current directory on the server.
            \t mkd <dir> | Create a new directory on the server.
            \t rmd <dir> | Remove the directory named <dir> on the server.
            \t dl <file> | Download  file to local system
            \t ul <file> | Upload file to server
            \t pwd       | Return the pathname of the current remote directory.
            \t help      | Print available commands
            \t quit      | Send a QUIT command to the server and close the connection.
            ''')

    return()


def main():
    try:
        print('Welcom to Python FTP Client!')
        infoList = getInputFromUser()
    except Exception as e:
        print(e)

    print('Attempting to log into server: ' + infoList[0])
    try:
        myFtp = ftpLogin(infoList[0], infoList[1], infoList[2])
        print('Logged in Successfully as user: ' + str(infoList[1]))
        loggedIn = True
    except Exception as e:
        print(e)

    if loggedIn == True:
        data = []
        myFtp.dir(data.append)
        #myFtp.quit()
        
        for line in data:
            print("-", line)

        printAvailableCommands()

        myCommand = ''

        #print(myCommand)

        while myCommand != 'quit':
            #myFtp.quit()
            myCommand = input('Enter a command: ')
            #print(str(myCommand))
            printAvailableCommands
            if str(myCommand) == 'help':
                printAvailableCommands()
            elif str(myCommand) == 'pwd':
                print('Printing current directory path: ')
                try:
                    print(myFtp.pwd())
                except Exception as e:
                    print(e)
            elif str(myCommand) == 'dir':
                print('Printing directory contents:')
                print(myFtp.dir())
            elif len(str(myCommand).split()) > 1:
                try:
                    commandList = str(myCommand).split()
                    print(commandList)
                    try:
                        theCommand = commandList[0]
                        #print(theCommand)
                    except Exception as e:
                        print(e)

                    try:
                        myDirectory = commandList[1]
                    except Exception as e:
                        print(e)

                    print('Executing command: %s' % str(myCommand))

                    if theCommand == 'cwd':
                        try:
                            myFtp.cwd(myDirectory)
                        except Exception as e:
                            print(e)
                    elif theCommand == 'dir':
                        try:
                            print(myFtp.dir(myDirectory))
                        except Exception as e:
                            print(e)
                    elif theCommand == 'mkd':
                        try:
                            myFtp.mkd(myDirectory)
                        except Exception as e:
                            print(e)
                    elif theCommand == 'rmd':
                        try:
                            myFtp.rmd(myDirectory)
                        except Exception as e:
                            print(e)
                    elif theCommand == 'dl':
                        if myDirectory.split('.')[1].lower() == 'txt':
                            try:
                                with open(myDirectory, 'wb') as fp:
                                    res = myFtp.retrbinary('RETR ' + myDirectory, fp.write)

                                    if not res.startswith('226 Transfer complete'):
                                        print('Download failed.')
                                        os.remove(myDirectory)

                                    print('Text transfer complete!')
                            except Exception as e:
                                print(e)
                        else:
                            try:
                                with open(myDirectory, 'wb') as fp:
                                    res = myFtp.retrbinary('RETR ' + myDirectory, fp.write, 1024)

                                    if not res.startswith('226 Transfer complete'):
                                        print('Download failed.')
                                        os.remove(myDirectory)

                                    print('Binary transfer complete!')
                            except Exception as e:
                                print(e)
                    elif theCommand == 'ul':
                        if myDirectory.split('.')[1].lower() == 'txt':
                            try:
                                with open(myDirectory) as fobj:
                                    res = myFtp.storlines('STOR ' + myDirectory, fobj)
                                    print(res)

##                                    if not res.startswith('226 Transfer complete'):
##                                        print('Download failed.')
##                                        os.remove(myDirectory)
##
##                                    print('Text transfer complete!')
                            except Exception as e:
                                print(e)
                        else:
                            try:
                                with open(myDirectory, 'rb') as fobj:
                                    res = myFtp.storbinary('STOR ' + myDirectory, fobj, 1024)
                                    print(res)
##                                    if not res.startswith('226 Transfer complete'):
##                                        print('Download failed.')
##                                        os.remove(myDirectory)
##
##                                    print('Binary transfer complete!')
                            except Exception as e:
                                print(e)

                    else:
                        print('Invalid command: ' + str(myCommand))
                    
                except Exception as e:
                    print(e)
                    print(str(myCommand))
            else:
               print('Invalid command: ' + str(myCommand))

        outtro = myFtp.quit()
        print(outtro)

    else:
        print('You are not logged in!')
        exit()


if __name__== "__main__":
    main()
