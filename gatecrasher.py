#!/bin/env python3
# gatecrasher: automated batch login to systems
# usage: python3 gatecrasher.py -c '/Users/user/.ssh/key' -u user -p password -i host/list
#        python3 gatecrasher.py -c '/Users/user/.ssh/key' -u user -p password -l '/Users/user/Desktop/hosts_file.txt'

import argparse
import paramiko

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--key', action="store")
parser.add_argument('-u', '--username', action="store")
parser.add_argument('-p', '--password', action="store")
parser.add_argument('-i', '--host', action="store")
parser.add_argument('-l', '--list', action="store")
args = parser.parse_args()

def create_ssh(host, username, password, key):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    try:
        print("creating connection to: {}".format(host))
        ssh.connect(host, username=username, key_filename=key, password=password)
        command_who = 'whoami'
        command_ver = 'uname -a'
        stdin, stdout, stderr = ssh.exec_command(command_who)
        for line in stdout.readlines():
            who_out = line
        stdin, stdout, stderr = ssh.exec_command(command_ver)
        for line in stdout.readlines():
            ver_out = line
        ssh.close()
        print("connected")
        return print(who_out,ver_out)
    except Exception as e:
        print('Connection Failed')
        print(e)

def main():
    if args.host:
        host_list = [str(args.host)]
    elif args.list:
        with open(args.list) as f:
            host_list = f.read().splitlines()
    username = args.username
    password = args.password
    key = args.key
    for host in host_list:
        create_ssh(host, username, password, key)

if __name__ == "__main__": # execute this as a program drectly. do not make available functions as standalone.
    main()
