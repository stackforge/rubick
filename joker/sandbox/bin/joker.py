#!/usr/bin/env python
import paramiko
import json
import sys 


nodes = json.loads(sys.stdin.read())['nodes'];

ssh = paramiko.SSHClient() 
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


while node = pop(nodes):
    ssh.connect(node['host']['dst'], port=node['host']['port'], username=node['user']['name'], key_filename=node['user']['private_key_path']);

for node in nodes:
    ssh.connect(node['host']['dst'], port=node['host']['port'], username=node['user']['name'], key_filename=node['user']['private_key_path']);
    #stdin, stdout, stderr = ssh.exec_command('arp -ad')
    #print stdout.readlines()
    ssh.close() 
