import paramiko
import os

ec2_host = "23.20.49.160"
ec2_port = 22
ec2_user = "ec2-user"
pem_key_path = "my-key.pem"

local_file_path =  os.path.expanduser("~/venv.txt")
remote_file_path = "/home/ec2-user/venv.txt"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ec2_host, username=ec2_user, key_filename=pem_key_path)

sftp = ssh.open_sftp()
sftp.put(local_file_path, remote_file_path)
sftp.close()

ssh.close()