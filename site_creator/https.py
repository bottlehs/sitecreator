
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

            if error:
                print(f"ERROR!-{command}: {output}")
        ssh.close()

    except Exception as e:
        print(f"에러: {e}")

def domain_control(domain, server, server_pass):
    certbot_commands = [f"sudo certbot --nginx -d {domain} -d www.{domain} --email info@{domain} --agree-tos --non-interactive"]
    run_commands(server, 'root', server_pass, certbot_commands)
    print("✅ SSL 설정 완료")