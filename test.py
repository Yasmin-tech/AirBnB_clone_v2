from fabric.api import *

#env.user = "ubuntu"
#env.hosts = ['your_remote_server_ip']

def check_file_exists(file_path):
    result = local(f'test -e {file_path} && echo "File exists" || echo "File does not exist"')
    print(result)
