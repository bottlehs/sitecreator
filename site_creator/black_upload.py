import paramiko
import os

def upload_server(local_path, remote_path, hostname, username, password, item_name=''):
    def upload_folder_recursive(local_folder_path, ec2_folder_path):
        for item in os.listdir(local_folder_path):
            local_item_path = os.path.join(local_folder_path, item)
            ec2_item_path = ec2_folder_path + '/' + item

            if os.path.isfile(local_item_path):
                sftp.put(local_item_path, ec2_item_path)
            elif os.path.isdir(local_item_path):
                try:
                    sftp.mkdir(ec2_item_path)
                except IOError:
                    pass
                upload_folder_recursive(local_item_path, ec2_item_path)

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        sftp = ssh.open_sftp()

        if os.path.isfile(local_path):
            remote_path = remote_path + '/' + item_name
            print(remote_path)
            sftp.put(local_path, remote_path)
        else:
            sftp.mkdir(remote_path + '/' + item_name)
            upload_folder_recursive(local_path, remote_path + '/' + item_name)

        sftp.close()
        ssh.close()

        return True

    except Exception as e:
        print(f"에러 ㅅㅂ: {e}")
        exit()


def run_commands(hostname, username, password, commands):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname, username=username, password=password)

        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()

            # print(f"{command}: {output}")

            if (error):
                print(f"ERROR!-{command}: {output}")
        ssh.close()

    except Exception as e:
        print(f"에러: {e}")

cp_cmd = ["cp -r /root/black.html /root/project/templates/"]

def black_upload(path, server, server_pass):

    print(path)
    print(server)
    print(server_pass)
    server_path = '/root'
    server_username = 'root'
    if len(path) and len(server) and len(server_pass):
        if (os.path.exists(path)):
            upload_server(path, server_path, server, server_username, server_pass, 'black.html')
            run_commands(server, server_username, server_pass, cp_cmd)

            print("✅ 블랙 업로드 성공")
        else:
            print("❌ 서버 정리 확인 필요")
    else:
        print("❌ 입력값 확인 필요")