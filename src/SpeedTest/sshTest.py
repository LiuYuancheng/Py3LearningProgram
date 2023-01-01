import paramiko

command = "df"

# Update the next three lines with your
# server's information

host = "gateway.ncl.sg"
username = "ncl-yuancheng"
password = "lyc1987@LYC"

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
_stdin, _stdout,_stderr = client.exec_command("ls")
print(_stdout.read().decode())
client.close()