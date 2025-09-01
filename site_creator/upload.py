import paramiko
import os
from tkinter import messagebox


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
        print(f"업로드 중 오류 발생: {e}")
        return False


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



def upload(path, domain, server, server_pass):
    project = os.path.join(os.getcwd(), 'page_default')
    server_path = '/root'
    server_username = 'root'
    if len(path) and len(domain) and len(server) and len(server_pass):
        if (os.path.exists(project)
                and (os.path.exists(os.path.join(path, 'white.html'))
                     and os.path.exists(os.path.join(path, 'static')))):
            upload_result = upload_server(project, server_path, server, server_username, server_pass,
                                          'project')

            if upload_result is True:
                upload_server(os.path.join(path, 'white.html'), server_path, server, server_username,
                              server_pass, 'white.html')
                upload_server(os.path.join(path, 'static.zip'), server_path, server, server_username,
                              server_pass, 'static.zip')
                messagebox.showinfo("성공", f"업로드 성공")
        else:
            messagebox.showinfo("실패", f"서버 정리 확인")
    else:
        messagebox.showinfo("실패", f"입력갑 확인")