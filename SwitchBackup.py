#!/usr/bin/env python3
import getpass
import os
import sys
import netmiko
import paramiko


# function to open file containing contents (IP address, credentials, Commands)
def Openfile(path, filenm):
    if os.path.exists(path):
        os.chdir(path)

        if os.path.exists(filenm):
            fileobj = open(filenm)
            return fileobj


# Function to create Text file in write mode to save device config
def CreatFiles(path, filenm):

    if os.path.exists(path):
        os.chdir(path)
        filename = filenm + ".txt"
        fileobj = open(filename,'w')
        return fileobj


if __name__ == "__main__":

    path1 = "C:\ConfBackup"
    path2 = "C:\ConfBackup\Config_files"

# variable to hold file names of contents
    IPs = "IPAddresses.txt"
    credentials = "Credentials.txt"
    commands = "Commands.txt"
    login = []
    cmdlist = []


# function call to get content from text files
    creds = Openfile(path1, credentials)
    ipaddress = Openfile(path1, IPs)
    cmds = Openfile(path1, commands)

# store all command in a list
    for line in cmds:
        cmdlist.append(line)


# store all logn credentials in a list
    for line in creds:
        login.append(line)

    username = login[0].strip()
    password = login[1].strip()
    enableSecret = login[2].strip()


# loop through each IP and capture command output
    for line in ipaddress:
        host = line
        try:
            ssh_session = netmiko.ConnectHandler(device_type='cisco_ios', ip=host, username=username, password=password, secret=enableSecret)
            ssh_session.enable()
            prompt = ssh_session.find_prompt()
            switchname = prompt.strip('#)')
            txtfile = CreatFiles(path2, switchname)
            txtfile.write(prompt + '\n' + prompt)
            ssh_session.send_command("terminal length 0")

            print('\n' + 'Taking configuration backup from ' + host, end='')
            for cmd in cmdlist:
                txtfile.write(cmd + '\n' + ssh_session.send_command(cmd))

                for k in range(8):
                    txtfile.write('\n' + prompt)

            ssh_session.disconnect()
            txtfile.close()

        except (netmiko.ssh_exception.NetMikoTimeoutException, netmiko.ssh_exception.NetMikoAuthenticationException, paramiko.ssh_exception.SSHException) as s_error:
            print(s_error)

    print('\n' + "Backup Completed")
    input("Enter any key to close")