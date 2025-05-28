import paramiko
import os

hostname = 'test_user.remote.server.com'
port = 22
username = 'test_username'
password = 'adhudnirjfklg'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    client.connect(hostname, port, username, password)

    stdin, stdout, stderr = client.exec_command('ls -la')
    print(stdout.read().decode())

    sftp = client.open_sftp()
    sftp.put('~/file.txt', "test_server:~/file.txt")
    sftp.close()

except Exception as e:
    print(f"connection failed：{e}")

finally:
    client.close()