import paramiko


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


clean_commands = [
    "rm -rf /root/project",
    "rm -rf /root/white.html",
    "rm -rf /root/static",
    "rm -rf /root/static.zip",
]

def clean(server, server_pass):
    run_commands(server, 'root', server_pass, clean_commands)
    print("✅ 서버 정리 완료")